/* jshint devel:true */

FilterList = require('./FilterList');
ConfigurationMenu = require('./ConfigurationMenu');

var Navbar = React.createClass({
  render: function() {
    return (
      <div className="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div className="container-fluid">
          <div className="navbar-header">
            <div className="navbar-brand">
              Taask
            </div>
          </div>
          <div className="navbar-collapse collapse">
            <ConfigurationMenu />
            <FilterList />
          </div>
        </div>
      </div>
    );
  }
});

module.exports = Navbar;
