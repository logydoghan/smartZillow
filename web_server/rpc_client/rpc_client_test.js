var client = require('./rpc_client');

// invoke "add"
client.add(1, 2, function(response) {
    console.log("1 + 2 = " + response);
});

// invoke "searchArea"
client.searchArea('94080', function(response) {
    console.log('94080: ' + response);
});

// invoke "searchByAddress"
client.searchByAddress('101 Mclellan', '94080', function(response) {
	console.log(response);
});

// invoke "searchAreaByZip"
client.searchAreaByZip('94080', function(response) {
  	console.log(response);
});

// invoke "searchAreaByCityState"
client.searchAreaByCityState('San Jose', 'CA', function(response) {
  	console.log(response);
});

// invoke "getDetailsByZpid"
client.getDetailsByZpid('2096899447', function(response) {
    console.log(response);
});