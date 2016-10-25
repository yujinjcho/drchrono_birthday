(function() {

  function addAllergyListen() {
    var addAllergyBtn = document.getElementById('add-allergy');
    addAllergyBtn.addEventListener('click', addAllergy);
  };

  function addAllergy() {
    var allergiesNone = document.getElementById('no-allergies');
    if (allergiesNone) {
      allergiesNone.className = 'no-allergies-hide';
    }

    var reactionsAdd = document.getElementById('reaction-to-add');
    var notesAdd = document.getElementById('notes-to-add');
    var allergyContainer = document.getElementById(
      'existing-allergy-container'
    );
    var allergyItem = document.createElement('div');

    allergyItem.className = 'allergy-item';

    reactionOutput = createReaction(reactionsAdd);
    notesOutput = createNote(notesAdd);

    allergyItem.appendChild(createStatus());
    allergyItem.appendChild(reactionOutput[0]);
    allergyItem.appendChild(notesOutput[0]);

    allergyContainer.appendChild(allergyItem);
    createNewAllergy(patientId, reactionOutput[1], notesOutput[1]);
  };

  function createNote(notes) {
    var notesRow = document.createElement('div');
    var notesLabel = document.createElement('label');
    var notesInputContainer = document.createElement('div');

    notesRow.className = 'form-group row';
    notesLabel.className = 'col-xs-4 col-form-label';
    notesLabel.innerHTML = 'Notes';
    notesInputContainer.className = 'col-xs-8';

    notesInputContainer.appendChild(
      createInput('form-control', 'test', 'text', notes.value, true)
    );

    notesVal = notes.value;
    notesRow.appendChild(notesLabel);
    notesRow.appendChild(notesInputContainer);
    notes.value = '';
    return [notesRow, notesVal];
  };

  function createInput(className, idName, type, val, disabled) {
    var inputElem = document.createElement('INPUT');
    inputElem.setAttribute('class', className);
    inputElem.setAttribute('id', idName);
    inputElem.setAttribute('type', type);
    inputElem.value = val;
    inputElem.disabled = disabled;

    return inputElem;
  };

  function createStatus() {
    var statusRow = document.createElement('div');
    var statusLabel = document.createElement('label');
    var statusInputContainer = document.createElement('div');

    statusRow.className = 'form-group row';
    statusLabel.className = 'col-xs-4 col-form-label';
    statusLabel.innerHTML = 'Status';
    statusInputContainer.className = 'col-xs-8';
    statusInputContainer.appendChild(createStatusDropdown());

    statusRow.appendChild(statusLabel);
    statusRow.appendChild(statusInputContainer);

    return statusRow;
  };

  function createStatusDropdown() {
    var selectElem = document.createElement('SELECT');
    selectElem.setAttribute('class', 'form-control');
    selectElem.appendChild(createOption('active'));
    selectElem.appendChild(createOption('inactive'));

    return selectElem;
  };

  function createOption(text) {
    optionElem = document.createElement('OPTION');
    optionElem.value = text;
    optionElem.innerHTML = text;

    if (text === 'active') {
      optionElem.selected = true;
    };

    return optionElem;
  };

  function createReaction(reactionReason) {

    var reactionIndex = [reactionReason.selectedIndex];
    var reactionSelect = reactionReason.options[reactionIndex].value;

    if (reactionSelect == '') {
      throw 'must select a reaction';
    }

    var reactionRow = document.createElement('div');
    var reactionLabel = document.createElement('label');
    var reactionInputContainer = document.createElement('div');
    reactionRow.className = 'form-group row';
    reactionLabel.className = 'col-xs-4 col-form-label';
    reactionLabel.innerHTML = 'Reaction';
    reactionInputContainer.className = 'col-xs-8';
    reactionInputContainer.appendChild(
      createInput('form-control', 'test', 'text', reactionSelect, true)
    );

    reactionRow.appendChild(reactionLabel);
    reactionRow.appendChild(reactionInputContainer);

    return [reactionRow, reactionSelect];
  }

  function createNewAllergy(patientId, reaction, notes) {
    newAllergy = {
      'patient_id': patientId,
      'reaction': reaction,
      'notes': notes
    };
    newAllergies.push(newAllergy);
  };

  function updateAllergyListen() {
    var exitBtn = document.getElementById('exit-checkin');
    exitBtn.addEventListener('click', updateAllergies);
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

  function updateAllergies() {

    var csrftoken = getCookie('csrftoken');
    var toSetInactive = getAllergiesSetInactive();

    postData = {'csrfmiddlewaretoken': csrftoken};
    postData.new_allergies = JSON.stringify(newAllergies);
    postData.set_inactive = toSetInactive;
    postData.appointment_id = appointmentId;

    $.ajax({
      type: 'POST',
      url: 'http://127.0.0.1:8000/signin/update_allergies/',
      data: postData,
      success: function(data) { window.location = exitUrl; },
      error: function(XMLHttpRequst, textStatus, errorThrown) {
        alert('There are some errors with your input, please fix them.');
      }
    });
  };

  function getAllergiesSetInactive() {
    var toUpdate = [];
    var arrayLength = existingAllergies.length;

    for (var i = 0; i < arrayLength; i++) {
      var currentAllergy = document.getElementById(
        'allergy-'.concat(existingAllergies[i].id)
      );
      var status = currentAllergy.options[currentAllergy.selectedIndex].value;
      if (status == 'inactive') {
        toUpdate.push(existingAllergies[i].id.toString());
      }
    };

    return toUpdate;
  }

  function main() {
    addAllergyListen();
    updateAllergyListen();
  };

  main();
})();
