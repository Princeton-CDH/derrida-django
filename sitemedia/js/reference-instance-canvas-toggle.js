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
  var jsonString = $('.get_autocomplete_instances div div .grp-readonly').text();
  if (jsonString) {
    instancePksArray = JSON.parse(
      $('.get_autocomplete_instances div div .grp-readonly').text()
    );
  }
  /*
  Check if there is an instance selected for Reference change_form or a
  digital edition chosen on the Instance change_form, and if not, disable
  the autcompletes.
  */
  if ($('#id_instance option:selected').val() == "" ||
    $('#id_digital_edition option:selected').val() == "") {
    $('select[id*="canvases"]').attr('disabled', true);
    $('select[id*="interventions"]').attr('disabled', true);

  } else {
    /*
    Enable autocompletes if either #id_instance on Reference change form,
    or the Instance being viewed reflect an instance with a digital edition.

    For the change form, use the parsed JSON from get_autocomplete_instances
    read-only field.
    */
    var digitalEdFlag = $('#id_digital_edition option:selected').val();
    var pkInArray = instancePksArray.indexOf($('#id_instance').val());
    if (pkInArray == 0 || (digitalEdFlag != "" && digitalEdFlag != undefined)) {
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
  })
  // bind to the change event on #digital_edition for the Instance change_form
  $("#id_digital_edition").change(function() {
    toggleReferenceAutocompletes();
  })
});
