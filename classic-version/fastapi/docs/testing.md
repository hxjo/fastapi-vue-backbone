# Testing
We're using pytest-xdist, which allows us to run tests concurrently, in order to make it faster.

## With poe
You can run the entire suite wiht `poe test` or target files with the same command.

## With your IDE
You can install the `pytest` extension from VSCode, or from any other IDE given it has the `pytest` extension

## Fixtures
Some fixtures are defined in `app/conftest.py`.
You can use `session` and `app` safely, as both target a test database, created for each test session and dropped at the end.
You can also use `background_tasks`, which is a mocker around FastAPI's `BackgroundTasks`.
You can use `fga_client` safely, as it targets a test store, created for each test and deleted at the end.

You're free to create more fixtures, but if they're not meant to be generic, please do so either in the test file, or in the test class.

## Model factories
You can create new factories in `app/modules/**/tests/factory.py`. 
You should at least create one which provides random values (a `new_default_**` function).
Once done, please update the `app/common/test_utils/factory.py` class to add your tuple, so we can use
`factory(Model, **kwargs)` in the tests.
This is used to ease the creation of new objects while creating them in the OpenFGA model, and in the Meilisearch database for example.
