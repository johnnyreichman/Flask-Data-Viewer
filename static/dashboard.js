
//Build the pie chart that compares what happens to popular congressional candidates
function BuildPieChart(pieRawData) {
  var ctx = document.getElementById("pieChart");
  var pieChart = new Chart(ctx, {
    type: 'pie',
    data:  {
      labels: [
        'One Term',
        'Two Term',
        '2+ Term'
      ],
      datasets: [{
        label: 'Popular candidate dataset',
        data: pieRawData,
        backgroundColor: [
          'rgb(255, 99, 132)',
          'rgb(54, 162, 235)',
          'rgb(0,128,0)'
        ],
        hoverOffset: 4
      }]
    }
  });
}

const barChartOptions = {
  scales: {
    yAxes: [{
      ticks: {
        beginAtZero: true
      },
    scaleLabel: {
      display: true,
      labelString: "Turnout"
    }
  }],
    xAxes: [{
      scaleLabel: {
        display: true,
        labelString: "Election year"
      }
    }]
  }
};

//Build the bar chart comparing presidential, house, and senate turnout over the years
function BuildBarChart(barData) {
  var senateTurnout = [];
  var houseTurnout = [];
  var presTurnount = [];
  var years = Object.keys(barData[1]);

  years.forEach((year) =>
  {
    senateTurnout.push(barData[0][year]);
    houseTurnout.push(barData[1][year]);
    presTurnount.push(barData[2][year]);
    });

  var ctx = document.getElementById("barChart");
  var barChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: years,
      datasets: [{
        label: 'Senate Turnout',
        data: senateTurnout,
        backgroundColor: 'rgb(255, 99, 132)'
      },
      {
        label: 'House Turnout',
        data: houseTurnout,
        backgroundColor: 'rgb(54, 162, 235)'
      },
      {
        label: 'Presidential Turnout',
        data: presTurnount,
        backgroundColor: 'rgb(0,128,0)'
      }
    ]},
    options: barChartOptions
  });
}
