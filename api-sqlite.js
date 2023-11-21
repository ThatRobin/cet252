var sqlite3 = require('sqlite3').verbose();
var db = new sqlite3.Database('weblinksDB');

db.serialize(function() {
    db.run("CREATE TABLE IF NOT EXISTS weblinks (url TEXT, rating INTEGER)");
    db.run("DELETE FROM weblinks");
    db.run("INSERT INTO weblinks (url, rating) VALUES (?, ?)", "https://www.bbc.co.uk", 6);
    db.run("INSERT INTO weblinks (url, rating) VALUES (?, ?)", "http://bbbc.com", 10);
});

var express = require('express');
var app = express();

app.get('/weblinks', function(req, res) {
    db.all("SELECT * FROM weblinks", function(err, rows){
        res.jsonp(rows);
    })
});

app.listen(4001);

console.log("Up and running...");