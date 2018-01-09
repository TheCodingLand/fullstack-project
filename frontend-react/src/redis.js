
//redis sub channels :
var redis = require('redis');


const redis_host = "148.110.107.15" 


var host= "redis://"+redis_host+":6379";

var sub = redis.createClient(host);
var sub2 = redis.createClient(host);
sub.select(4);
sub2.select(4);

//var queries2=redis.createClient(host);
//var bodyParser = require('body-parser');


//SOCKETIO
var starttime = Date.now();
var io = require('socket.io')(3002);

io.on('connection', function (socket) {
  io.emit('this', { will: 'be received by everyone'});

  socket.on('message', function (from, msg) {
    console.log('I received a private message by ', from, ' saying ', msg);
  });

sub.subscribe("call");
sub2.subscribe("agent");
 // Handle receiving messages
var timeInMs = Date.now();
var callback = function (channel, data) {


if (Date.now() - timeInMs >100 ){

timeInMs = Date.now();

data = "update recieved on " + channel + " " + data
io.emit('message', {data})
console.log(data);

}};


sub.on('message', callback);
sub2.on('message', callback);



  socket.on('disconnect', function () {
    io.emit('user disconnected');
  });
});


// Create server
//var server = express();
//server.use(bodyParser.json());

// Middleware
//server.use(function (req, res, next) {
  // allow origin for demo purposes
//  res.setHeader('Access-Control-Allow-Origin', 'http://localhost:8080');
//  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, DELETE');
//  res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type');
//  next();
//});




/* 
function initData(item, res) {
    var queries= redis.createClient(host);
    var queries2= redis.createClient(host);
    queries.select(4);
    queries2.select(4);
    queries.keys(item+'*', function (err, keys) {
        keys.forEach(function (key, pos) {
            obj = queries2.HGETALL(key,function (err, obj) {
                res.send(obj);
                }
                
            )
           
        }
    )
})} */

// var io = require('socket.io')(80);





// server.get('/agents', function (req, res) {
    
//     var queries= redis.createClient(host);
//     queries.select(4);
//     // Get agents
//     queries.lrange('agent', 0, -1, function (err, agents) {
//         if (err) {
//           console.log(err);
//         } else {
//           // Get agent
//           var agent_list = [];
//           var tod = [];
//           agents.forEach(function (agent, i) {
//             tod.push(JSON.parse(agent));
//             console.log(agent)
            
//           });
//           res.send({ "todos" : tod });      
//         }}
//     )
   // {"todos":[{"text":"test","timestamp":"31/12/2017","id":11}]}
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
//} ); 


//First call to app to init agents


//setup socket




port =3001
// var io = require('socket.io')({}).listen(server.listen(port));
// console.log("Listening on port " + port);
// // Handle connections
// io.sockets.on('connection', function (socket) {
//   // Subscribe to the Redis channels
//   sub.subscribe("call");
//   sub2.subscribe("agent");
//   // Handle receiving messages
//   var callback = function (channel, data) {
//     data = updateClient(channel,data);
//     socket.emit('message', data);
//   };

//   sub.on('message', callback);
//   sub2.on('message', callback);
//   // Handle disconnect
//   socket.on('disconnect', function () {
//     subscribe.removeListener('message', callback);
//   });
// }); 


 