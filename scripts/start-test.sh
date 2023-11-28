#! /bin/bash
docker compose -p nutrition -f compose-db-test.yaml --env-file ./.env.testing up --build -d
docker compose -p nutrition -f compose-server-test.yaml --env-file ./.env.testing up --build -d
