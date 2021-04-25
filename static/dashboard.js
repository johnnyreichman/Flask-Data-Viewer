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

function BuildBarChart() {
  var ctx = document.getElementById("barChart");
  var barChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ["hi", "there", "sup"],
      datasets: [{
        label: 'My First Dataset',
        data: [1,2,3],
        backgroundColor: [
          'rgba(255, 99, 132, 0.2)',
          'rgba(255, 159, 64, 0.2)',
          'rgba(255, 205, 86, 0.2)',
          'rgba(75, 192, 192, 0.2)',
          'rgba(54, 162, 235, 0.2)',
          'rgba(153, 102, 255, 0.2)',
          'rgba(201, 203, 207, 0.2)'
        ],
        borderColor: [
          'rgb(255, 99, 132)',
          'rgb(255, 159, 64)',
          'rgb(255, 205, 86)',
          'rgb(75, 192, 192)',
          'rgb(54, 162, 235)',
          'rgb(153, 102, 255)',
          'rgb(201, 203, 207)'
        ],
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    },
  });
}
