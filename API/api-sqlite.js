var sqlite3 = require('sqlite3').verbose();
var db = new sqlite3.Database('ModDB.db');

db.serialize(function() {
    db.run("CREATE TABLE IF NOT EXISTS mods (mod_name TEXT, username TEXT, json TEXT, version TEXT, mod_id TEXT)");
});

var express = require('express');
var app = express();

app.use(express.json());

/**
 * @api {get} /mods/ Get all mods
 * @apiName GetMods
 * @apiGroup Mods
 * @apiVersion 1.0.0
 * 
 * @apiSuccess {Object[]} mods A List of Objects containing metadata for all mods.
 * @apiSuccess {String} mod.mod_name The name of the mod.
 * @apiSuccess {String} mod.username The username of the user who created the mod.
 * @apiSuccess {String} mod.json The encoded JSON data of the mod.
 * @apiSuccess {String} mod.version The version of the mod.
 * @apiSuccess {String} mod.mod_id The unique identiifer of the mod.
 * @apiError (Error 500) {String} error There was an internal server error.
 */
app.get('/mods', (req, res) => {
    db.all("SELECT * FROM mods", (err, rows) => {
        if(err) {
            console.error(err.message);
            res.status(500).json({error:'Internal server error'});            
        } else {
            res.status(200).json({mods: rows});
        }
    });
});

/**
 * @api {get} /mods/:mod_id Get a specific mod by its Identifier
 * @apiName GetMod
 * @apiGroup Mods
 * @apiVersion 1.0.0
 * 
 * @apiParam {String} mod_id The unique identiifer of the mod.
 * 
 * @apiSuccess {Object} mod An Object containing the mod metadata
 * @apiSuccess {String} mod.mod_name The name of the mod.
 * @apiSuccess {String} mod.username The username of the user who created the mod.
 * @apiSuccess {String} mod.json The encoded JSON data of the mod.
 * @apiSuccess {String} mod.version The version of the mod.
 * @apiSuccess {String} mod.mod_id The unique identiifer of the mod.
 * @apiError (Error 404) {String} error The mod did not exist in the database.
 * @apiError (Error 500) {String} error There was an internal server error.
 */
app.get('/mods/:mod_id', (req, res) => {
    const mod_id = req.params.mod_id;

    db.get('SELECT * FROM mods WHERE mod_id = ? LIMIT 1', [mod_id], (err, row) => {
        if(err) {
            console.error(err.message);
            res.status(500).json({error:'Internal server error'});
        } else if (!row) {
            res.status(404).json({error:'Mod not found'});
        } else {
            res.status(200).json({mod: row});
        }
    });
});

/**
 * @api {post} /mods Adds a new mod
 * @apiName AddMod
 * @apiGroup Mods
 * @apiVersion 1.0.0
 * 
 * @apiBody {String} mod_name The name of the mod.
 * @apiBody {String} username The username of the user who created the mod.
 * @apiBody {String} json The encoded JSON data of the mod.
 * @apiBody {String} version The version of the mod.
 * @apiBody {String} mod_id The unique identiifer of the mod.
 * 
 * @apiSuccess {String} message Validation successful. The Mod has been added to the database.
 * @apiError (Error 400) {String} error The JSON body of the request could not be serialized.
 * @apiError (Error 500) {String} error There was an internal server error.
 */
app.post('/mods', (req, res) => {
    const { mod_name, username, json, version, mod_id } = req.body;
    
    if(mod_name && username && json && version && mod_id &&
        typeof mod_name === 'string' &&
        typeof username === 'string' &&
        typeof json === 'string' &&
        typeof version === 'string' &&
        typeof mod_id === 'string') {
            db.run("INSERT INTO mods (mod_name, username, json, version, mod_id) VALUES (?, ?, ?, ?, ?)", 
            [mod_name, username, json, version, mod_id],
            (err) => {
                if(err) {
                    console.error(err.message);
                    res.status(500).json({error:'Internal server error'});
                } else {
                    res.status(200).json({message: 'Mod Successfully Uploaded'});
                }
            });
    } else {
        res.status(400).json({error:'Invalid JSON body'});
    }
});

/**
 * @api {put} /mods/:mod_id Update a mod by its given Identifier
 * @apiName UpdateMod
 * @apiGroup Mods
 * @apiVersion 1.0.0
 * 
 * @apiParam {String} mod_id The unique identiifer of the mod.
 * 
 * @apiBody {String} mod_name The name of the mod.
 * @apiBody {String} username The username of the user who created the mod.
 * @apiBody {String} json The encoded JSON data of the mod.
 * @apiBody {String} version The version of the mod.
 * 
 * @apiSuccess {String} message The mod updated successfully.
 * @apiError (Error 400) {String} error The JSON body of the request could not be serialized.
 * @apiError (Error 500) {String} error There was an internal server error.
 */
app.put('/mods/:mod_id', (req, res) => {
    const mod_id = req.params.mod_id;
    const { mod_name, username, json, version } = req.body;

    if(mod_name && username && json && version && mod_id &&
        typeof mod_name === 'string' &&
        typeof username === 'string' &&
        typeof json === 'string' &&
        typeof version === 'string' &&
        typeof mod_id === 'string') {
            db.run(
                "UPDATE mods SET mod_name = ?, json = ?, version = ? WHERE mod_id = ?",
                [mod_name, json, version, mod_id],
                (err) => {
                    if(err) {
                        console.error(err.message);
                        res.status(500).json({error:"Internal server error"});
                    } else {
                        res.status(200).json({message: 'Mod Successfully Updated'});
                    }
                }
            );
    } else {
        res.status(400).json({error:'Invalid JSON body'});
    }
});

/**
 * @api {delete} /mods/:mod_id Delete a specific mod using its Identifier
 * @apiName DeleteMod
 * @apiGroup Mods
 * @apiVersion 1.0.0
 * 
 * @apiParam {String} mod_id The unique identiifer of the mod.
 * 
 * @apiSuccess {String} message MOd deleted successfully.
 * @apiError (Error 500) {String} error There was an internal server error.
 */
app.delete('/mods/:mod_id', (req, res) => {
    const mod_id = req.params.mod_id;

    db.get('SELECT * FROM mods WHERE mod_id = ? LIMIT 1', [mod_id], (err, row) => {
        if(err) {
            console.error(err.message);
            res.status(500).json({error:'Internal server error'});
        } else if (!row) {
            res.status(404).json({error:'Mod not found'});
        } else {
            db.run("DELETE FROM mods WHERE mod_id = ?", [mod_id], (err) => {
                if(err) {
                    console.error(err.message);
                    res.status(500).json({error:"Internal server error"});
                } else {
                    res.status(200).json({message: 'Mod Successfully Deleted'});
                }
            });
        }
    });

    
});

app.listen(4001, () => {
    console.log('Server has started on port 4001');
});

console.log("Up and running...");