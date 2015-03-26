/* jshint devel:true */

TaskList = require('./TaskList');


var Sidebar = React.createClass({
  render: function() {
    return (
      <div className="col-sm-3 col-md-2 sidebar">
        <button type="button" className="btn btn-primary">
          <i className="fa fa-plus-circle fa-lg"></i>
          &nbsp;&nbsp;Add new task
        </button>
        <br/><br/>
        <small>NEW</small>
        <ul className="nav nav-sidebar">
          <li id="inbox">
            <a href="#">
              Inbox
              <span className="badge pull-right">
                count
              </span>
            </a>
          </li>
        </ul>
        <small>VIEWS</small>
        <ul className="nav nav-sidebar">
          <li id="today">
            <a href="#">
              Today
              <span className="badge pull-right">
                count
              </span>
              <span className="badge pull-right">
                <span className="label-time">
                  time hrs
                </span>
              </span>
            </a>
          </li>
          <li id="next">
            <a href="#">
              Next
              <span className="badge pull-right">
                count
              </span>
            </a>
          </li>
          <li id="scheduled">
            <a href="#">
              Scheduled
              <span className="badge pull-right">
                count
              </span>
            </a>
          </li>
          <li id="recurring">
            <a href="#">
              Recurring
              <span className="badge pull-right">
                count
              </span>
            </a>
          </li>
          <li id="someday">
            <a href="#">
              Someday
              <span className="badge pull-right">
                count
              </span>
            </a>
          </li>
        </ul>
        <small>PROJECTS</small>
        <ul className="nav nav-sidebar">
          <li id="project_1">
            <a href="#">
              project 1
            </a>
          </li>
          <li id="project_2">
            <a href="#">
              project 2
            </a>
          </li>
        </ul>
        <small>OLD</small>
        <ul className="nav nav-sidebar">
          <li id="completed">
            <a href="#">
              Completed
            </a>
          </li>
          <li id="rubbish">
            <a href="#">
              Rubbish
              <span className="badge pull-right">
                count
              </span>
            </a>
          </li>
        </ul>
        <small>SEARCH</small>
        <form role="form" className="nav nav-sidebar navbar-form">
          <input type="text" className="search form-control"
            placeholder="Search in menu..." />
          <button type="button" className="btn btn-primary hidden">
            Clear search
          </button>
        </form>
      </div>
    );
  }
});


module.exports = Sidebar;
