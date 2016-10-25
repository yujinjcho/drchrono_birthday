(function (){

  function addAllergyListen() {
    var addAllergyBtn = document.getElementById('add-allergy');
    addAllergyBtn.addEventListener('click', addAllergy)
  };

  function addAllergy(){
    var allergiesNone = document.getElementById('no-allergies');
    if (allergiesNone) {
      allergiesNone.className = "no-allergies-hide";
    }

    var reactionsAdd = document.getElementById('reaction-to-add');
    var notesAdd = document.getElementById('notes-to-add');
    var allergyContainer = document.getElementById('existing-allergy-container');
    var allergyItem = document.createElement("div");

    allergyItem.className = "allergy-item";

    reaction_output = createReaction(reactionsAdd);
    notes_output = createNote(notesAdd)

    allergyItem.appendChild(createStatus());
    allergyItem.appendChild(reaction_output[0]);
    allergyItem.appendChild(notes_output[0]);

    allergyContainer.appendChild(allergyItem);
    createNewAllergy(patient_id, reaction_output[1], notes_output[1])
  }

  function createNote(notes){
    var notesRow = document.createElement("div");
    var notesLabel = document.createElement("label");
    var notesInputContainer = document.createElement("div");

    notesRow.className = 'form-group row';
    notesLabel.className = "col-xs-4 col-form-label";
    notesLabel.innerHTML = 'Notes';
    notesInputContainer.className = "col-xs-8";
    notesInputContainer.innerHTML = "<input class='form-control' type='text' value='".concat(notes.value).concat("' id='test' disabled>");
    notesVal = notes.value;

    notesRow.appendChild(notesLabel);
    notesRow.appendChild(notesInputContainer);
    notes.value = '';
    return [notesRow, notesVal]
  }

  function createStatus(){
    var statusRow = document.createElement("div");
    var statusLabel = document.createElement("label");
    var statusInputContainer = document.createElement("div");

    statusRow.className = "form-group row";
    statusLabel.className = "col-xs-4 col-form-label";
    statusLabel.innerHTML = 'Status';
    statusInputContainer.className = "col-xs-8";
    statusInputContainer.innerHTML = '<select class="form-control"><option value="active" selected>active</option><option value="Inactive">inactive</option></select>';

    statusRow.appendChild(statusLabel);
    statusRow.appendChild(statusInputContainer);

    return statusRow
  }

  function createReaction(reactionReason){

    var reactionIndex = [reactionReason.selectedIndex];
    var reactionSelect = reactionReason.options[reactionIndex].value;

    if (reactionSelect == "") {
      throw "must select a reaction"
    }

    var reactionRow = document.createElement("div");
    var reactionLabel = document.createElement("label");
    var reactionInputContainer = document.createElement("div");
    reactionRow.className = 'form-group row';
    reactionLabel.className = 'col-xs-4 col-form-label';
    reactionLabel.innerHTML = 'Reaction';
    reactionInputContainer.className = 'col-xs-8';
    reactionInputContainer.innerHTML = "<input class='form-control' type='text' value='".concat(reactionSelect).concat("' id='test' disabled>");

    reactionRow.appendChild(reactionLabel);
    reactionRow.appendChild(reactionInputContainer);

    return [reactionRow, reactionSelect]
  }

  function createNewAllergy(patient_id, reaction, notes){
    newAllergy = {
      'patient_id':patient_id,
      'reaction':reaction,
      'notes':notes
    }
    newAllergies.push(newAllergy);
  }

  function updateAllergyListen(){
    var exitBtn = document.getElementById('exit-checkin');
    exitBtn.addEventListener("click", updateAllergies);
  };

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

  function updateAllergies(){

    var csrftoken = getCookie('csrftoken');
    var toSetInactive = getAllergiesSetInactive();

    postData = {'csrfmiddlewaretoken': csrftoken};
    postData['new_allergies'] = JSON.stringify(newAllergies);
    postData['set_inactive'] = toSetInactive;
    postData['appointment_id'] = appointmentId;

    $.ajax({
      type: "POST",
      url: "http://127.0.0.1:8000/signin/update_allergies/",
      data: postData,
      success: function(data){window.location = exit_url},
      error: function(XMLHttpRequst, textStatus, errorThrown){
        alert("There are some errors with your input, please fix them.")
      }
    });
  }

  function getAllergiesSetInactive(){
    var toUpdate = [];
    var arrayLength = existingAllergies.length;

    for (var i = 0; i < arrayLength; i++) {
      var currentAllergy = document.getElementById("allergy-".concat(existingAllergies[i]['id']));
      var status = currentAllergy.options[currentAllergy.selectedIndex].value;
      if (status == "inactive") {
        toUpdate.push(existingAllergies[i]['id'].toString())
      }
    };

    return toUpdate
  }

  function main() {
    addAllergyListen();
    updateAllergyListen();
  };

  main();

})();



