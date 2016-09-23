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

  //add event listener on submit button
  function submitListen(){
    var submitBtn = document.getElementById('form-submit');
    submitBtn.addEventListener('click', submitForm);
  }

  //get values for each input
  function submitForm(){
    var csrftoken = getCookie('csrftoken');
    
    patient_data['csrfmiddlewaretoken'] = csrftoken;
    patient_data['doctor'] = doctor_id;
    patient_data['patient_id'] = patient_id;

    /////
    //
    delete patient_data['updated_at']
    delete patient_data['offices']
    delete patient_data['id']
    delete patient_data['primary_care_physician']
    delete patient_data['date_of_first_appointment']
    delete patient_data['ethnicity']
    delete patient_data['disable_sms_messages']
    delete patient_data['patient_photo_date']
    delete patient_data['patient_photo']
    delete patient_data['date_of_last_appointment']
    delete patient_data['social_security_number']
    delete patient_data['chart_id']
    delete patient_data['preferred_language']
    delete patient_data['race']
    delete patient_data['copay']
    ////
  
    var arrayLength = data.length;
    for (var i = 0; i < arrayLength; i++){
      var currentField = document.getElementById("patient-".concat(data[i]));
      patient_data[data[i]] = currentField.value;
    }

    $.ajax({
      type: "POST",
      url: "http://127.0.0.1:8000/signin/patient_form_submit/",
      data: patient_data,
      //success: function(data){return},
      success: function(data){window.location = exit_url},
      error: function(XMLHttpRequst, textStatus, errorThrown){
        alert("There are some errors with your input, please fix them.")
      }
    });

  };

  function main() {
    submitListen()
  }

  main();


})();