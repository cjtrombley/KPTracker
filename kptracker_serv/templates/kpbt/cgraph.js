var ctxL = document.getElementById("lineChart").getContext('2d');

var data = {"xAxisLabels": ["January", "February", "March", "April", "May", "June", "July"], "datasets":  {
	label: "My First dataset",
	data: [28, 48, 40, 19, 86, 27, 90],
	backgroundColor: ['rgba(0, 137, 132, .2)'],
	borderColor: ['rgba(0, 10, 130, .7)'],
	borderWidth: 2
}}

var myLineChart = new Chart(ctxL, {
	type: 'line',
	data: {
		labels: xAxisLabels,
		datasets: [ data['datasets'] ]
	},
	options: {
		responsive: true
	}
});
