# Nutrition Backend

## Setup

### Environment

Two environment files are required: `.env.local` and `.env.testing`. The variables required for the app to run are as follows:

- `secret_key`: The secret key for the main Flask app.
- `server_port`: The port that the Flask app runs on.
- The database connection info should be included in these variables:
    - `db_username`
    - `db_password`
    - `db_host`
    - `db_port`
    - `db_database`
- `food_data_central_api_key`: The API key for the US FoodData Central (request for free [here](https://fdc.nal.usda.gov/)). Not required for the testing environment.

It may help to have the `server_port` and `db_port` variables be different between the local and testing environments, so that both environments can be up and running simultaneously.

### Running

The local and test environments can be started by running these scripts.
Note: make sure you are in the root directory when running these.

```
./scripts/start-local.sh
./scripts/start-test.sh
```

The environments can be stopped by running these scripts.

```
./scripts/stop-local.sh
./scripts/stop-test.sh
```

## Testing

The full test suite can be ran with:

```
./scripts/run-tests.sh
```
