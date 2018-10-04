/*
Javascript snippet to toggle the Canvas and Intervention autocompletes
sanely based on the presence of a digital edition for a selected Instance (or
the instance being edited in the case of the Reference Inline)
*/



/*
Toggle on or off based on the presence of an Instance with a digtial edition,
either in the selector on the Reference change_form or inline when editing
an Instance
*/
function toggleReferenceAutocompletes() {
  var instancePksArray = []
  var jsonString = $('.field-instance_ids_with_digital_editions .readonly').text();
  if (jsonString) {
    instancePksArray = JSON.parse(jsonString);
  }

  // Flag to see if a digital edition is set on Instance change_form
  var digitalEdFlag = $('#id_digital_edition option:selected').val();

  // Flag to see if an instance is selected on Reference change_form
  var selectedInstancePk = $('#id_instance').val()
  // Flag to see if instance on Reference change_form is in array of
  // Instances with digital editions
  var pkInArray = instancePksArray.indexOf(parseInt(selectedInstancePk));

  /*
  Check if:
  1) There is an instance selected for Reference change_form and if it is
  on the list of those with digital editions.
  2) There is  a digital edition set on the Instance change_form.

  If either are not true, disable the selectors
  */
      // value of #id_instance is not in the list of digital editions or
      // #id_instance doesn't exist
  if ((pkInArray == -1 && $('#id_instance').val() != undefined) ||
      // #digital_edition select is either not set or doesn't exist
      (digitalEdFlag == "" && digitalEdFlag != undefined)) {
    $('select[id*="canvases"]').attr('disabled', true);
    $('select[id*="interventions"]').attr('disabled', true);

  } else {
    /*
    Enable autocompletes if either #id_instance on Reference change form,
    or the Instance being viewed reflect an instance with a digital edition.

    For the change form, use the parsed JSON from get_autocomplete_instances
    read-only field.
    */
    // if #id_instance exists and is in the array or check or
    // if #digital_edition exists and is set
    if (pkInArray != -1 || (digitalEdFlag != "" && digitalEdFlag != undefined)) {
      $('select[id*="canvases"]').removeAttr('disabled', true);
      $('select[id*="interventions"]').removeAttr('disabled', true);
    }
  }
}

$(document).ready(function() {
  // bind function once on page load
  toggleReferenceAutocompletes();
  // bind to the change event on #id_instance for the Reference change_form
  $("#id_instance").change(function() {
    toggleReferenceAutocompletes();
  });
  // Do NOT bind on page load for Instance change_form, since autocompletes need
  // a saved instance to be accruate.
});
