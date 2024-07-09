from flask import Flask, jsonify, request
from datetime import datetime
from db import MongoDB
from models import RandomNumber
from rabbitmq import RabbitMQ
import random

app = Flask(__name__)

mongo = MongoDB('mongodb://localhost:27017/', 'mydatabase')
collection = mongo.get_collection('random_numbers')

rabbitmq = RabbitMQ()

@app.route('/publish_random_number', methods=['POST'])
def publish_random_number():
    random_number = random.randint(1, 6)
    
    random_number_doc = RandomNumber(number=random_number, created_at=datetime.utcnow())
    collection.insert_one(random_number_doc.to_dict())
    
    rabbitmq.publish_message(random_number)
    
    return jsonify(message=f"Published and saved random number: {random_number}")

if __name__ == '__main__':
    app.run(debug=True)
