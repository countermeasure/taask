/* jshint devel:true */

Navbar = require('./Navbar');
Sidebar = require('./Sidebar');
TaskList = require('./TaskList');


var Application = React.createClass({
  render: function() {
    return (
      <div>
        <Navbar />
        <div className="container-fluid">
          <div className="row">
            <Sidebar />
            <TaskList />
          </div>
        </div>
      </div>
    );
  }
});


module.exports = Application;
