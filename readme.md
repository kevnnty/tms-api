# Transport Management System API

This is a basic API for managing drivers and routes in a transport management system.
Check out Django version of the system [here](https://github.com/kevnnty/tms)

## Features

- **Route Management:** Create, update, and delete routes with details including start and end locations, estimated travel time, and assigned vehicles.
- **Vehicle Management:** Register vehicles, view assigned routes, and track the availability of vehicles for each route.
- **Driver Management:** Manage drivers, assign vehicles to drivers, and view driver details.
- **Pagination and Filtering:** Efficient pagination and filtering to manage a large number of records seamlessly.
- **User Authentication:** Secure login and registration to manage data.
- **Analytics:** Analytics about Vehicle informance and Driver performance (Coming soon)

## Technologies Used

- **FastAPI**: For building the API.
- **SQLAlchemy**: For database models and ORM.
- **PostgreSQL**: Database .

## Endpoints

### `/drivers`

- **POST** `/drivers/`: Create a new driver.
- **GET** `/drivers/`: Get a list of all drivers.
- **GET** `/drivers/{driver_id}/`: Get a specific driver by ID.
- **PUT** `/drivers/{driver_id}/`: Update a driver's details.
- etc

### `/routes`

- **POST** `/routes/`: Create a new route.
- **GET** `/routes/`: Get a list of all routes.
- **GET** `/routes/{route_id}/`: Get a specific route by ID.
- **PUT** `/routes/{route_id}/`: Update a route's details.
- etc

## Database

By default, the application uses **PostgreSQL** for development. The database URL should be specified in the `.env` file using the `DATABASE_URL` environment variable. Check `.env.example` for more information.


## How to run

### Clone the repository
```
git clone https://github.com/kevnnty/tms-api.git
cd tms-api
```

### Setup and enable virtual environment
```
python -m venv venv
\venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the API using uvicorn

```bash
uvicorn app.main:app --reload
```
This will start the server on `http://127.0.0.1:8000`. The --reload option enables auto-reloading during development.


### Testing the API
Once the server is running, you can interact with the API using tools like Postman, Insomnia or Thuner Client. You can also view the interactive API documentation provided by FastAPI at [Swagger docs](http://127.0.0.1:8000/docs).


## Maintained by

This project is actively maintained by [Kevin](https://github.com/kevnnty).
