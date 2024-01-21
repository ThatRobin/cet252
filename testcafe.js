const axios = require('axios');
const { Selector } = require('testcafe');

fixture('Api Testing')
.page('http://localhost:4001');

test('POST /mods - Add a new mod', async (t) => {
    const response = await axios.post('http://localhost:4001/mods', {
        mod_name: 'Test Mod',
        username: 'ThatRobin3001',
        json: '(insert compressed json here)',
        version: '1.0.0',
        mod_id: 'test_mod'
    });

    await t.expect(response.status).eql(200);
    await t.expect(response.data.message).eql('Mod Successfully Uploaded');
});

test('GET /mods - Get all mods', async (t) => {
    const response = await axios.get('http://localhost:4001/mods');

    await t.expect(response.status).eql(200);
    await t.expect(response.data.mods).ok();
});

test('GET /mods/:mod_id - Get a specific mod by mod_id', async (t) => {
    const response = await axios.get('http://localhost:4001/mods/test_mod');

    await t.expect(response.status).eql(200);
    await t.expect(response.data.mod).ok();
});

test('PUT /mods/:mod_id - Update a specific mod by mod_id', async (t) => {
    const response = await axios.put('http://localhost:4001/mods/test_mod', {
        mod_name: 'Test Mod',
        username: 'ThatRobin3001',
        json: '(insert compressed json here)',
        version: '1.1.0'
    });

    await t.expect(response.status).eql(200);
    await t.expect(response.data.message).eql('Mod Successfully Updated');
});

test('DELETE /mods/:mod_id - Delete a specific mod by mod_id', async (t) => {
    const response = await axios.delete('http://localhost:4001/mods/test_mod');

    await t.expect(response.status).eql(200);
    await t.expect(response.data.message).eql('Mod Successfully Deleted');
});