/* jshint devel:true */

var TaskActions = require('../actions/TaskActions');
var TaskStore = require('../stores/TaskStore');

var TaskItemView = React.createClass({

  render: function() {
  
    var visibility = (this.props.filter != this.props.context) ? "" : "";
    
    return (
      <tr className="{visibility}" onClick={this._handleClick}>
        <td>
          <i className="fa fa-toggle-right fa-lg"></i>
        </td>
        <td>
          {this.props.description} <i className="fa fa-file-text"></i>
        </td>
        <td>
          <span className="label label-default">
            {this.props.project}
          </span>
        </td>
        <td>
          <span className="label label-primary">
            {this.props.context}
          </span>
        </td>
        <td>
          <span className="label label-primary label-time">
            {this.props.time_remaining} mins
          </span>
        </td>
        <td>
          <span className="label label-primary label-time">
            {this.props.time_spent} mins
          </span>
        </td>
        <td>
          <span className="label label-primary">
            {this.props.priority}
          </span>
        </td>
        <td>
          <span className="label label-danger label-date">
            {this.props.deadline}
          </span>
        </td>
        <td>
          <span className="label label-danger label-date">
            {this.props.scheduled}
          </span>
        </td>
        <td>
          <span className="label label-danger">
            {this.props.repeat_units}
          </span>
        </td>
        <td>
          <span className="label label-danger label-date">
            {this.props.repeat_next}
          </span>
        </td>
        <td>
          <span className="label label-danger label-date">
            {this.props.repeat_ends}
          </span>
        </td>
        <td>
          <span className="label label-danger label-date">
            {this.props.completed}
          </span>
        </td>
      </tr>
    );
  },

  _handleClick: function () {
    TaskActions.editTask(this.props.id);
  },

});


module.exports = TaskItemView;
