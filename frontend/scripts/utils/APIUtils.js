/* jshint devel:true */

var AppDispatcher = require('../dispatcher/AppDispatcher');
var APIReceiveActions = require('../actions/APIReceiveActions');
var DummyFilters = require('../components/DummyFilterData');
var DummyTasks = require('../components/DummyTaskData');


var APIUtils = {

  getTasksFromServer: function() {
    var rawTasks = JSON.parse(DummyTasks);
    APIReceiveActions.receiveTasks(rawTasks);
  },

  getFiltersFromServer: function() {
    var rawFilters = JSON.parse(DummyFilters);
    APIReceiveActions.receiveFilters(rawFilters);
  },

};


module.exports = APIUtils;
