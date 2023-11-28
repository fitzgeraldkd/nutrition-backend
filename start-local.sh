#! /bin/bash
docker compose -p nutrition -f compose-db-local.yaml --env-file ./.env.local up --build -d
docker compose -p nutrition -f compose-server-local.yaml --env-file ./.env.local up --build -d
docker exec nutrition-local-server python -m flask db upgrade
