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
    await t.expect(response.data.message).eql('Validation successful. Data added to the database');
});