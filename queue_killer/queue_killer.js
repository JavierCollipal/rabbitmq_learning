const q = "para-borrar";
const printing = x => {console.log(x)};

const conn = require('amqplib').connect({
    protocol: 'amqp',
    hostname: '0.0.0.0',
    port: 5672,
    username: 'admin@admin',
    password: 'LD8K¿w8?1un?',
});
conn.then(conn=> {
    let ok = conn.createChannel().then(ch => {
        return ch.deleteQueue(q);
    });
    return ok.then(conn.close.bind(conn));
}).then(null,console.warn);


