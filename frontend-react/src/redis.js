//redis sub channels :
var redis = require('redis');
const redis_host = "redis"

var host = "redis://" + redis_host + ":6379";

var sub = redis.createClient(host);
var sub2 = redis.createClient(host);
sub.select(4);
sub2.select(4);

//SOCKETIO
var starttime = Date.now();
var io = require('socket.io')(3001);

io.on('connection', function (socket) {
  io.emit('this', { will: 'be received by everyone' });

  socket.on('message', function (from, msg) {
    console.log('I received a private message by ', from, ' saying ', msg);
  });

  sub.subscribe("call");
  sub2.subscribe("agent");
  // Handle receiving messages
  var timeInMs = Date.now();
  var olddata = ""
  var pl = ""

  var callback = function (channel, data) {
    if (data != olddata) {
      olddata = data;
      if (Date.now() - timeInMs >10 ){
      timeInMs = Date.now();
      pl = data
      io.emit('message', { pl })
      //console.log(pl);
    }}
  };

  sub.on('message', callback);
  sub2.on('message', callback);

  socket.on('disconnect', function () {
    io.emit('user disconnected');
  });
});

