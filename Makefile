list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

run:
	docker-compose up --build

stop:
	docker-compose down

shell:
	docker exec -i -t zerowaste_zw-api_1 bash

dbshell:
	docker-compose exec zw-db psql -U zw # \q + enter to exit psql

new_migration:
	docker-compose exec zw-api alembic revision -m "$(name)"

apply_migrations:
	docker-compose exec zw-api alembic upgrade head

view_migrations:
	docker-compose exec zw-api alembic history --verbose

test:
	if [ -z "$(path)" ]; then \
		docker-compose exec zw-api pytest tests/; \
	else \
		docker-compose exec zw-api pytest "$(path)"; \
	fi

unit_test:
	docker-compose exec zw-api pytest tests/unit/

integration_test:
	docker-compose exec zw-api pytest tests/integration/

coverage:
	docker-compose exec zw-api pytest --cov=app --cov-report html tests/

format:
	docker-compose exec zw-api black --config=./pyproject.toml .
