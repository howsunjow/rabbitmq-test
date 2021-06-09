import pika, click

@click.command()
@click.option('--host', default='localhost', help='Host to send to.')
@click.option('--port', default=5672)
@click.option('--queue', default='test-queue', help='Queue from which to receive messages.')
@click.option('--user', default='guest', help='User name.')
@click.option('--password', default='guest', help='User password.')
def rabbit_mq_receiver(host, port, user, password, queue):
    def message_handler(ch, method, properties, body):
        print(f'[{host}:{port}]: {body}')
    print('Starting receiver')
    credentials = pika.PlainCredentials(user, password)
    parameters = pika.ConnectionParameters(host, port, '/',credentials)
    try:
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
    except Exception as e:
        print(f'Unable to open connection to {host}:{port}')
        print(f'Type "{type(e)}" exception received')
        return
    print(f'Connection to {host} established')
    try:	           
        channel.basic_consume(queue=queue, on_message_callback=message_handler, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()        
    except pika.exceptions.UnroutableError:
        print(f'Channel Error')
        print(f'Type "{type(e)}" exception received')

if __name__ == '__main__':
    rabbit_mq_receiver()
