(function (){

  var upcomingButton = document.getElementById("upcoming-btn");
  var pastButton = document.getElementById("past-btn");

  function greetingBtnListen(){
    var arrayLength = patient_data.length;
    for (var i = 0; i < arrayLength; i++) {
      var greetBtnElem = document.getElementById('greet-'.concat(patient_data[i].id));
      greetBtnElem.addEventListener("click", createMessage)
    };
  }; 

  function toggleCheckMark(patient_id) {
      var children = document.getElementById(patient_id).childNodes;

      for (var i = 0; i < children.length; i++) {
          if (children[i].tagName == "SPAN") {
              var checkSign = children[i];
              if (checkSign.className.includes('msg-sent')) {
                  return
              }
              else {
                  checkSign.className = checkSign.className.concat(' msg-sent')
              }
          };
      };
  };

  function createMessage(e) {

    var id = e.currentTarget.id.substr(6);
    
    $(function () {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        var csrftoken = getCookie('csrftoken');

        $.post(
          "http://127.0.0.1:8000/create_message",
          {
            "patient_id":id,
            'csrfmiddlewaretoken': csrftoken
          },
          toggleCheckMark(id)
        );

    });
  };

  function patientListListen(){
    var arrayLength = patient_data.length;
    for (var i = 0; i < arrayLength; i++) {
      var patientElem = document.getElementById(patient_data[i].id);
      patientElem.addEventListener("click", showProfile)
    }
  }

  function showProfile(e){

      hideProfiles();
      var arrayLength = patient_data.length;
      for (var i = 0; i < arrayLength; i++) {
          if (patient_data[i].id == e.currentTarget.id ) {
            
            var activeProfile = document.getElementById('profile-'.concat(patient_data[i].id));
            activeProfile.className = "patient-profile";
          };
      };
    };

  function hideProfiles(){
    var profiles = document.getElementsByClassName("patient-profile");
    var arrayLength = profiles.length;
    for (var i = 0; i < arrayLength; i++) {
        profiles[i].className = "patient-profile profile-hidden";
    };
  };

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

  function main(){
    patientListListen();
    upcomingButton.addEventListener("click", toggleButtons);
    pastButton.addEventListener("click", toggleButtons);
    greetingBtnListen()
  }


  main()
})();



