/* jshint devel:true */

var AppDispatcher = require('../dispatcher/AppDispatcher');
var Constants = require('../constants/Constants');
var EventEmitter = require('events').EventEmitter;
var assign = require('object-assign');

var ActionType = Constants.ActionType;
var CHANGE_EVENT = 'change';

var _filters = {};


function initialise(rawFilters) {
  _filters['All'] = 'on';
  _.forEach(rawFilters, function(filter) {
    _filters[filter['context']] = 'off';
  });
};

function updateState(filter) {
  _.forEach(_filters, function(value, key) {
    _filters[key] = 'off';
  });
  _filters[filter] = 'on';
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
    activeFilter =  _.findKey(_filters, function(chr) {
      return chr == 'on';
    });
    if (activeFilter) {
      activeFilter = activeFilter.toLowerCase();
    };
    return activeFilter;
  },

});


FilterStore.dispatchToken = AppDispatcher.register(function(action) {
      
  switch (action.type) {

    case ActionType.RECEIVE_FILTERS:
      initialise(action.rawFilters);
      FilterStore.emitChange();
      break;

    case ActionType.SET_FILTER:
      updateState(action.activeFilter);
      FilterStore.emitChange();
      break;

    default:
      // do nothing
  }
});


module.exports = FilterStore;
