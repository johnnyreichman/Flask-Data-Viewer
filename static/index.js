$('#deleteOne').click(function() {
if ($(this).is(':checked')) {
  $(".shape3").hide();
  $(".shape5").hide();
  $(".shape8").hide();
  $(this).siblings('label').html('bring them back');
  $.post("AddRow",
  {
    "id": $('#idnum').val(),
    "name": $('#name').val(),
    "age": $('#age').val(),
    "state": $('#state').val(),
    "othernum": $('#othernum').val(),
  },
  function(result){
    $(this).siblings('label').html(result);
  });
} else {
  $(".shape3").show();
  $(".shape5").show();
  $(".shape8").show();
  $(this).siblings('label').html('Delete a column');
}
});

var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [{
            label: '# of Votes',
            data: [12, 19, 3, 5, 2, 3],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
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
    }
});
