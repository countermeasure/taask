/* jshint devel:true */

var AppDispatcher = require('../dispatcher/AppDispatcher');
var Constants = require('../constants/Constants');

var ActionType = Constants.ActionType;


var FilterActions = {

  setFilter: function(filter) {
    AppDispatcher.handleViewAction({
      type: ActionType.SET_FILTER,
      activeFilter: filter
    });
  }

};


module.exports = FilterActions;
