const q = "para-borrar";
const conn = require('amqplib').connect({
    protocol: 'amqp',
    hostname: '0.0.0.0',
    port: 5672,
    username: 'admin@admin',
    password: 'LD8K¿w8?1un?',
});
const channel = conn.then(x=> {
    return x.createChannel();
});
channel.then(x => {
    x.assertQueue(q).then(y => {
        console.log(y)
    })
});
