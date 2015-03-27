/* jshint devel:true */

var AppDispatcher = require('../dispatcher/AppDispatcher');
var Constants = require('../constants/Constants');
var EventEmitter = require('events').EventEmitter;
var assign = require('object-assign');

var ActionType = Constants.ActionType;
var CHANGE_EVENT = 'change';

var _filters = {};


function initialise(rawFilters) {
  _filters[0] = {context: 'All', status: 'on'};
  _.forEach(rawFilters, function(filter) {
    _filters[filter['id']] = {
      context: filter['context'],
      status: 'off'
    };
  });
};

function updateState(newFilter) {
  _.forEach(_filters, function(obj, id) {
    _filters[id]['status'] = 'off';
  });
  _filters[newFilter]['status'] = 'on';
};


var FilterStore = assign({}, EventEmitter.prototype, {

  emitChange: function() {
    this.emit(CHANGE_EVENT);
  },

  addChangeListener: function(callback) {
    this.on(CHANGE_EVENT, callback);
  },

  removeChangeListener: function(callback) {
    this.removeListener(CHANGE_EVENT, callback);
  },

  getFilters: function() {
    return _filters;
  },

  getActiveFilter: function() {
    return  _.findKey(_filters, 'status', 'on');
  },

});


FilterStore.dispatchToken = AppDispatcher.register(function(action) {
      
  switch (action.type) {

    case ActionType.RECEIVE_FILTERS:
      initialise(action.rawFilters);
      FilterStore.emitChange();
      break;

    case ActionType.SET_FILTER:
      updateState(action.newFilter);
      FilterStore.emitChange();
      break;

    default:
      // do nothing
  }
});


module.exports = FilterStore;
