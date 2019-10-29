const q = "para-borrar";
const printing = x => {console.log(x)};
const conn = require('amqplib').connect({
    protocol: 'amqp',
    hostname: '35.238.179.150',
    port: 5672,
    username: 'carlos@woorkit.cl',
    password: 'LD8K¿w8?1un?',
});
conn.then(conn=> {
    let ok = conn.createChannel().then(ch => {
        return ch.deleteQueue(q);
    });
    return ok.then(conn.close.bind(conn));
}).then(null,console.warn);


