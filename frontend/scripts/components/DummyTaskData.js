/* jshint devel:true */


var dummyTaskData = JSON.stringify([
{description:"Description of task 9",
 id:"9",
 view:"scheduled",
 time_remaining:"15",
 project:"ProjectA",
 context:"['Email']",
 priority:"High",
 scheduled:"2015-05-18",
 created:"2015-03-23",
 modified:"2015-03-23"
},
{description:"Description of task 7",
 id:"7",
 view:"inbox",
 created:"2015-03-21",
 modified:"2015-03-21"
},
{description:"Description of task 6",
 id:"6",
 view:"inbox",
 created:"2015-03-20",
 modified:"2015-03-20"
},
{description:"Description of task 3",
 id:"3",
 view:"today",
 time_remaining:"5",
 context:"['Work']",
 priority:"Medium",
 created:"2015-03-17",
 modified:"2015-03-22"
},
{description:"Description of task 1",
 id:"1",
 underway:"True",
 view:"today",
 time_remaining:"5",
 context:"['Work']",
 priority:"Extra High",
 created:"2015-03-16",
 modified:"2015-03-21"
}
]);


module.exports = dummyTaskData;
