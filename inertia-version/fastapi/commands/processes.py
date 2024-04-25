import os
import subprocess
import time
from typing import Any
import queue as base_queue

import multiprocessing
from multiprocessing.synchronize import Event
import logging
import logging.handlers



def setup_logger(queue: Any) -> None:
    """Set up the logger configuration."""
    handler = logging.handlers.QueueHandler(queue)  # Send events to the queue
    root = logging.getLogger()
    root.addHandler(handler)
    root.setLevel(logging.DEBUG)


def logger_listener(queue: Any) -> None:
    """Listen for log messages on the queue and process them."""
    try:
        while True:
            try:
                record = queue.get(timeout=1)  # Timeout to allow periodic check
                if record is None:  # Sentinel value to tell the listener to quit.
                    break
                logger = logging.getLogger(record.name)
                logger.handle(record)
            except base_queue.Empty:
                continue
    except KeyboardInterrupt:
        print("Logger listener received KeyboardInterrupt")


def backend(queue: Any, host: str, port: int, shutdown_event: Event) -> None:
    setup_logger(queue)
    logger = logging.getLogger("Backend")
    logger.info("Backend started")
    app_port = os.getenv("FASTAPI_PORT", str(port))
    app_host = os.getenv("FASTAPI_HOST", host)
    process = None
    try:
        process = subprocess.Popen(
            ["poe", "runapp", "--host", app_host, "--port", app_port]
        )
        while not shutdown_event.is_set():
            if process.poll() is not None:
                break
            time.sleep(0.5)
    except KeyboardInterrupt:
        logger.info("Backend received KeyboardInterrupt")
    finally:
        if process and process.poll() is None:
            process.terminate()
            process.wait()
        logger.info("Backend shutting down")


def frontend(queue: Any, shutdown_event: Event) -> None:
    setup_logger(queue)
    logger = logging.getLogger("Frontend")
    logger.info("Frontend started")
    process = None
    try:
        process = subprocess.Popen(
            ["npm", "run", "dev", "--", "--host", "0.0.0.0"],
            cwd=os.path.join(os.path.dirname(__file__), "..", "..", "vue"),
        )
        while not shutdown_event.is_set():
            if process.poll() is not None:
                break
            time.sleep(0.5)
    except KeyboardInterrupt:
        logger.info("Frontend received KeyboardInterrupt")
    finally:
        if process and process.poll() is None:
            process.terminate()
            process.wait()
        logger.info("Frontend shutting down")


def run_apps(host: str, port: int) -> None:
    shutdown_event = multiprocessing.Event()
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    log_queue: Any = multiprocessing.Queue()

    listener = multiprocessing.Process(
        target=logger_listener, args=(log_queue,)
    )
    listener.start()

    p1 = multiprocessing.Process(
        target=backend, args=(log_queue, host, port, shutdown_event)
    )
    p2 = multiprocessing.Process(target=frontend, args=(log_queue, shutdown_event))

    try:
        p1.start()
        p2.start()

        p1.join()
        p2.join()

    except KeyboardInterrupt:
        print("Caught KeyboardInterrupt, signaling processes to terminate")
        shutdown_event.set()

    finally:
        # Ensure all processes are terminated before exiting
        p1.join()
        p2.join()
        print("Processes have been terminated.")

        # Tell the logger_listener to finish
        log_queue.put(None)
        # Assuming `listener` is a process that needs to be joined
        listener.join()
        print("Logger listener has finished.")
