//<div id="calendar"></div> // <-- HTML CODE FOR CHART

function formateDate(date) {
	var day = date.getDate();
	var month = date.getMonth();
	var year = date.getYear();

	if(day < 10) {
		day = "0" + day;
	}

	if(month < 10) {
		month = "0" + month;
	}

	return year + "-" + month + "-" + day;
}

var today = new Date();
var data = {"events": [
	{
		title: 'Front-End Conference',
		start: '2018-11-16',
		end: '2018-11-18'
	},
	{
		title: 'Hair stylist with Mike',
		start: '2018-11-20',
		allDay: true
	},
	{
		title: 'Car mechanic',
		start: '2018-11-14T09:00:00',
		end: '2018-11-14T11:00:00'
	},
	{
		title: 'Dinner with Mike',
		start: '2018-11-21T19:00:00',
		end: '2018-11-21T22:00:00'
	},
	{
		title: 'Chillout',
		start: '2018-11-15',
		allDay: true
	},
	{
		title: 'Vacation',
		start: '2018-11-23',
		end: '2018-11-29'
	},
]};

$('#calendar').fullCalendar({
	header: {
		left: 'prev,next today',
		center: 'title',
		right: 'month,agendaWeek,agendaDay,listWeek'
	},
	defaultDate: formateDate(today),
	navLinks: true,
	eventLimit: true,
	events: data["events"]
});