/* jshint devel:true */

var AppDispatcher = require('../dispatcher/AppDispatcher');
var Constants = require('../constants/Constants');

var ActionType = Constants.ActionType;


var APIReceiveActions = {

  receiveFilters: function(rawFilters) {
    console.log('--> API RECEIPT: Filters data');
    AppDispatcher.handleViewAction({
      type: ActionType.RECEIVE_FILTERS,
      rawFilters: rawFilters
    });
  },
  
  receiveTasks: function(rawTasks) {
    console.log('--> API RECEIPT: Tasks data');
    AppDispatcher.handleViewAction({
      type: ActionType.RECEIVE_TASKS,
      rawTasks: rawTasks
    });
  }

};


module.exports = APIReceiveActions;
