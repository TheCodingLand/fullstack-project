//REDIS QUEUES : 
var redis = require('redis');
var host= "redis://192.168.1.22:6379/"
var sub = redis.createClient(host);
var sub2 = redis.createClient(host);
sub.select(3);
sub2.select(3);
var http = require('http').Server(app)

//basic APP SERVER
port =3001
var express = require('express');
var server = express();
var bodyParser = require('body-parser');
server.use(bodyParser.json());


server.use(function (req, res, next) {
    // allow origin for demo purposes
    res.setHeader('Access-Control-Allow-Origin', 'http://localhost:8080');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, DELETE');
    res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type');
    next();
    });


server.get('/agents', function (req, res) {res.send({ "ok" : 'ok' }); })

var io = require('socket.io')({}).listen(server.listen(port));

console.log("Listening on port " + port);


// Handle connections
io.sockets.on('connection', function (socket) {
  // Subscribe to the Redis channels
  sub.subscribe("call");
  sub2.subscribe("agent");
  // Handle receiving messages
  var callback = function (channel, data) {
    data = updateClient(channel,data);
    socket.emit('message', data);
  };

  sub.on('message', callback);
  sub2.on('message', callback);
  // Handle disconnect
  socket.on('disconnect', function () {
    subscribe.removeListener('message', callback);
  });
}); 