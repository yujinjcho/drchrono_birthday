(function (){

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
  };

  function handlePatientResponse(data){
    var patientFound = document.getElementById("patient-found-alert")
    var patientNotFound = document.getElementById("patient-not-found-alert")

    if (data == null) {
      //If Patient information is NOT found
      patientNotFound.className = "alert alert-warning"
      patientFound.className = "alert alert-success patient-alert"
    }
    else {
      //If Patient information is found
      patientFound.className = "alert alert-success"
      patientNotFound.className = "alert alert-warning patient-alert"
      createPatientInfo(data);
      setAppointmentFinder(data);
    }
  };

  function createPatientInfo(data){
    var patientInfo = document.getElementById("patient-info");
    patientInfo.innerHTML = "<div id='profile-pic'></div><div id='social-security-number'></div><div id='email'></div>";
    var profilePic = document.getElementById("profile-pic");
    var socialSecurityNumber = document.getElementById('social-security-number');
    var email = document.getElementById('email');

    profilePic.innerHTML = '<img class="profile-pic" src='.concat(data.patient_photo).concat('>')
    socialSecurityNumber.innerHTML = 'SSN: '.concat(data.social_security_number);
    email.innerHTML = 'Email: '.concat(data.email);
  };

  function setAppointmentFinder(data){
    /*
    var appointmentBtn = document.getElementById('find-appointment-btn');
    appointmentBtn.setAttribute('data', data.id);
    appointmentBtn.addEventListener('click', findAppointments);
    */
    var appointmentBtn = document.getElementById('check-appointment-btn');
    var appointmentHref = appointmentBtn.getAttribute('href');
    var patientId = data.id;
    appointmentBtn.setAttribute(
      'href', 
      appointmentHref.concat('?id=').concat(patientId)
    );

  };

  function handleAppointmentResponse(data){
    if (data.count == 0) {
      return
    } else {
      //Assuming only one appointment for now
      //Think about how to handle multiple


    }

  };

  function findAppointments(e){

    var patientId = document.getElementById(e.currentTarget.id).getAttribute('data');
    var csrftoken = getCookie('csrftoken');

    $.post(
      "http://127.0.0.1:8000/signin/find_appointment/",
      {
        "patient_id": patientId,
        'csrfmiddlewaretoken': csrftoken
      },
      function(data){handleAppointmentResponse(data)}
    );

  };

  function findPatient() {

    var firstName = document.getElementById("InputFirstName")
    var lastName =document.getElementById("InputLastName")
    var dateOfBirth = document.getElementById("DateofBirth")
    var csrftoken = getCookie('csrftoken');

    $.post(
      "http://127.0.0.1:8000/signin/find_patient/",
      {
        "first_name": firstName.value,
        "last_name": lastName.value,
        "date_of_birth": dateOfBirth.value,
        'csrfmiddlewaretoken': csrftoken
      },
      function(data){handlePatientResponse(data)}
    );

  };

  function main(){
    var patientSigninBtn = document.getElementById('patient-signin-btn');
    patientSigninBtn.addEventListener('click',findPatient)
  };

  main();
})();