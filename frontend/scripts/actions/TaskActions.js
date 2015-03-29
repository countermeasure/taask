/* jshint devel:true */

var AppDispatcher = require('../dispatcher/AppDispatcher');
var Constants = require('../constants/Constants');

var ActionType = Constants.ActionType;


var TaskActions = {

  editTask: function(taskId) {
    AppDispatcher.handleViewAction({
      type: ActionType.EDIT_TASK,
      taskId: taskId
    });
  }

};


module.exports = TaskActions;
