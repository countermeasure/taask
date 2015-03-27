/* jshint devel:true */


var WaitingSpinner = React.createClass({

  render: function() {
    return (
      <div className="text-center spinner">
        <i className="fa fa-circle-o-notch fa-spin fa-5x"></i>
      </div>
    );
  },

});


module.exports = WaitingSpinner;
