#! /bin/bash
docker compose -p nutrition -f compose-db-test.yaml --env-file ./.env.testing up --build -d
docker compose -p nutrition -f compose-server-test.yaml --env-file ./.env.testing up --build -d

docker exec nutrition-test-server python -m unittest

echo "Stopping Docker containers..."
docker stop nutrition-test-server nutrition-test-db
