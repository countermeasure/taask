/* jshint devel:true */


var ConfigurationMenu = React.createClass({

  render: function() {
    return (
      <ul className="nav navbar-nav navbar-right">
        <li className="dropdown">
          <a href="#" className="dropdown-toggle" data-toggle="dropdown">
            <i className="fa fa-cog fa-lg"></i>
            &nbsp;&nbsp;
            <i className="fa fa-caret-down fa-lg"></i>
          </a>
          <ul className="dropdown-menu" role="menu">
            <li><a href="#">Contexts</a></li>
            <li><a href="#">Priorities</a></li>
            <li><a href="#">Projects</a></li>
            <li className="divider"></li>
            <li><a href="#">Documentation</a></li>
          </ul>
        </li>
      </ul>
    );
  }
});


module.exports = ConfigurationMenu;
