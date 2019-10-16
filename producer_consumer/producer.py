import pika
# Concepto base
# RabbitMQ es un message broker, un ejemplo de mensajeria broker seria:
# Necesito enviar una carta a alguien, para enviarla necesito una post office, eventualmente la carta
# llegara al destinatario.
# Yo soy el productor, el destinatario el consumidor y la post office el canal de comunicación.
# RabbitqMQ puede ser estos 3 actores, donde el canal de comunicación es el queue, el destinatario
# es el consumer y yo el producer.

# Este archivo cumplira el rol de producer

# Conexión de pika a nuestro localhost
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672))

channel = connection.channel()
# para enviar un mensaje, primero necesitaremos un canal y lo llamaremos hola
channel.queue_declare(queue='hola')
# El mensaje necesita saber el canal donde sera publicado, la variable exchange='' nos esta permitiendo
# que nuestro mensaje vaya al canal especificado en routing_key
message = "hola mundo"
channel.basic_publish(exchange='', routing_key='hola', body=message)
print(" [x] Envio un hola mundo")
connection.close()
