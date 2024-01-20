var sqlite3 = require('sqlite3').verbose();
var db = new sqlite3.Database('ModDB');

db.serialize(function() {
    db.run("CREATE TABLE IF NOT EXISTS mods (mod_name TEXT, username TEXT, json TEXT, version TEXT, mod_id TEXT)");
});

var express = require('express');
var app = express();

app.use(express.json());

app.get('/mods', function(req, res) {
    db.all("SELECT * FROM mods", function(err, rows){
        res.jsonp(rows);
    })
});

app.post('/mods', (req, res) => {
    const { mod_name, username, json, version, mod_id } = req.body;
    db.run("INSERT INTO mods (mod_name, username, json, version, mod_id) VALUES (?, ?, ?, ?, ?)", mod_name, username, json, version, mod_id);
    res.status(200).json({message: 'Successfully Validated'});
});

app.get('/mods/:mod_id', (req, res) => {
    const mod_id = req.params.mod_id;

    db.get('SELECT * FROM mods WHERE mod_id = ? LIMIT 1', [mod_id], (err, row) => {
        console.log(row);
        res.status(200).json({mod: row});
    });
});

app.listen(4001, () => {
    console.log('Server has starteed on port 4001');
});

console.log("Up and running...");