# Solution Documentation

## Overview

In this solution, we have built a simplified trading API that allows for order placement via a REST API. The API handles the creation of orders, stores them in a database, and subsequently triggers an asynchronous task to place the order at the stock exchange.

The primary goal of this solution is to ensure that the API is:
1. **Highly Scalable**
2. **Reliable**
3. **Resilient to failures**

### Key Requirements:
- **Highly Scalable**: The system should be capable of handling a high volume of requests and operations efficiently.
- **Reliable**: The API should remain responsive even when the stock exchange system fails or has connection issues. The reliability of the stock exchange interaction should not affect the reliability of the API.
- **Asynchronous Order Status Update**: The order status will be updated asynchronously after placing the order, and users can check the status of the order through the `GET` API.

The solution involves the following components:
- **FastAPI** for the API layer.
- **SQLAlchemy** for ORM-based database interaction.
- **Celery** for handling asynchronous tasks.
- **Redis** as the message broker for Celery.
- **SQLite** as the database for order storage.
- **Docker** for containerization and ensuring consistent environments.

## Key Decisions

**1. FastAPI for the API Layer**

**2. SQLAlchemy for Database Interaction**

**3. Celery for Asynchronous Task Management**

**4. SQLite as the Database**

**5. Redis as the Broker for Celery**

**6. Docker for Containerization**

## Solution Implementation

### 1. **POST /orders Endpoint**
The `/orders` endpoint accepts a POST request to create an order. It saves the order to the database and then triggers a Celery task to place the order at the stock exchange.

**Key Responsibilities:**
- Accepts order details.
- Saves order to the database using SQLAlchemy.
- Triggers an asynchronous task to place the order at the stock exchange.

The reliability of the **POST /orders** endpoint is ensured because:
- **Order Placement** is handled asynchronously by Celery, so even if the stock exchange is down or facing issues, the **POST /orders** endpoint will not be blocked.
- The endpoint will always return a **201 status code** indicating that the order has been successfully created, and the task of placing the order at the stock exchange will happen asynchronously.

### 2. **Celery Task for Placing Orders**
The Celery task runs asynchronously and tries to place the order at the stock exchange. If the stock exchange is unavailable, the task retries with exponential backoff for up to three attempts.

**Key Responsibilities:**
- Retrieve the order from the database.
- Attempt to place the order at the stock exchange.
- Update the order status to "placed" once successful.

If there are any issues in placing the order at the stock exchange, the task will retry. In case of a failure after all retry attempts, the order status will be marked accordingly.

### 3. **Place Order Function**
This function simulates placing an order at the stock exchange. It randomly fails to simulate connection issues, which is handled by the Celery retry mechanism.

**Key Responsibilities:**
- Simulates placing an order at the stock exchange.
- Simulates network failure for testing retry behavior.

### 4. **Database Models and Session Management**
Orders are stored in a database (SQLite in this case) with the `OrderDB` model using SQLAlchemy ORM. Each order contains essential fields like `id`, `status`, `created_at`, etc.

**Key Responsibilities:**
- Define the database schema for storing orders.
- Create and initialize the database using SQLAlchemy.

### 5. **Order Status Updates (Async)**
After the order is created through the `POST /orders` endpoint, the order status will be updated asynchronously as part of the Celery task that interacts with the stock exchange. The `GET /orders/{order_id}` endpoint can be used to check the status of an order.

**Key Responsibilities:**
- The order status will initially be set to "pending" and updated to "placed" once the order has been successfully placed at the stock exchange.
- The `GET /orders/{order_id}` endpoint allows clients to check the status of the order at any point in time, providing the current state of the order (e.g., "pending," "placed," or "failed").

### 6. **Error Handling**
If there is an error during the creation of the order or the placement of the order at the stock exchange, the API returns a `500 Internal Server Error` with a generic message:
```json
{
  "message": "Internal server error while placing the order"
}
```

### 7. **Testing**
Unit tests are written using pytest to verify the functionality of the API. The tests ensure that:
- Orders are successfully created and stored in the database.
- The Celery task correctly handles order placement.
- Proper error handling occurs when something goes wrong.
Tests also ensure that the correct status codes are returned for different scenarios, including success and failure cases.

### 8. **Dockerization**
The application is containerized using Docker to ensure a consistent development and deployment environment. The docker-compose.yml file sets up the necessary services:
- FastAPI app
- Celery worker
- Redis broker

### 9. **Future Improvements**
- **Database Migration**: For larger-scale applications, a database migration tool like Alembic should be used to handle schema changes and version control.
- **Task Retry Mechanism**: The retry logic for the Celery task can be improved, and the retry count can be made configurable.
- **Scalability**: The use of SQLite limits scalability, so switching to a production-grade database like PostgreSQL or MySQL should be considered for high-volume systems.
- **Error Reporting**: Adding more detailed error reporting (e.g., logging, monitoring) can help troubleshoot issues in production environments.

### 9. **Bonus Task**
To handle a large number of real-time order execution updates, we introduce the following changes:
- A dedicated WebSocket client listens for execution updates and publishes them to a message queue.
- A separate worker listens to Redis Pub/Sub and updates the order status in the database.
- Optimize Database for High-Volume Updates