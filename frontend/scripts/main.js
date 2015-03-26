/* jshint devel:true */

// This file bootstraps the app

var APIRequestActions = require('./actions/APIRequestActions');
var Application = require('./components/Application');


APIRequestActions.initialiseApp();


React.render(
  <Application />,
  document.getElementById('main')
);
