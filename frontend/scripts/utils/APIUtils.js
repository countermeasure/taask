/* jshint devel:true */

var AppDispatcher = require('../dispatcher/AppDispatcher');
var APIReceiveActions = require('../actions/APIReceiveActions');
var DummyFilters = require('../components/DummyFilterData');
var request = require('superagent');

var BASE_URL = 'http://localhost:8001/';
var TIMEOUT = 10000;


function get(url) {
  return request
    .get(BASE_URL + url)
    .timeout(TIMEOUT)
    .set('Accept', 'application/json');
}


var APIUtils = {

  getTasksFromServer: function() {
    get('tasks').end(
      function(error, response) {
        rawTasks = JSON.parse(response.text);
        APIReceiveActions.receiveTasks(rawTasks);
      }
    );
  },

  getFiltersFromServer: function() {
    var rawFilters = JSON.parse(DummyFilters);
    APIReceiveActions.receiveFilters(rawFilters);
  },

};


module.exports = APIUtils;
