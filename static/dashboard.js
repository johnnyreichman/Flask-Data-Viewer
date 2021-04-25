var $currentNavPage = $("#home");

function FindCandidateForParty(candidates,party){
  var match = ""
  candidates.forEach((candidate)=>
  {
    if(candidate.Party === party){
      if(match === "" || match.VotesRecieved < candidate.VotesRecieved){
        match = candidate;
      }
    }
  });
  return match;
}

function BuildLineGraph(elections){
  var ctx = document.getElementById("myChart");
  var dates = [];
  var democratPercents = []
  var republicanPercents = []
  var candidateHoverDict = {};
  elections.forEach((election) =>
    {
      dates.push(election.year);
      var democrat = FindCandidateForParty(election.Candidates, "DEMOCRAT");
      var republican = FindCandidateForParty(election.Candidates, "REPUBLICAN");
      var democratVoteShare = ((democrat.VotesRecieved / election.TotalVotes) * 100).toFixed(1);
      var republicanVoteShare = ((republican.VotesRecieved / election.TotalVotes) * 100).toFixed(1);
      democratPercents.push(democratVoteShare);
      republicanPercents.push(republicanVoteShare);
      candidateHoverDict[democratVoteShare] = democrat.Name;
      candidateHoverDict[republicanVoteShare] = republican.Name;
    }
  );
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: dates,
      datasets: [{
        label: "Democrat",
        data: democratPercents,
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff'
      },
      {
        label: "Republican",
        data: republicanPercents,
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#FF0000',
        borderWidth: 4,
        pointBackgroundColor: '#FF0000'
      }]
    },
    options: {
      tooltips: {
                enabled: true,
                mode: 'single',
                callbacks: {
                  label: function(tooltipItems, data) {
                      return candidateHoverDict[tooltipItems.yLabel] + ' : ' + tooltipItems.yLabel + " %";
                  }
                }
            },
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

//Load the OverTime Data
var $overTimeBtn = $("#change-over-time");
$overTimeBtn.click(function() {
  $currentNavPage.find(".nav-link").removeClass("active");
  $currentNavPage = $overTimeBtn;
  $overTimeBtn.find(".nav-link").addClass("active");
  $.get("ChangeOverTime",
  {
    state: "WI"
  },
   function(data){
       $('#content').html($(data.html));
       BuildLineGraph(data.elections);
       var $stateSelect = $("#state-select");
       $stateSelect.change(function() {
         $.get("ChangeState",
         {
           state: $stateSelect.val()
         },
          function(data){
              $('#chart-container').html($(data.html));
              BuildLineGraph(data.elections);
          });
       });
   });
});

var $dashboardBtn = $("#dashboard");
$dashboardBtn.click(function() {
  $currentNavPage.find(".nav-link").removeClass("active");
  $currentNavPage = $dashboardBtn;
  $dashboardBtn.find(".nav-link").addClass("active");
});

var $homeBtn = $("#home");
$homeBtn.click(function() {
  $currentNavPage.find(".nav-link").removeClass("active");
  $currentNavPage = $homeBtn;
  $homeBtn.find(".nav-link").addClass("active");
});
