

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

function hideProfiles(){
  var profiles = document.getElementsByClassName("patient-profile");
  var arrayLength = profiles.length;
  for (var i = 0; i < arrayLength; i++) {
      profiles[i].className = "patient-profile profile-hidden";
  };
};

function showProfile(e){
  hideProfiles();
  var arrayLength = patient_data.length;
  for (var i = 0; i < arrayLength; i++) {
      if (patient_data[i].id == e ) {
        
        var activeProfile = document.getElementById('profile-'.concat(patient_data[i].id));
        activeProfile.className = "patient-profile";
      };
  };
};

