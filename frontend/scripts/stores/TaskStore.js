/* jshint devel:true */

var AppDispatcher = require('../dispatcher/AppDispatcher');
var Constants = require('../constants/Constants');
var EventEmitter = require('events').EventEmitter;
var assign = require('object-assign');

var ActionType = Constants.ActionType;
var CHANGE_EVENT = 'change';

var _taskBeingEdited = null;
var _tasks = {};


function initialise(rawTasks) {

  _.forEach(rawTasks, function(task) {
    _tasks[task.id] = task;
  });
  _taskBeingEdited = null;
};

function noteTaskBeingEdited(taskId) {
  _taskBeingEdited = taskId;
};


var TaskStore = assign({}, EventEmitter.prototype, {

  emitChange: function() {
    this.emit(CHANGE_EVENT);
  },

  addChangeListener: function(callback) {
    this.on(CHANGE_EVENT, callback);
  },

  removeChangeListener: function(callback) {
    this.removeListener(CHANGE_EVENT, callback);
  },

  getAllTasks: function() {
    return _tasks;
  },

  getTaskBeingEdited: function() {
    return _taskBeingEdited;
  },

});


TaskStore.dispatchToken = AppDispatcher.register(function(action) {
      
  switch (action.type) {

    case ActionType.RECEIVE_TASKS:
      initialise(action.rawTasks);
      TaskStore.emitChange();
      break;

    case ActionType.EDIT_TASK:
      noteTaskBeingEdited(action.taskId);
      TaskStore.emitChange();
      break;

    default:
      // do nothing
  }
});


module.exports = TaskStore;
