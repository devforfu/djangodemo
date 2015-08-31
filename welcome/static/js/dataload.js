// Custom functions to support CSRF tokens (django)
function getCookie(name) {
    var cookieValue = null;

    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');

        for (var i = 0; i < cookies.length; i++) {
            var cookie = $.trim(cookies[i]);

            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        var safe = /^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type);
        var token = getCookie('csrftoken')

        if (!safe && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", token);
        }
    }
});


//Generating random data.
var localData  = {};

localData.dataForBarChart = [];

//var startingDate = new Date(2015, 4, 1);
//var sDate = new Date(startingDate);
//for(var i = 0; i<100; i++){
//	var obj = {};
//	obj.date = new Date(startingDate);
//	obj.val = Math.round(Math.random() * 500);
//	localData.dataForBarChart.push(obj);
//	startingDate.setDate(startingDate.getDate()+1);
//}
//startingDate.setDate(startingDate.getDate()-1);
//var eDate = new Date(startingDate);
//// startingDate.setMonth(startingDate.getMonth()+2);
//var endDate = new Date(startingDate);

var startingDate = new Date(2015, 7, 1);

var sDate = new Date(startingDate);
startingDate.setDate(startingDate.getDate() + 99);

var eDate = new Date(startingDate);
//startingDate.setMonth(startingDate.getMonth() + 2);

var endDate = new Date(startingDate);


$('#date1').datetimepicker({
	language:  'eng',
	weekStart: 1,
	startDate: sDate,
	endDate: endDate,
	autoclose: 1,
	startView: 2,
	minView: 2,
	initialDate: sDate
});

$('#date2').datetimepicker({
	language:  'eng',
	weekStart: 1,
	startDate: sDate,
	endDate: endDate,
	autoclose: 1,
	startView: 2,
	minView: 2,
	initialDate: eDate
});

$('#date1')
.datetimepicker()
.on('changeDate', function(ev){
	$('#date2').datetimepicker('setStartDate', ev.date);
	sDate = new Date(ev.date);
	loadData('dataForBarChart', '#area1', barChartRender);
	loadData('users', '#metrics', lineChartRender);
});

$('#date2')
.datetimepicker()
.on('changeDate', function(ev){
	var newEndDate = new Date(ev.date);
	endDate = new Date(newEndDate);
	newEndDate.setMonth(newEndDate.getMonth()+2);
	$('#date1').datetimepicker('setEndDate', newEndDate);
	loadData('dataForBarChart', '#area1', barChartRender);
	loadData('users', '#metrics', lineChartRender);
});

localData.users = [];

var startingDate = new Date(sDate);
for (var i = 0; i < 100; i++) {          
	var tmpObj  = {};             
	tmpObj.date = new Date(startingDate);        
	tmpObj.DAU  = Math.round(Math.random() * 300);
	localData.users.push(tmpObj);
	startingDate.setDate(startingDate.getDate()+1);
}

localData.openTickets = Math.round(Math.random() * 100);
localData.avgReplyTime = (Math.random() * 5).toFixed(2);;
localData.avgTicketCloseTime = (Math.random() * 20).toFixed(2);;

//var loadData = function loadData(dataName, reference, callback) {
//	if(dataName==='dataForBarChart'){
//		var arr = [];
//		for(var i = 0; i < localData.dataForBarChart.length; i++){
//			if(localData.dataForBarChart[i].date>=sDate && localData.dataForBarChart[i].date<=endDate){
//				arr.push(localData.dataForBarChart[i]);
//			}
//		}
//		callback(reference, arr);
//		return;
//	}
//	if(dataName==='users'){
//		var arr = [];
//		for(var i = 0; i < localData.users.length; i++){
//			if(localData.users[i].date>=sDate && localData.users[i].date<=endDate){
//				arr.push(localData.users[i]);
//			}
//		}
//		callback(reference, arr);
//		return;
//	}
//	callback(reference, localData[dataName]);
//}

function convertDate(date) {
    var day = date.getDate();
    var month = date.getMonth();
    var year = date.getFullYear();

    return (month + 1) + "/" + day + "/" + year;
}

var loadData = function loadData(dataName, reference, callback) {
    var handlers = {
        "dataForBarChart": "bar_chart",
        "users": "users",
        "openTickets": "open_tickets",
        "avgReplyTime": "avg_reply_time",
        "avgTicketCloseTime": "avg_ticket_close_time"
    };

    if (handlers[dataName] == undefined)
        return;

    $.ajax({
        url: "/welcome/chart/" + handlers[dataName],
        type: "post",
        data: {
            'start_date': convertDate(sDate),
            'end_date': convertDate(endDate)
        },

        success: function(data) {
            //alert(data);
            //return;

            var result = JSON.parse(data)['result'];

            if (Object.prototype.toString.call(result) === '[object Array]') {
                var arr = [];

                for (var i = 0; i < result.length; ++i) {
                    var entry = result[i];

                    entry.date = new Date(entry.date);
                    arr.push(entry);
                }

                callback(reference, arr);

            } else {
                callback(reference, result);
            }
        },

        error: function() {
            alert('Error occurred!');
        }
    });

    //event.preventDefault();
};

// It should work like this:

// loadData(dataName, reference, callback);

// dataName: its' the name of the data e.g. "opentickets"
// reference: dom element were the chart should go
// callback: It calls the chart rendering function and as parameter it pass the data and reference

// ChartRender(reference, data);
// This is the chart rendering (or better just data binding) function which get called from loadData

function barChartRender (reference, data) {
	document.querySelector(reference).innerHTML = '';

	var margin = {top: 50, right: 20, bottom: 70, left: 40},
	    width = 620 - margin.left - margin.right,
	    height = 300 - margin.top - margin.bottom;

	// Parse the date / time
	var	parseDate = d3.time.format("%Y-%m").parse;

	var x = d3.scale.ordinal().rangeRoundBands([0, width], .05);

	var y = d3.scale.linear().range([height, 0]);

	var xAxis = d3.svg.axis()
    	.scale(x)
    	.orient("bottom")
    	// .tickValues([1, 2, 3])
    	.tickFormat(d3.time.format("%d-%m-%y"));

	var yAxis = d3.svg.axis()
	    .scale(y)
	    .orient("left")
	    .ticks(10);

	var chart1 = d3.select(reference).append("svg")
	    .attr("width", width + margin.left + margin.right)
	    .attr("height", height + margin.top + margin.bottom)
		.append("g")
	    .attr("transform", 
	          "translate(" + margin.left + "," + margin.top + ")");

    data.forEach(function(d) {
        // d.date = parseDate(d.date);
        d.val = +d.val;
    });
	
  x.domain(data.map(function(d) { return d.date; }));
  y.domain([0, d3.max(data, function(d) { return d.val; })]);

  chart1.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
    .selectAll("text")
      .attr("class", "x-axis-label")
      .style("text-anchor", "end")
      .attr("dx", "-1em")
      .attr("dy", "-.5em")
      .attr("transform", "rotate(-90)" );

    var labels = document.querySelectorAll('.x-axis-label');
    console.log(labels);
    for(var i = 0; i < labels.length; i++){
    	if(i%3!=0){
    		labels[i].innerHTML = '';
    	}
    }

    chart1.append("text")
	    .attr("class", "axis-label")
	    .attr("text-anchor", "end")
	    .attr("x", -10)
	    .attr("y", height + 34)
	    .text('Date');

  chart1.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      // .attr("transform", "rotate(-90)")
      .attr("y", -20)
      // .attr("dy", "1em")
      // .style("text-anchor", "end")
      .text("Number of open tickets");

  chart1.selectAll("bar")
      .data(data)
    .enter().append("rect")
      .style("fill", "steelblue")
      .attr("x", function(d) { return x(d.date); })
      .attr("width", x.rangeBand())
      .attr("y", function(d) { return y(d.val); })
      .attr("height", function(d) { return height - y(d.val); });
}

function lineChartRender (reference, data) {
	function getMaxObjectValue(this_array, element) {
		var values = [];
		for (var i = 0; i < this_array.length; i++) {
			values.push(Math.ceil(parseFloat(this_array[i][""+element])));
		}
		values.sort(function(a,b){return a-b});
		return values[values.length-1];
	}

	function getMinObjectValue(this_array, element) {
		var values = [];
		for (var i = 0; i < this_array.length; i++) {
			values.push(Math.floor(parseFloat(this_array[i][""+element])));
		}
		values.sort(function(a,b){return a-b});
		return values[0];
	}

	document.querySelector(reference).innerHTML = '';

	var width = 600, height = 300;
	var margin = {top: 30, right: 10, bottom: 40, left: 60}, width = width - margin.left - margin.right, height = height - margin.top - margin.bottom;
	
	var minDate = (data[0].date),
	maxDate = data[data.length-1].date;
	minObjectValue = getMinObjectValue(data, 'DAU');
	maxObjectValue = getMaxObjectValue(data, 'DAU');

	var vis= d3.select(reference).append("svg")
    	.data(data)
		.attr("class", "metrics-container")
   		.attr("width", width + margin.left + margin.right)
    	.attr("height", height + margin.top + margin.bottom)
  	.append("g")
    	.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	var y = d3.scale.linear().domain([ minObjectValue - (.1 * minObjectValue) , maxObjectValue + (.1 * maxObjectValue) ]).range([height, 0]),
	x = d3.time.scale().domain([minDate, maxDate]).range([0, width]);

	var yAxis = d3.svg.axis()
		.scale(y)
		.orient("left")
		.ticks(5);

	var xAxis = d3.svg.axis()
		.scale(x)
		.orient("bottom")
		.ticks(5);

	vis.append("g")
	    .attr("class", "axis")
	    .call(yAxis);

	vis.append("g")
		.attr("class", "axis")
	    .attr("transform", "translate(0," + height + ")")
	    .call(xAxis);

	//add the axes labels
	vis.append("text")
	    .attr("class", "axis-label")
	    .attr("text-anchor", "end")
	    .attr("x", 20)
	    .attr("y", height + 34)
	    .text('Date');

	vis.append("text")
	    .attr("class", "axis-label")
	    // .attr("text-anchor", "end")
	    .attr("y", -20)
	    .attr("x", 10)
	    // .attr("transform", "rotate(-90)")
	    .text('Avg Replytime');

	var line = d3.svg.line()
		.x(function(d) { return x(d["date"]); })
		.y(function(d) { return y(d["DAU"]); })

	vis.append("svg:path")
		.attr("d", line(data))
		.style("stroke", function() { 
			return "#000000";
		})
		.style("fill", "none")
		.style("stroke-width", "2.5");

	var dataCirclesGroup = vis.append('svg:g');

	var circles = dataCirclesGroup.selectAll('.data-point')
		.data(data);

	circles
		.enter()
		.append('svg:circle')
		.attr('class', 'dot')
		.attr('fill', function() { return "red"; })
		.attr('cx', function(d) { return x(d["date"]); })
		.attr('cy', function(d) { return y(d["DAU"]); })
		.attr('r', function() { return 3; })
		.on("mouseover", function(d) {
				d3.select(this)
				.attr("r", 8)
				.attr("class", "dot-selected")
				.transition()
  					.duration(750);
		})
		.on("mouseout", function(d) {
				d3.select(this)
				.attr("r", 3)
				.attr("class", "dot")
				.transition()
  					.duration(750);
		});
}

function renderText (reference, data) {
	document.querySelector(reference).innerHTML = data;
}

loadData('dataForBarChart', '#area1', barChartRender);
loadData('users', '#metrics', lineChartRender);
loadData('openTickets', '#openTickets', renderText);
loadData('avgReplyTime', '#replyTime', renderText);
loadData('avgTicketCloseTime', '#closeTime', renderText);