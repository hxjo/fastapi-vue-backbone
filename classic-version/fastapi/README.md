# FastAPI backbone

## Installation
> In all cases, you'll need to have a `.env` file. You can copy the 
> - `../.env.example` file (if you are running fastAPI in local) and edit it to your needs.
> - `../.env.example.docker` file (if you are running fastAPI in a docker container, eg: with dev caontainers) and edit it to your needs.

### With dev containers
You can run the project in dev containers.
For VSCode, you can install the extension `Dev containers` and run the command:
`Dev containers: Rebuild and reopen in Container`.

This will create the necessary services in a docker-compose and reopen VSCode in a dev container.  
This allows you to not worry about anything related to versioning, etc. and work easily.  

> Note: You'll be asked for your ssh key on dev container creation, this is so your ssh key is passed to the dev container.  
> That way you can use git commands from the container.

### Without dev containers, with fastAPI in Docker
#### I don't have python on my machine
Run the following commands:
```shell
cp .env.example.docker .env
docker compose up -d --build
docker exec -it backbone-backend-1 poe cmd setup setup-after-docker
```

Please note that you'll have to `sh` into the container to run any command.
You can do so with `docker exec -it backbone-backend-1 sh`

#### I have python on my machine
Run the following commands:
```shell
pip3 install poetry

# Either create the virtual environment here:
poetry config virtualenvs.in-project true
poetry install
source .venv/bin/activate

# Or create it with poetry's default behaviour
poetry install
poetry shell

cp .env.example.docker .env
poe cmd setup setup  # Then choose to install fastAPI in docker
```

### Without dev containers, with fastAPI in local
Run the following commands:
```shell
pip3 install poetry

# Either create the virtual environment here:
poetry config virtualenvs.in-project true
poetry install
source .venv/bin/activate

# Or create it with poetry's default behaviour
poetry install
poetry shell

cp .env.example .env
poe cmd setup setup  # Then choose to install fastAPI in local
poe run  # Start the app
````

## Access the back-office
To access the back-office, you'll first need to ensure the project is installed and all migrations are properly run.  
You also need to have a user with is_superuser set to True  

To create / get superuser rights, you can run `poe cmd admin i` and either create one 
or set yourself superuser.
Note you need to have the app running (at least the database), you can use
- `poe run_services` (runs the services)
- `poe run` (runs the services and the app)

You can then visit [the backoffice](http://127.0.0.1:8000/admin)


## Useful commands
- see all available commands `poe --help`
- run the interactive commands menu `poe cmd`
- run the app: `poe run`
- make migrations: `poe migrations`
- migrate: `poe migrate`
- rollback last migrate operation: `poe rollback`
- format app folder content with black, isort and autoflake: `poe format`
- add dependencies: `poetry add $dependency_name`

## General Documentation

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLModel](https://sqlmodel.tiangolo.com/)
- [OpenFGA](https://openfga.dev/docs/authorization-and-openfga)
- [Meilisearch](https://www.meilisearch.com/docs)
- [Alembic (migration handler)](https://alembic.sqlalchemy.org/en/latest/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [SQLAlchemy Model Factory](https://sqlalchemy-model-factory.readthedocs.io/en/latest/factories.html)


## Technical documentation
- [Routes CSV](https://epitechfr-my.sharepoint.com/:x:/g/personal/malo_genty_epitech_eu/EUS-smd3gE5KuASTtlf0UjABI9W55fBO56CYgMrqWtD1vg)

## Features documentation
- [Authentication documentation](docs/auth.md)
- [Authorization documentation](docs/authz.md)
- [Testing documentation](docs/testing.md)

## API Documentation
- [Swagger](http://127.0.0.1:8000/api/docs)
- [Redoc](http://127.0.0.1:8000/api/redoc)