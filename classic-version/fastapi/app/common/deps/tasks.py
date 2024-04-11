from fastapi import BackgroundTasks, Depends


def tasks(background_tasks: BackgroundTasks) -> BackgroundTasks:
    """Just a wrapper dependency for BackgroundTasks"""
    return background_tasks


TaskDep = Depends(tasks)
