import pika
import json

# Este archivo es el consumidor.
# El consumidor se encarga de consumir el canal designado.
# Conexion a nuestro rabbitqm con pika
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672))
channel = connection.channel()

# Declaracion del canal que consumiremos
# Podemos declarar multiples veces un mismo canal con queue_declare, pero una sola vez quedara
# registrado.
channel.queue_declare(queue='hola')


# Para recibir un mensaje, necesitamos adjuntar una funcion callback a nuestro canal
def callback(ch, method, properties, body):
    print(body)
    print(json.loads(body))


# Con basic_consume le decimos a rabbit que este callback recibira mensajes del canal
# hola.
channel.basic_consume(queue='hola', on_message_callback=callback, auto_ack=True)
print('[*] Esperando por mensajes.')
# Con start_consuming empezamos un loop que espera la data y responde con un callback
# cuando sea necesario.
channel.start_consuming()
