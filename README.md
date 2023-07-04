# Event Management System

The Event Management System is a web application built with Django that allows users to manage events, registrations, venues, and users. It provides features for event creation, registration management, venue management, user profile access, and more.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Testing](#testing)
- [Contributing](#contributing)

## Installation

1. Clone the repository:
  ```
  git clone https://github.com/vanimittal1304/Django_Event_Management
  ```

2. Install the required packages:
  ```
  pip install -r requirements.txt
  ```

3. Set up the database:
- Configure the database settings in `settings.py`.
- Run migrations:
  ```
  python manage.py migrate
  ```

4. Create a superuser:
  ```
  python manage.py createsuperuser
  ```

## Usage

1. Start the development server:
  ```
  python manage.py runserver
  ```

2. Access the application in your web browser at `http://localhost:8000/`.

3. Use the provided API endpoints to interact with the application.

## API Endpoints

The application provides the following API endpoints:

- `/admin`: To access admin panel.
- `/api/upcoming-events`: GET request to fetch a list of upcoming events.
- `/api/filter-events`: GET request to filter events based on categories, tags, date, or location.
- `/api/event-details/<event_id>`: GET request to get details of a specific event.
- `/api/register`: POST request to register for an event.
- `/api/rsvp/<event_id>`: POST request to RSVP for an event.
- `/api/registration-history`: GET request to fetch the registration history of the authenticated user.

For detailed API documentation, refer to the [API documentation file](API_DOCUMENTATION.md).

## Authentication

The application uses JSON Web Tokens (JWT) for authentication. To authenticate, make a POST request to the `/api/token` endpoint with the username and password. The response will contain an access token, which should be included in the `Authorization` header of subsequent requests.

## Testing

To run the test cases, use the following command:
  ```
  python manage.py test
  ```

For detailed test coverage, refer to the [test coverage report file](TEST_COVERAGE.md).

## Contributing

Contributions to the Event Management System are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

