/* jshint devel:true */

var FilterActions = require('../actions/FilterActions');


var FilterItem = React.createClass({

  render: function() {
    var buttonClass = (this.props.status == 'on') ?
      "btn btn-primary" : "btn btn-default";
    return (
      <button
        type="button"
        key={this.props.filter}
        className={buttonClass}
        onClick={this._handleClick}>
        {this.props.filter}
      </button>
    );
  },

  _handleClick: function(event) {
    FilterActions.setFilter(this.props.filter);
  },


});


module.exports = FilterItem;
