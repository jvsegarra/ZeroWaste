# ZeroWaste
## Main goal
Deliver leftovers from stores to social shelters

## Structure
Project following the guidelines of Domain Driven Design

## Open the project initially in 'dev' environment
* run `git clone `
* create a `.env` file in the root folder copying the `.env.template` file in the repository.
* in a terminal, from the root folder run `make run`
* open `http://127.0.0.1:8000/docs` to see the apidoc

## Run/stop the project in 'dev' environment
* To stop the running the project run `make stop`
* To run the project again, just run `make run`

## Run tests:
### Out of the container
* run `make test` to run all the tests
* run `make unit_test` to run all the unit tests
* run `make integration_test` to run all the integration tests
* run `make test path="<filepath>"` to run specific test files or folders

### In the container
* run `pytest tests/` to run all the tests
* run `pytest tests/unit/` to run all the unit tests
* run `pytest tests/integration/` to run all the integration tests
* run `pytest <filepath>` to run specific test files or folders
* run `pytest <filepath> -k "<test_method_name>"` to run one specific test in a test file

## Run / display coverage
* run `make coverage`
* open coverage report in the generated folder `htmlcov/index.html`

## API documentation:
* the API documentation can be found at the `/docs` endpoint
* call the endpoint from the browser to get an interactive Swagger UI

## Open Postgres DB terminal
* run `make dbshell`
* run `\q` to exit psql terminal

## Migrations:
### Create new migration:
* run `make new_migration name=<migration name>`
* edit the new migration that has been created inside `/migrations/versions`
### Apply migrations:
* run `make apply_migrations`
### View migrations history:
* run `make view_migrations`
### Upgrade/downgrade migrations:
* open a shell with `make shell`
* run `alembic upgrade +n` or `alembic downgrade -n`,
  where n is the number of migrations you want to go back/forward to.

## Debug
* copy `.env.debug` into `.env`
* start db container and pycharm debugger pointing to `main.py`
