import pika
import json
import random
import time  

# RabbitMQ connection settings
RABBITMQ_HOST = '127.0.0.1'
RABBITMQ_PORT = '15672'
RABBITMQ_USER = 'guest'
RABBITMQ_PASSWORD='guest'
RABBITMQ_QUEUE = 'mqtt_queue'


def send_message():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

    while True:
        status = random.randint(0, 6)
        message = {
            "status": status,
            "timestamp": time.time()
        }
        channel.basic_publish(
            exchange='',
            routing_key=RABBITMQ_QUEUE,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,
            ))
        print(f"Sent: {message}")
        time.sleep(1)

    connection.close()

if __name__ == "__main__":
    send_message()
