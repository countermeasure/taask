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
        .replace(/extra\shigh/,4)
        .replace(/high/,3)
        .replace(/medium/,2)
        .replace(/extra\slow/,0)
        .replace(/low/,1);
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
    var sort_order = JSON.parse($( "#sort-order" ).html());
    $("#tasktable").tablesorter({
      widgets: ["filter"],
      headers: { 6: { sorter: 'priority' },
                 13: { sorter: 'view' },
               },
      sortList: sort_order,
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
    dateFormat: 'dd M yy',
    numberOfMonths: 2,
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
    var time = $( this ).prev().html();
    var hours = Math.floor( time/60 );
    var minutes = time % 60;
    var formatted_time = '';
    if ( ( hours != 0 ) || ( minutes != 0 ) ) {
      formatted_time = hours + ":" + ( minutes < 10 ? "0" : "" ) + minutes;
    };
    $( this ).html( formatted_time );
  });
  $( ".label-date" ).each(function() {
    var today = new Date();
    today.setHours(0,0,0,0);
    var tomorrow = new Date();
    tomorrow.setTime(today.getTime() + (24*60*60*1000));
    var yesterday = new Date();
    yesterday.setTime(today.getTime() - (24*60*60*1000));
    var day = $( this ).html();
    var date = Date.parse(day);
    if ( date == today.getTime() ) {
      $( this ).html ( "Today" );
      $( this ).removeClass ( "label-danger" );
      $( this ).addClass ( "label-warning" );
    } else if ( date == tomorrow.getTime() ) {
      $( this ).html ( "Tomorrow" );
      $( this ).removeClass ( "label-danger" );
      $( this ).addClass ( "label-success" );
    } else if ( date > tomorrow.getTime() ) {
      $( this ).removeClass ( "label-danger" );
      $( this ).addClass ( "label-success" );
    } else if ( date == yesterday ) {
      $( this ).html ( "Yesterday" );
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
    var task_id_verbatim = "#" + task_id
    $.ajax({
      url: target_url,
      type: "GET",
      dataType : "html",
      success: function( resp ) {
        $( task_id_verbatim ).hide();
        $( target ).html( resp );
      },
      complete: function() {
        ReactivateForm();
        ActivateDatepicker();
        MarkSelectedButtons();
        Accordian();
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
          $( row_id ).show();
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

/* Shows which radio buttons or checkboxes are selected
------------------------------------------------------- */

function MarkSelectedButtons() {
  $( "input" ).each(function() {
    var isButton = ["radio", "checkbox"].indexOf($( this ).attr( "type" )) > -1;
    if (isButton && $( this ).attr( "checked" ) == "checked") {
      $( this ).parent().addClass( "active" );
    }
  })
};

/* Enable form submission when Enter is pressed
-------------------------------------------------- */

$(document).keydown(function( event ) {
  if ( event.keyCode == 13 ) {
    var notes_has_focus = $( ".notes" ).is( ":focus" );
    if ( !notes_has_focus ) {
      $( ".btn-save" ).click();
      event.preventDefault();
    };
  };
});


/* Control the repeating task form fields
-------------------------------------------------- */

$(document).on("change", "#id_repeat_units", function() {
  var units = $( "#id_repeat_units" ).val();
  $( "#repeat-weekly, #repeat-monthly, #repeat-yearly" ).addClass( "hidden" );
  if ( units == "daily" ) {
    $( ".repeat-units" ).html( "day/s" );
  } else if ( units == "weekly" ) {
    $( ".repeat-units" ).html( "week/s" );
    $( "#repeat-weekly" ).toggleClass( "hidden" );
  } else if ( units == "monthly" ) {
    $( ".repeat-units" ).html( "month/s" );
    $( "#repeat-monthly" ).toggleClass( "hidden" );
  } else if ( units == "yearly" ) {
    $( ".repeat-units" ).html( "year/s" );
    $( "#repeat-monthly" ).toggleClass( "hidden" );
    $( "#repeat-yearly" ).toggleClass( "hidden" );
  } else if ( units == "" ) {
    $( ".repeat-units" ).html( "" );
  }
});


/* Control the underway field
-------------------------------------------------- */

function ManageUnderwayField() {
  $( ".underway-btn" ).on("click", function(event) {
    // Don't let the click bubble up to the row, or the task edit form opens.
    event.stopPropagation();
    var taskId = $( this ).attr( "taskid" );
    $.ajax({
      url: '../../../task/toggle-underway/' + taskId + '/',
      context: $( this )
    }).done(function(response) {
      $( this ).toggleClass( 'active' );
      var status = (response.underway) ? 'True' : 'False';
      $( this ).next().html( status );
      // Resort the table.
      $("table").trigger("update", [true]);
    });
  });
}


/* Collapse and expand task edit form sections
-------------------------------------------------- */

function Accordian() {
  // Hide the notes section if it is empty.
  if ($( "#id_notes" ).html() == "") {
    $( "#notes-body" ).addClass( "hidden" );
    $( "#notes-heading" ).html( 'Notes <i class="fa fa-caret-down"></i>' );
  }
  // Expand the notes section when its heading is clicked.
  $( "#notes-heading" ).on("click", function() {
    $( "#notes-body" ).removeClass( "hidden" );
    $( "#notes-heading" ).html( "Notes" );
  });
  // Hide the scheduling section if it is empty.
  if (
    !$( "#id_deadline" ).attr( "value" ) &&
    !$( "#id_scheduled" ).attr( "value" )
  ) {
    $( "#scheduling-body" ).addClass( "hidden" );
    var schedulingWithCaret = 'Scheduling <i class="fa fa-caret-down"></i>';
    $( "#scheduling-heading" ).html( schedulingWithCaret );
  }
  // Expand the scheduling section when its heading is clicked.
  $( "#scheduling-heading" ).on("click", function() {
    $( "#scheduling-body" ).removeClass( "hidden" );
    $( "#scheduling-heading" ).html( "Scheduling" );
  });
  // Hide the recurring section because it is not yet in use.
  // TODO: Hide this section only if it is empty.
  $( "#recurring-body" ).addClass( "hidden" );
  var recurringWithCaret = 'Recurring <i class="fa fa-caret-down"></i>';
  $( "#recurring-heading" ).html( recurringWithCaret );
  // Expand the recurring section when its heading is clicked.
  $( "#recurring-heading" ).on("click", function() {
    $( "#recurring-body" ).removeClass( "hidden" );
    $( "#recurring-heading" ).html( "Recurring" );
  });
}
