import pika, click

@click.command()
@click.option('--host', default='localhost', help='Host to send to.')
@click.option('--port', default=5672)
@click.option('--queue', default='test-queue', help='Queue to which to send messages.')
@click.option('--user', default='guest', help='User name.')
@click.option('--password', default='guest', help='User password.')
@click.option('--message', help='Message to place on the queue.')
def rabbit_mq_sender(host, port, user, password, queue, message):
    credentials = pika.PlainCredentials(user, password)
    parameters = pika.ConnectionParameters(host, port, '/',credentials)
    try:
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
    except Exception as e:
        print(f'Unable to open connection to {host}:{port}')
        print(type(e))
        return

    try:	
        channel.queue_declare(queue=queue)
        channel.confirm_delivery()        
        channel.basic_publish(exchange='', routing_key=queue, body=message,
                              properties=pika.BasicProperties(content_type='text/plain',
                              delivery_mode=1), mandatory=True)
        print(f'Message was published to queue "{sendqueue}" at {host}:{port}')
    except pika.exceptions.UnroutableError:
        print(f'Message could not be delivered to queue "{sendqueue}" at {host}:{port}')

if __name__ == '__main__':
    rabbit_mq_sender()
