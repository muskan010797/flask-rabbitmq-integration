import schedule
import time
from datetime import datetime
from rabbitmq import RabbitMQ
from db import MongoDB
from models import RandomNumber
import random

mongo = MongoDB('mongodb://localhost:27017/', 'mydatabase')
collection = mongo.get_collection('random_numbers')

rabbitmq = RabbitMQ()

def publish_random_number():
    random_number = random.randint(1, 6)
    
    random_number_doc = RandomNumber(number=random_number, created_at=datetime.utcnow())
    collection.insert_one(random_number_doc.to_dict())
    
    rabbitmq.publish_message(random_number)

def process_message(ch, method, properties, body):
    print(f" [x] Received {body}")

schedule.every().second.do(publish_random_number)

rabbitmq.consume_messages(process_message)

while True:
    schedule.run_pending()
    time.sleep(1)
