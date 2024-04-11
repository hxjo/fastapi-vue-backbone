from typing import cast

import urllib.parse

import asyncpg


async def async_database_exists(url: str) -> bool:
    # Remove "postgresql+asyncpg://" prefix and parse
    clean_url = url.replace("postgresql+asyncpg://", "")
    parsed_url = urllib.parse.urlparse(f"//{clean_url}")
    dbname = parsed_url.path[1:]  # Extract the database name from the path
    user = parsed_url.username
    password = parsed_url.password
    host = parsed_url.hostname
    port = parsed_url.port if parsed_url.port else 5432

    default_dbname = "postgres"  # Default database to connect to for the check
    try:
        # Connect using asyncpg
        conn = await asyncpg.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=default_dbname,
        )
        # Query to check if the database exists
        exists = await conn.fetchval(
            "SELECT EXISTS(SELECT 1 FROM pg_database WHERE datname=$1)", dbname
        )
        await conn.close()
        return cast(bool, exists)
    except Exception as e:
        print(f"Error checking database existence: {e}")
        return False


async def async_create_database(url: str) -> None:
    clean_url = url.replace("postgresql+asyncpg://", "")
    parsed_url = urllib.parse.urlparse(f"//{clean_url}")
    dbname = parsed_url.path[1:]
    user = parsed_url.username
    password = parsed_url.password
    host = parsed_url.hostname
    port = parsed_url.port if parsed_url.port else 5432

    default_dbname = "postgres"
    try:
        conn = await asyncpg.connect(
            user=user, password=password, host=host, port=port, database=default_dbname
        )
        await conn.execute(f'CREATE DATABASE "{dbname}"')
        await conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")
        raise


async def async_drop_database(url: str) -> None:
    clean_url = url.replace("postgresql+asyncpg://", "")
    parsed_url = urllib.parse.urlparse(f"//{clean_url}")
    dbname = parsed_url.path[1:]
    user = parsed_url.username
    password = parsed_url.password
    host = parsed_url.hostname
    port = parsed_url.port if parsed_url.port else 5432

    default_dbname = "postgres"
    try:
        conn = await asyncpg.connect(
            user=user, password=password, host=host, port=port, database=default_dbname
        )
        await conn.execute(f'DROP DATABASE IF EXISTS "{dbname}"')
        await conn.close()
    except Exception as e:
        print(f"Error dropping database: {e}")
        raise
