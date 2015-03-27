/* jshint devel:true */

var AppDispatcher = require('../dispatcher/AppDispatcher');
var Constants = require('../constants/Constants');

var ActionType = Constants.ActionType;


var FilterActions = {

  setFilter: function(newFilter) {
    AppDispatcher.handleViewAction({
      type: ActionType.SET_FILTER,
      newFilter: newFilter
    });
  }

};


module.exports = FilterActions;
