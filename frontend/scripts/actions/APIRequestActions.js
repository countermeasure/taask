/* jshint devel:true */

var APIUtils = require('../utils/APIUtils');


var APIRequestActions = {

  initialiseApp: function() {
    this.requestFilters();
    this.requestTasks();
  },

  requestFilters: function() {
    console.log('<-- API REQUEST: Filters data');
    APIUtils.getFiltersFromServer();
  },

  requestTasks: function() {
    console.log('<-- API REQUEST: Tasks data');
    APIUtils.getTasksFromServer();
  },
  
};


module.exports = APIRequestActions;
