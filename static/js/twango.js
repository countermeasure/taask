/* Get CSRF token
-------------------------------------------------- */

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};
var csrftoken = getCookie('csrftoken');


/* Manage the search field and the 'Clear search' button
-------------------------------------------------- */

$( "#search-box" ).focus(function () {
  $( "#clear-search" ).removeClass( "hidden" );
});
$( "#clear-search" ).click(function () {
  $( "#search-box" ).html();
  $( "#clear-search" ).addClass( "hidden" );
});


/* Make context buttons indicate current context
-------------------------------------------------- */

$( ".btn-context" ).click(function () {
  $( ".btn-context" ).filter( ".btn-primary" ).toggleClass(
    "btn-primary btn-default"
  );
  $( this ).toggleClass( "btn-default btn-primary" )
});


/* Activate Tablesorter filter and search
-------------------------------------------------- */

function ActivateTablesorter() {
  $.tablesorter.addParser({
    id: 'priority',
    is: function(s, table, cell) {
      return false;
    },
    format: function(s, table, cell, cellIndex) {
      return s.toLowerCase()
        .replace(/high/,2)
        .replace(/medium/,1)
        .replace(/low/,0);
    },
    type: 'numeric'
  });
  $.tablesorter.addParser({
    id: 'view',
    is: function(s, table, cell) {
      return false;
    },
    format: function(s, table, cell, cellIndex) {
      return s.toLowerCase()
        .replace(/inbox/,7)
        .replace(/today/,6)
        .replace(/next/,5)
        .replace(/scheduled/,4)
        .replace(/recurring/,3)
        .replace(/someday/,2)
        .replace(/completed/,1)
        .replace(/rubbish/,0);
    },
    type: 'numeric'
  });
  $(function(){
    $("#tasktable").tablesorter({
      widgets: ["filter"],
      headers: { 6: { sorter: 'priority' },
                 12: { sorter: 'view' },
               },
      // Sort by 'priority', then 'order', then 'time', then 'view'
      sortList: [[12,1],[6,1],[7,0],[5,0]],
      widgetOptions : {
        filter_columnFilters : false,
        filter_defaultFilter: { 0 : '~{query}' },
        filter_external : '.search',
        filter_reset: '.reset-filter',
      },
    });
    $('button[data-filter-column]').click(function(){
      $t = $(this);
      column = $t.data('filter-column');
      // The contents of 'context' need to be lower case for the search to
      // work, even if the term being searched for is upper case.
      context = $t.data('filter-text');
      var columns = [];
      columns[column] = context;
      $('table').trigger('search', [ columns ]);
    });
  });
};


/* Activate the date picker
-------------------------------------------------- */

function ActivateDatepicker() {
  $( ".datepicker" ).datepicker({
    inline: true
  });
};


/* Override Tablesorter's deactivation of forms
-------------------------------------------------- */

function ReactivateForm() {
  $('#form-contents').appendTo($('#edittaskform'));
};


/* Expand time and priority label abbreviations
-------------------------------------------------- */

function ExpandLabels() {
  $( ".label-time" ).each(function() {
    var time = $( this ).html();
    if ( (time) && !(time.substr(-4) =="mins")) {
      $( this ).append(" mins");
    };
  });
  $( ".label-priority" ).each(function() {
    var priority_code = $( this ).html();
    if ( priority_code == "L") {
      $( this ).html ( "Low" );
    } else if ( priority_code == "M" ) {
      $( this ).html ( "Medium" );
    } else if ( priority_code == "H" ) {
      $( this ).html ( "High" );
    };
  });
  $( ".label-date" ).each(function() {
    var today_raw = new Date();
    today = $.datepicker.formatDate( "dd M yy", today_raw);
    var tomorrow_raw = new Date();
    tomorrow_raw.setTime(today_raw.getTime() + (24*60*60*1000));
    tomorrow = $.datepicker.formatDate( "dd M yy", tomorrow_raw);
    var due_date = $( this ).html();
    if ( due_date == today ) {
      $( this ).html ( "Today" );
    } else if ( due_date == tomorrow ) {
      $( this ).html ( "Tomorrow" );
    };
  });
};


/* Enable Ajax form display and saving
-------------------------------------------------- */

function EnableAjaxForm() {
  // Display the task for editing
  $(document).one("click", ".task-row", function( EditTask ){
    var task_id = $( this ).attr("id");
    var task_no = task_id.slice(5);
    var target = "#edit-" + task_id;
    var target_url = $( this ).attr("url");
    $.ajax({
      url: target_url,
      type: "GET",
      dataType : "html",
      success: function( resp ) {
        $( target ).html( resp );
      },
      complete: function() {
        ReactivateForm();
        ActivateDatepicker();
      },
    });
  });
  // Save the edited task
  $(document).on("click", ".btn-save", function( SaveTask ){
    var task_id = $( this ).attr("id");
    var task_no = task_id.slice(10);
    var form_data = $( "#edittaskform" ).serialize();
    var target_url = $( "#edittaskform" ).attr( "action" );
    var row_id = "#task-" + task_no
    $.ajax({
      url: target_url,
      type: "POST",
      data: form_data,
      dataType : "html",
      success: function( resp ) {
        if (resp.substr(0,4) == "<td>") {
          // Do this if the response starts with <td>, which indicates
          // that the task was successfully updated.
          $( row_id ).html ( resp );
          $( "#task-edit-cell" ).remove();
          ExpandLabels();
          $("#tasktable").trigger('update');
          EnableAjaxForm();
        } else {
          // Otherwise, the response contains the form with validation
          // error messages, so render that.
          $( "#task-edit-cell" ).html ( resp );
          ReactivateForm();
          ActivateDatepicker();
        };
      },
    });
  });
};
