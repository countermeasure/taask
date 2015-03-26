/* jshint devel:true */

var FilterItem = require('./FilterItem');
var FilterStore = require('../stores/FilterStore');


function getFilters() {
  return FilterStore.getFilters();
};


var FilterList = React.createClass({

  getInitialState: function() {
    return {filters: getFilters()};
  },

  componentDidMount: function() {
    FilterStore.addChangeListener(this._onChange);
  },

  componentWillUnmount: function() {
    FilterStore.removeChangeListener(this._onChange);
  },

  render: function() {
    filters = this.state.filters;
    var filterItems = [];
    _.forEach(filters, function(status, filter) {
      filterItems.push(
        <FilterItem
          key={filter}
          filter={filter}
          status={status}
        />
      );
    });
    return (
      <div className="navbar-form navbar-right">
        {filterItems}
      </div>
    );
  },
  
  _onChange: function() {
    this.setState(getFilters());
  },
  
});


module.exports = FilterList;
