/* jshint devel:true */

var assign = require('object-assign');
var TaskActions = require('../actions/TaskActions');
var FilterStore = require('../stores/FilterStore');
var TaskItemEdit = require('./TaskItemEdit');
var TaskItemView = require('./TaskItemView');
var TaskStore = require('../stores/TaskStore');
var WaitingSpinner = require('./WaitingSpinner');


function getStateFromTaskStores() {
  return {
    tasks: TaskStore.getAllTasks(),
    taskBeingEdited: TaskStore.getTaskBeingEdited()
  };
};

function getStateFromFilterStores() {
  return {
    activeFilter: FilterStore.getActiveFilter(),
    filters: FilterStore.getFilters(),
  };
};


var TaskList = React.createClass({

  getInitialState: function() {
    var initState = assign(
      getStateFromFilterStores(),
      {waiting: true}
    );
    return initState;
  },

  componentWillMount: function() {
    this.setState(
      assign(
        getStateFromFilterStores(),
        getStateFromTaskStores()
      )
    );
  },

  componentDidMount: function() {
    FilterStore.addChangeListener(this._onFiltersChange);
    TaskStore.addChangeListener(this._onTasksChange);
  },

  componentWillUnmount: function() {
    FilterStore.removeChangeListener(this._onFiltersChange);
    TaskStore.removeChangeListener(this._onTasksChange);
  },

  render: function() {

    var activeFilter = +this.state.activeFilter;
    var filters = this.state.filters;
    var taskBeingEdited = this.state.taskBeingEdited;
    var taskItems = [];
    var tasks = this.state.tasks;

    _.forEach(tasks, function(props, key) {
      var contextNo = +props.context;
      if (_.includes([contextNo, 0], activeFilter)) {
        var context = filters[contextNo]['context'];

        switch (props['id'] == taskBeingEdited) {

          case true:
            taskItems.push(
              <TaskItemEdit
                {...props}
                key={key}
                context={context}
                filter={activeFilter}
              />
            );
            break;

          case false:
            taskItems.push(
              <TaskItemView
                {...props}
                key={key}
                context={context}
                filter={activeFilter}
              />
            );
            break;

        };
      };
    });

    switch (this.state.waiting) {

      case true:
        return (
          <div className="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
            <WaitingSpinner />
          </div>
        );
        break;

      case false:
        return (
          <div className="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
            <table className="table tablesorter" id="tasktable">
              <thead>
                <tr>
                  <th><i className="fa fa-toggle-right fa-lg"></i></th>
                  <th>Description</th>
                  <th>Project</th>
                  <th>Contexts</th>
                  <th>Time remaining</th>
                  <th>Time spent</th>
                  <th>Priority</th>
                  <th>Deadline</th>
                  <th>Postpone</th>
                  <th>Repeat units</th>
                  <th>Repeat next</th>
                  <th>Repeat ends</th>
                  <th>Completed</th>
                 </tr>
              </thead>
              <tbody>
                {taskItems}
              </tbody>
            </table>
          </div>
        );
        break;

      default:
        // do nothing

    };
  },

  _onFiltersChange: function() {
    this.setState(
      getStateFromFilterStores()
    );
  },

  _onTasksChange: function() {
    this.setState(
      assign(
        getStateFromFilterStores(),
        getStateFromTaskStores(),
        {waiting: false}
      )
    );
  },

});


module.exports = TaskList;
