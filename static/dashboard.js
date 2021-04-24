function FindCandidateForParty(candidates,party){
  var match = ""
  candidates.forEach((candidate)=>
  {
    if(candidate.Party === party){
      match = candidate.VotesRecieved;
    }
  });
  return match;
}

function BuildLineGraph(elections){
  var ctx = document.getElementById("myChart");
  var dates = [];
  var democrats = []
  var republicans = []
  elections.forEach((election) =>
    {
      dates.push(election.year);
      democrats.push(FindCandidateForParty(election.Candidates, "DEMOCRAT"));
      republicans.push(FindCandidateForParty(election.Candidates, "REPUBLICAN"));
    }
  );
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: dates,
      datasets: [{
        label: "Democrat",
        data: democrats,
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff'
      },
      {
        label: "Republican",
        data: republicans,
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#FF0000',
        borderWidth: 4,
        pointBackgroundColor: '#FF0000'
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: false
          }
        }]
      },
      legend: {
        display: true,
      }
    }
  });
}

var $overTimeBtn = $("#change-over-time");
$overTimeBtn.click(function() {
  $.get("ChangeOverTime",
  {
    state: "WI"
  },
   function(data){
       $('#content').html($(data.html));
       BuildLineGraph(data.elections);
       var $stateSelect = $("#state-select");
       $stateSelect.change(function() {
         $.get("ChangeOverTime",
         {
           state: $stateSelect.val()
         },
          function(data){
              $('#content').html($(data.html));
              BuildLineGraph(data.elections);
          });
       });
   });
});
