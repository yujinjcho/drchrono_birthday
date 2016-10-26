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
        };
      };
    };
    return cookieValue;
  };

  //add event listener on submit button
  function submitListen() {
    var submitBtn = document.getElementById('form-submit');
    submitBtn.addEventListener('click', submitForm);
  };

  //get values for each input
  function submitForm() {
    var csrftoken = getCookie('csrftoken');

    var postData = {
      'csrfmiddlewaretoken': csrftoken,
      'doctor': doctorId,
      'patient_id': patientId
    };

    var arrayLength = data.length;
    for (var i = 0; i < arrayLength; i++) {
      var currentField = document.getElementById('patient-'.concat(data[i]));
      postData[data[i]] = currentField.value;
    };

    var postUrl = document.createElement('A');
    postUrl.href = window.location.href;
    postUrl.pathname = '/signin/patient_form_submit/';

    $.ajax({
      type: 'POST',
      url: postUrl.href,
      data: postData,
      success: function(data) { document.patientForm.submit(); },
      error: function(XMLHttpRequst, textStatus, errorThrown) {
        alert('There are some errors with your input, please fix them.');
      }
    });
  };

  function main() {
    submitListen();
  };

  main();
})();
