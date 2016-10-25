(function() {

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

  function handlePatientResponse(data) {
    var patientFound = document.getElementById('patient-found-alert');
    var patientNotFound = document.getElementById('patient-not-found-alert');

    if (data == null) {
      //If Patient information is not found
      patientNotFound.className = 'alert alert-warning';
      patientFound.className = 'alert alert-success patient-alert';
    } else {
      patientFound.className = 'alert';
      patientNotFound.className = 'alert alert-warning patient-alert';
      createPatientInfo(data);
      setAppointmentFinder(data);
    }
  };

  function createPatientInfo(data) {
    var patientInfo = document.getElementById('patient-info');
    patientInfo.innerHTML = '';

    var profilePic = document.createElement('DIV');
    profilePic.setAttribute('id', 'profile-pic');
    var profileImage = document.createElement('IMG');
    profileImage.setAttribute('class', 'profile-pic');
    profileImage.setAttribute('src', data.patient_photo);
    profilePic.appendChild(profileImage);

    patientInfo.appendChild(profilePic);
    patientInfo.appendChild(
      createPatientIdentifier('SSN', data.social_security_number)
    );
    patientInfo.appendChild(createPatientIdentifier('Email', data.email));
  };

  function createPatientIdentifier(IdType, IdValue) {
    var elem = document.createElement('DIV');
    elem.setAttribute('id', IdType.toLowerCase());
    var elemText = document.createElement('STRONG');
    elemText.innerHTML = IdType.concat(': ').concat(IdValue);
    elem.appendChild(elemText);
    return elem;
  }

  function setAppointmentFinder(data) {
    var patientId = data.id;
    var apptIdBtn = document.getElementById('appointmentId');
    apptIdBtn.value = patientId;
  };

  function findPatient() {

    var firstName = document.getElementById('InputFirstName');
    var lastName = document.getElementById('InputLastName');
    var dateOfBirth = document.getElementById('DateofBirth');
    var csrftoken = getCookie('csrftoken');

    $.post(
      'http://127.0.0.1:8000/signin/find_patient/',
      {
        'first_name': firstName.value,
        'last_name': lastName.value,
        'date_of_birth': dateOfBirth.value,
        'csrfmiddlewaretoken': csrftoken
      },
      function(data) {handlePatientResponse(data);}
    );
  };

  function main() {
    var patientSigninBtn = document.getElementById('patient-signin-btn');
    patientSigninBtn.addEventListener('click', findPatient);
  };

  main();
})();
