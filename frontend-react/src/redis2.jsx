
    
var redis = require('redis');
var host= "redis://192.168.1.22:6379/"
var sub = redis.createClient(host);
var sub2 = redis.createClient(host);
sub.select(3);
sub2.select(3);

var queries2=redis.createClient(host);
var express = require('express');
var bodyParser = require('body-parser');
var _ = require('lodash');
// Create server


// Create server
var server = express();
server.use(bodyParser.json());

// Middleware
server.use(function (req, res, next) {
  // allow origin for demo purposes
  res.setHeader('Access-Control-Allow-Origin', 'http://192.168.1.22:8000');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, DELETE');
  res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type');
  next();
});

    
  
function initData(item, res) {
    var queries= redis.createClient(host);
    var queries2= redis.createClient(host);
    queries.select(4);
    queries2.select(4);
    queries.keys(item+'*', function (err, keys) {
        keys.forEach(function (key, pos) {
            obj = queries2.HGETALL(key,function (err, obj) {
                resizeBy.send(obj);
                }

            )

        }
    )
})}



var app = express();
app.use(bodyParser.json());

app.get('/agents', function (req, res) {
    // Get tweets
 
    
    
    
    
    
    
    initData('agents', res);

    /*    queries.lrange('stream:tweets', 0, -1, function (err, tweets) {
         if (err) {
           console.log(err);
         } else {
           // Get tweets
           var tweet_list = [];
           tweets.forEach(function (tweet, i) {
             tweet_list.push(JSON.parse(tweet));
           });
           // Render page
           var markup = React.renderToString(Tweets({ data: tweet_list.reverse() }));
           res.render('index', {
             markup: markup,
             state: JSON.stringify(tweet_list)
           });
         }
       }); */
     });
   
   
   //First call to app to init agents
   
   
   //setup socket
   port =3002
   var io = require('socket.io')({
   }).listen(app.listen(port));
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
   
   
   