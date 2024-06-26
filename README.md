# MQTT Messaging with RabbitMQ and MongoDB

This project demonstrates a client-server script in Python that handles MQTT messages via RabbitMQ.

## Prerequisites

Before you start, ensure you have the following installed:

1. Python   : 3.12.1
2. RabbitMQ : 3.13.3
3. MongoDB  : 7.0.4 

## Installation

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/python_rabbitmq_message/mqtt-rabbitmq-mongodb.git
    cd mqtt-rabbitmq-mongodb
    ```

2. **Create a Virtual Environment**:

    ```bash
    python -m venv .venv
    `.venv\Scripts\activate`
    ```

3. **Install Dependencies**:

    ```bash
    pip install paho-mqtt pika pymongo flask
    ```

## Configuration

Ensure RabbitMQ and MongoDB services are running on your machine. The default configuration assumes the services are accessible at `localhost`.

## Running the Server

1. **Start the Server**:

    ```bash
    python d_server.py
    ```

    The server will start and listen for incoming messages from RabbitMQ. It also provides an HTTP endpoint for querying the status counts.

## Running the Client

1. **Start the Client**:

    Open a new terminal and navigate to the project directory, then run:

    ```bash
    python d_client.py
    ```

    The client will start sending MQTT messages to RabbitMQ every second.

## Querying the Server

You can query the status counts by making a GET request to the `/status_count` endpoint with `start_time` and `end_time` parameters in UNIX timestamp format.

Example:

```bash
GET "http://localhost:5000/status_count?start_time=START_TIMESTAMP&end_time=END_TIMESTAMP"
