

var request = require('supertest');
describe('Simple express server tests', function () {
  var server;
  // restart the server before each test 
  beforeEach(function () {
	//delete require.cache[require.resolve('./node_server')];
    server = require('./node_server.js');
  });
  // responds to default route
  it('responds to /', function testSlash(done) {
  request('http://localhost:3000')
    .get('/')
    .expect(200, done);
  });
  // if the invalid path is mentioned, should return 404
  it('404 everything else', function testPath(done) {
    request('http://localhost:3000')
      .get('/lkjhgdgdf')
      .expect(404, done);
  });
});