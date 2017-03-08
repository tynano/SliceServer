var app          = require('express')();
var express      = require('express');
var fs           = require('fs');
var bodyParser   = require('body-parser')
var zerorpc      = require('zerorpc');
var debug        = require('debug')('sliceserver');
var dotenv       = require('dotenv');

dotenv.load({ path: '.env.example' });

app.use('/res', express.static('res'));

var httpsrvr  = require('http').Server(app);

httpsrvr.listen(8086);
//console.log("started sliceserver");

// python/io_rpc.py
var io_client = new zerorpc.Client({'heartbeatInterval' : 30 * 1000});
io_client.connect("tcp://127.0.0.1:5240");

app.get('/', function (req, res, next) {
    //res.send("yo!");    
    fs.readFile('html/index.html', function (err, data) {
          if (err){
            debug(err);
            res.send("error retrieving data");
          }else{
            res.send(data.toString());
          }
        });
});

app.get('/sp500/nodes', function (req, res, next) {
    io_client.invoke('nodes', function(error, result, more){
        if(error == undefined){
            res.send(result);
        }else{
            res.send('{"error": "problem retrieving node data"}');
        }
    });
});

app.get('/sp500/links', function (req, res, next) {
    io_client.invoke('links', function(error, result, more){
        if(error == undefined){
            res.send(result);
        }else{
            res.send('{"error": "problem retrieving link data"}');
        }
    });
});

app.get('/sp500/embedding', function (req, res, next) {
    io_client.invoke('embedding', function(error, result, more){
        if(error == undefined){
            res.send(result);
        }else{
            //console.log(error);
            res.send('{"error": "problem retrieving node embedding data"}');
        }
    });
});

app.get('/sp500/rankNodes', function (req, res, next) {
    var statistic = req.query['statistic'];
    if(statistic == undefined){
        statistic = "closeness_centrality";
    }
    io_client.invoke('rankNodes', statistic, function(error, result, more){
        if(error == undefined){
            res.send(result);
        }else{
            //console.log(error);
            res.send('{"error": "problem retrieving node stat data"}');
        }
    });
});





