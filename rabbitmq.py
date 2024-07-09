import pika

class RabbitMQ:
    def __init__(self, host='localhost', queue_name='my_queue'):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()
        self.queue_name = queue_name
        self.channel.queue_declare(queue=self.queue_name)

    def publish_message(self, message):
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_name,
                                   body=str(message))
        
    def consume_messages(self, callback):
        self.channel.basic_consume(queue=self.queue_name,
                                   on_message_callback=callback,
                                   auto_ack=True)
        self.channel.start_consuming()

    def close_connection(self):
        self.connection.close()
