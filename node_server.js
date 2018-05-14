// var https = require("https");
var url = require('url');
var https = require('https');
var express = require('express');
var path = require('path');

var app = express();

//API responds to requested username when path is HOST/MyGitContributionsAPI?uname={username}, same url can beused as an API too.
app.get('/MyGitContributionsAPI', function (req, res) {


    var url_parts = url.parse(req.url, true);
    console.log("wokring");

    var request = require('request');
    let access_code =  req.query.access_code;//url.parse(req.url, true);
    // Configure the request
    var options = {
        url: "https://github.com/login/oauth/access_token?client_id=d3653ed7b5aa1c180cff&redirect_uri=http://git-contribution.us-east-2"+
        ".elasticbeanstalk.com/MyContributions&client_secret=b502132e1797209549d277bce3f0bdf4a7b64a5e&code="+access_code,
        method: 'POST'
    }
    request(options, function (error, response, body) {
        //console.log(error+" "+response+"   ---->");
        if (!error && response.statusCode == 200) {
            //console.log(response);
            //console.log(body);
            /* If error access_token will have - "[ 'bad_verification_code' ]" */
            let access_token = response.body.split('&').slice(0,1).toString().split('=').slice(1);
            console.log(access_token);
            // access_token might generate - bad_verification_code, need to handle
            const {spawn} = require('child_process');
            const pyProg= spawn('python',['./scripts/MyContributions.py',req.query.uname, access_token])    // spawn process with single argument
            //const pyProg= spawn('python',['./scripts/sample_test.py'])
            let py_data;
            let collect="";
            pyProg.stdout.on('data', function(data){
                collect += data.toString();
            })
            pyProg.stdout.on('end', function(){
                console.log(collect+" is collect");
                if(collect.trim()=="[]" || collect.trim()=="" || access_token=="[ 'bad_verification_code' ]"){
                    console.log("trying to access public repos 1");
                    const {spawn1} = require('child_process');
                    const pyProg1= spawn('python',['./scripts/MyContributions_public.py',req.query.uname])
                    collect="";
                    pyProg1.stdout.on('data', function(data){
                        collect += data.toString();
                    })
                    pyProg1.stdout.on('end', function(){
                        if(collect.trim()=="[]" || collect.trim()==""){
                            console.log("failed to access public repos");
                            console.log("No contribution data for user "+req.query.uname);
                            res.status(404).send("No contributions present for "+req.query.uname);
                        }
                        else{
                        py_data=JSON.parse(collect);
                        console.log("response sent about user in public repos - "+req.query.uname);
                        res.send(py_data);
                        }
                    })
                }
                else{
                py_data=JSON.parse(collect);
                console.log("response sent about user for public/private repos - "+req.query.uname);
                res.send(py_data);
                }
            })
            //res.send(response.body);
        }
    })
});

//display html file if a StarIndex path is requested
app.get('/MyContributions', function (req, res) {
    res.sendFile(path.join(__dirname, 'GIT_contributions.html'));
});

app.get('/oauth/success',function(req,res){
    var url_parts = url.parse(req.url, true);
    console.log(url_parts);
    console.log("auth activated callback");
    res.send(url_parts);
    //req.query.uname
});
app.get('/test', function(req,res){
    //url = "https://github.com/login"
    var request = require('request');
    let access_code =  req.query.access_code;//url.parse(req.url, true);
    // Configure the request
    var options = {
        url: "https://github.com/login/oauth/access_token?client_id=d3653ed7b5aa1c180cff&redirect_uri=http://git-contribution.us-east-2"+
        ".elasticbeanstalk.com/oauth/success&client_secret=b502132e1797209549d277bce3f0bdf4a7b64a5e&code="+access_code,
        method: 'POST'
        //headers: headers
    }
    // Start the request
    request(options, function (error, response, body) {
        if (!error && response.statusCode == 200) {
            console.log(response);
            console.log(body);
            let access_token = response.body.split('&').slice(0,1).toString().split('=').slice(1);
            res.send(access_token);
        }
    })
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
