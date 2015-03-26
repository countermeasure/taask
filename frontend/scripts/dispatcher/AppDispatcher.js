/* jshint devel:true */

var Dispatcher = require('flux').Dispatcher;
var assign = require('object-assign');


var AppDispatcher = assign(new Dispatcher(), {
  handleViewAction: function(action) {
    description = JSON.stringify(action);
    console.log('*** DISPATCHER:  ' + _.trunc(description, 100));
    this.dispatch(action);
  }
});


module.exports = AppDispatcher;
