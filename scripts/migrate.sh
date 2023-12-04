#! /bin/bash

if [ "$1" = "" ]
then
    echo "Please provide a migration message."
    exit 1
fi

docker exec -u 0:0 nutrition-local-server python -m flask db migrate -m "$1"
