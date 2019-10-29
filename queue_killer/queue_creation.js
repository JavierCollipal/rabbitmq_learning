const q = "para-borrar";
const conn = require('amqplib').connect({
    protocol: 'amqp',
    hostname: '35.238.179.150',
    port: 5672,
    username: 'carlos@woorkit.cl',
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