(function (){

  var upcomingButton = document.getElementById("upcoming-btn");
  var pastButton = document.getElementById("past-btn");

  upcomingButton.addEventListener("click", toggleButtons);
  pastButton.addEventListener("click", toggleButtons);

  function toggleButtons(e){
    if (e.target.className == 'btn btn-default active') {
      return
    } else {
      switchActive();
      switchProfiles();
    };
  };

  function switchActive(){
    if (upcomingButton.className == 'btn btn-default active'){
      upcomingButton.className = 'btn btn-default'
      pastButton.className = 'btn btn-default active'
    } else {
      upcomingButton.className = 'btn btn-default active'
      pastButton.className = 'btn btn-default'
    };
  };

  function switchProfiles(){
    var upcomingList = document.getElementsByClassName("upcoming-group");
    var passedList = document.getElementsByClassName("passed-group");

    if (upcomingList[0].className == 'list-group upcoming-group'){
      upcomingList[0].className = 'list-group upcoming-group hide-group'
      passedList[0].className = 'list-group passed-group'
    } else {
      upcomingList[0].className = 'list-group upcoming-group'
      passedList[0].className = 'list-group passed-group hide-group'
    };
  };

  

  

})();



