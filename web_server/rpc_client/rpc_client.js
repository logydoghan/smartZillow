var jayson = require('jayson');

// create a client connnected to backend server
var client = jayson.client.http({
  port: 4040,
  hostname: 'localhost'
});

// Test Rpc method
function add(a, b, callback) {
    client.request('add', [a, b], function(err, error, response) {
        if (err) throw err;
        console.log(response);
        callback(response);
    });
}

// Search property using address and city/state or zip code.
function searchByAddress(address, citystatezip, callback) {
    client.request('searchByAddress', [address, citystatezip], function(err, error, response) {
        if (err) throw err;
        console.log(response);
        callback(response);
    });
}

// Search properties using zip code.
function searchAreaByZip(zipcode, callback) {
    client.request('searchAreaByZip', [zipcode], function(err, error, response) {
        if (err) throw err;
        console.log(response);
        callback(response);
    });
}

// Search properties using city and state.
function searchAreaByCityState(city, state, callback) {
    client.request('searchAreaByCityState', [city, state], function(err, error, response) {
        if (err) throw err;
        console.log(response);
        callback(response);
    });
}

// Search properties.
function searchArea(text, callback) {
    client.request('searchArea', [text], function(err, error, response) {
        if (err) throw err;
        console.log(response);
        callback(response);
    });
}

// Get property details by Zillow Property ID (zpid).
function getDetailsByZpid(zpid, callback) {
    client.request('getDetailsByZpid', [zpid, true], function(err, error, response) {
        if (err) throw err;
        console.log(response);
        callback(response);
    });
}

module.exports = {
    add : add,
    searchByAddress : searchByAddress,
    searchAreaByZip : searchAreaByZip,
    searchAreaByCityState : searchAreaByCityState,
    searchArea : searchArea,
    getDetailsByZpid : getDetailsByZpid
};
