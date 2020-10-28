var express = require('express');
var app = new express();
var http = require('http').createServer(app);
var io = require('socket.io')(http);
var port = process.env.PORT || 3000;
app.use(express.static('public'))

app.use(express.static(__dirname + '/publico'));
http.listen(port, function(){
console.log('Servidor escuchando en: %s', port)
});
app.get('/', function(req, res){
res.redirect('./index.html');
});
io.on('connection', function(socket){
socket.on('stream',function(image){
socket.broadcast.emit('stream', image);
});
});
