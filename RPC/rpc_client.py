import pika
import uuid


# El concepto de RPC en RabbitMQ es facil de entender, un cliente envia un mensaje con request
# a nuestro rpc_server y el rpc_server responde con una respuesta

# En este ejemplo, este archivo se encargara de ser el cliente.
class FibonacciRpcClient(object):
    # El constructor de la clase se esta encargando de configurar pika
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()
        # Cuando el canal del cliente empieza, este declara un callback Que exclusivo y anonimo
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        # Tambien declara que empezara a consumir nuestro queue declarado y pasamos la funcion on_response
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)
    # Esta funcion esta esperando si la correlation_id de las responses corresponden con la request
    # Si son iguales, guarda la respuesta en this.response  y termina el consuming loop
    # este termino del loop se nota cuando ejecutamos el ejemplo, cuando el cliente recibe la response
    # el script de python termina su funcionamiento.
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        # valor unico con uuid para nuestra correlation_id
        self.corr_id = str(uuid.uuid4())
        # Reply_to puede vincular el queue a ejecutar. Correlation id sirve para poder identificar que la respuesta
        # del server pertenece a la request enviada por nuestro cliente. Esta buena practica de correlation id nos
        # sirve para que en caso de morir rabbit, en su reinicio pueda procesar la request que necesitamos nuevamente

        # Enviamos la request a nuestro canal rpc_queue
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)



fibonacci_rpc = FibonacciRpcClient()

print(" [x] Quiero fib(30)")
# call enviara una Request RPC y quedara bloqueada hasta que reciba una respuesta
response = fibonacci_rpc.call(30)

print(" [.] Obtuve %r" % response)
