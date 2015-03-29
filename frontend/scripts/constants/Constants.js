/* jshint devel:true */

var keyMirror = require('keymirror');


module.exports = {

  ActionType: keyMirror({
    EDIT_TASK: null,
    RECEIVE_FILTERS: null,
    RECEIVE_TASKS: null,
    SET_FILTER: null,
    SAVE_TASKS: null
  })
  
};
