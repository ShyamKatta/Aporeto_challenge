// var https = require("https");
var url = require('url');
var https = require('https');
var express = require('express');
var path = require('path');

var app = express();

//API responds to requested username when path is HOST/MyGitContributionsAPI?uname={username}, same url can beused as an API too.
app.get('/MyGitContributionsAPI', function (req, res) {
    var url_parts = url.parse(req.url, true);
    // populate data for git hub api
    const {spawn} = require('child_process');
    const pyProg= spawn('python',['./scripts/MyContributions.py',req.query.uname])    // spawn process with single argument
    let py_data;
    let collect;
    pyProg.stdout.on('data', function(data){
        collect = data.toString(); 
    })
    pyProg.stdout.on('end', function(){
        py_data=JSON.parse(collect);
        res.send(py_data)
    })
});

//display html file if a StarIndex path is requested
app.get('/MyContributions', function (req, res) {
    res.sendFile(path.join(__dirname, 'GIT_contributions.html'));
});

// render the HTML file for default route
app.get('/', function (req, res) {
    res.sendFile(path.join(__dirname, 'GIT_contributions.html'));
});

// below code is modified for deployement, 0.0.0.0 is added to make this accept public requests, Port number doesnt matter, no need to include in URL
var port = process.env.PORT || 3000;
app.listen(port, "0.0.0.0", function () {
    console.log('listening on', port);
});
