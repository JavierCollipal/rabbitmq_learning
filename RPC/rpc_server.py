import pika
# Este archivo es el rpc_server, el cual nos entregara n numeros de la secuencia fibonnaci

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = connection.channel()
# declaramos  declarando un queue
channel.queue_declare(queue='rpc_queue')


# Funcion fibonnaci
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


# callback para manejar la request del cliente
def on_request(ch, method, props, body):
    # Manejo de la propiedad body y la respuesta a entregar
    n = int(body)
    print(" [.] fib(%s)" % n)
    response = fib(n)
    # Configuracion de la response
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
# Configuracion del canal.
# Cuando el cliente envie una request con publish, el rpc_server respondera con un callback.
# Este callback tambien continua con la respuesta que le tenemos que dar a nuestro cliente
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(" [x] Esperando requests RPC ")
channel.start_consuming()
