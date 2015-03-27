/* jshint devel:true */

var TaskActions = require('../actions/TaskActions');
var FilterStore = require('../stores/FilterStore');
var TaskItem = require('./TaskItem');
var TaskStore = require('../stores/TaskStore');
var WaitingSpinner = require('./WaitingSpinner');


function getActiveFilter() {
  return FilterStore.getActiveFilter();
};

function getFilters() {
  return FilterStore.getFilters();
};

function getAllTasks() {
  return TaskStore.getAllTasks();
};


var TaskList = React.createClass({

  getInitialState: function() {
    return {
      filter: getActiveFilter(),
      waiting: true
    };
  },

  componentWillMount: function() {
    this.setState({filter: getActiveFilter()});
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
    var activeFilter = +this.state.filter;
    var filters = getFilters();
    var taskItems = [];
    _.forEach(getAllTasks(), function(value, key) {
      /* value.context is an array, so .flatten is required to effectively
         add All to it */
      if (_.includes(_.flatten([value.context, 0]), activeFilter)) {
        var contextNo = +value.context;
        taskItems.push(
          <TaskItem
            key={key}
            completed={value['completed']}
            description={value['description']}
            deadline={value['deadline']}
            repeat_details={value['repeat_details']}
            repeat_ends={value['repeat_ends']}
            repeat_every={value['repeat_every']}
            repeat_next={value['repeat_next']}
            repeat_units={value['repeat_units']}
            notes={value['notes']}
            scheduled={value['scheduled']}
            time_remaining={value['time_remaining']}
            time_spent={value['time_spent']}
            underway={value['underway']}
            view={value['view']}
            context={filters[contextNo]['context']}
            priority={value['priority']}
            project={value['project']}
            task={value['task']}
          />
        );
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
    this.setState({filter: getActiveFilter()});
  },

  _onTasksChange: function() {
    this.setState({
      tasks: getAllTasks(),
      waiting: false
    });
  },

});


module.exports = TaskList;
