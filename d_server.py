import pika
import json
from pymongo import MongoClient
from flask import Flask, request, jsonify
from datetime import datetime
from threading import Thread
import signal
import os

# MongoDB settings
MONGO_URI = 'mongodb://localhost:27017/'
MONGO_DB = 'sensor_data'
MONGO_COLLECTION = 'status_messages'

# RabbitMQ settings
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT= '15672'
RABBITMQ_QUEUE = 'mqtt_queue'

# Setup MongoDB client
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[MONGO_DB]
collection = db[MONGO_COLLECTION]

# Flask app setup
app = Flask(__name__)

@app.route('/status_count', methods=['GET'])
def status_count():
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    
    if not start_time or not end_time:
        return jsonify({"error": "Please provide both start_time and end_time in UNIX timestamp format"}), 400
    
    try:
        start_time = float(start_time)
        end_time = float(end_time)
    except ValueError:
        return jsonify({"error": "Invalid timestamp format"}), 400

    pipeline = [
        {
            "$match": {
                "timestamp": {"$gte": start_time, "$lte": end_time}
            }
        },
        {
            "$group": {
                "_id": "$status",
                "count": {"$sum": 1}
            }
        }
    ]

    result = collection.aggregate(pipeline)
    status_counts = {str(item['_id']): item['count'] for item in result}

    return jsonify(status_counts)

# Function to process messages from RabbitMQ
def callback(ch, method, properties, body):
    message = json.loads(body)
    collection.insert_one(message)
    print(f"Received: {message}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Setup RabbitMQ connection and consume messages
def start_rabbitmq_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
    channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback)
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()  

def signal_handler(sig, frame):
    print('Shutting down gracefully...')
    os._exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    rmq_thread = Thread(target=start_rabbitmq_consumer)
    rmq_thread.start()
    
    try:
        app.run(host='127.0.0.1', port=3004)
    finally:
        os._exit(0)
