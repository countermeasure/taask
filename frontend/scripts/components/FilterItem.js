/* jshint devel:true */

var FilterActions = require('../actions/FilterActions');


var FilterItem = React.createClass({

  render: function() {
    var buttonClass = (this.props.status == 'on') ?
      "btn btn-primary" : "btn btn-default";
    return (
      <button
        type="button"
        className={buttonClass}
        onClick={this._handleClick}>
        {this.props.context}
      </button>
    );
  },

  _handleClick: function() {
    FilterActions.setFilter(this.props.id);
  },


});


module.exports = FilterItem;
