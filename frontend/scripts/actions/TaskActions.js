/* jshint devel:true */

var AppDispatcher = require('../dispatcher/AppDispatcher');
var Constants = require('../constants/Constants');

var ActionType = Constants.ActionType;


var TaskActions = {

  saveTasks: function(tasks) {
    AppDispatcher.handleViewAction({
      type: ActionType.SAVE_TASKS,
      rawTasks: tasks
    });
  }

};


module.exports = TaskActions;
