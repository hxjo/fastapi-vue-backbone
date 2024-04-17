# FastAPI & Vue Backbone

## Installation
> In all cases, you'll need to have a `.env` file. You can copy the 
> - `.env.example` file (if you are running fastAPI and Vue in local) and edit it to your needs.
> - `.env.example.docker` file (if you are running fastAPI and Vue in a docker container or dev-container) and edit it to your needs.

### With dev containers
You can run the project in dev containers.
For VSCode, you can install the extension `Dev containers` and run the command:
`Dev containers: Rebuild and reopen in Container`.
In Jetbrains IDEs, you can access them through the `Show dev containers` actions. You can then follow
the instructions to build it.

This will create the necessary services in a docker-compose and reopen your IDE in a dev container.  
This allows you to not worry about anything related to versioning, etc. and work easily.  

> Note: You'll be asked for your ssh key on dev container creation, this is so your ssh key is passed to the dev container.  
> That way you can use git commands from the container.

### Without dev containers, using Docker
Run the following commands:
```shell
cp .env.example.docker .env
docker compose up -d --build
docker exec -it backbone-backend-1 poe cmd setup setup-after-docker
```

Please note that you'll have to run commands in the container.
You can do so with `docker exec -it backbone-app-1 poe <your command>`


### Without dev containers, in local
Run the following commands:
```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
# Then open a new terminal and run
cd fastapi
uv venv
source .venv/bin/activate
uv pip install -r requirements.dev.in

cp .env.example .env
poe run

# Then, in another terminal
cd ../vue
npm run dev
````

## Generate The api services in Vue
You first need to get the openapi.json schema
You can generate it with the following command: `poe cmd` and selecting the `Generate OpenAPI schema` option. 

You can use the following command to generate the api services in Vue:
From the `vue` folder, run the following command:
```shell
npx @hey-api/openapi-ts -i ../openapi.json -o src/api
```


## Access the back-office
To access the back-office, you'll first need to ensure the project is installed and all migrations are properly run.  
You also need to have a user with is_superuser set to True  

To create / get superuser rights, you can run `poe cmd admin i` and either create one 
or set yourself superuser.
Note you need to have the app running (at least the database), you can use `poe run`
If you're using dev containers, you can run the command from the container.
If you're using docker, you can run the command like so: `docker exec -it backbone-app-1 poe cmd admin i`

You can then visit [the backoffice](http://127.0.0.1:8000/admin)


## Useful commands
- see all available commands `poe --help`
- run the interactive commands menu `poe cmd`
- open a shell `poe shell`
- run the app: `poe run`
- make migrations: `poe migrations`
- migrate: `poe migrate`
- rollback last migrate operation: `poe rollback`
- format app folder content with ruff: `poe format`
- do a pre-commit check: `poe pc`
- add dependencies: `poetry add $dependency_name`

## General Documentation

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLModel](https://sqlmodel.tiangolo.com/)
- [OpenFGA](https://openfga.dev/docs/authorization-and-openfga)
- [Meilisearch](https://www.meilisearch.com/docs)
- [Alembic (migration handler)](https://alembic.sqlalchemy.org/en/latest/)
- [SQLAlchemy](https://www.sqlalchemy.org/)

## Features documentation
- [Authentication documentation](fastapi/docs/auth.md)
- [Authorization documentation](fastapi/docs/authz.md)
- [Testing documentation](fastapi/docs/testing.md)

## API Documentation
- [Swagger](http://127.0.0.1:8000/api/docs)
- [Redoc](http://127.0.0.1:8000/api/redoc)