
var interventions = {

    /**
     * Parse and return the last value from a comma-delimited string
     * @param {string}
     */
    last_term: function(str) {
      var terms = str.split(',');
      return terms[terms.length - 1].trim();
    },

    /**
     * Convert django-autocomplete-light response into the format
     * jquery-ui expects.
     * @param data
     */
    data_for_jqui: function(data) {
      return $.map(data.results, function(value, key) {
          return {
              label: value.text,
              value: value.text,
              id: value.id
          };
        });
    },

    /**
     * Update a comma-separated list text input with the selected value
     * @param text - input element
     * @param value - newly selected value
     */
    multival_select: function(input, value) {
      // store values as a list on the input data
      if (input.data('value') == undefined) {
        // initialize as empty list if not set
        input.data('value', []);
      }
      // retrieve the current list of values and add the new item
      var val_list = input.data('value');
      val_list.push(value);
      // display comma separated list and store the updated list
      input.val(val_list.join(', ') + ', ');
      input.data('value', val_list)
    },


    /**
     *  Annotation viewer method, for customizing marginalia display.
     * Only handles annotation text field display.
     * @param annotation
     */
   viewer: function(annotation) {
      // default behavior
      if (annotation.text) {
        return annotator.util.escapeHtml(annotation.text);
      } else {
        // override default "no comment" to indicate this is a non-verbal
        // annotation
        return "<i>(non-verbal annotation)</i>";
      }
    },

    /**
     * Generate and return an annotator editor extension based on the
     * specified set of fields.
     * @param confs
     */
    getEditorExtension: function(confs) {

      return function editorExtension(editor) {
          // update built-in annotation text field so label and placeholders
          // make sense for how it is being used in this project
          // TODO: could these overrides be included in the config?
          editor.fields[0].label = 'Annotation Text';
          // editor inputs have already been generated at this point
          var text_input = editor.element.find('textarea').first();
          // replace default placeholder text ('Comments...')
          text_input.attr('placeholder', 'Transcription of annotation text, if any');
          // add a label
          text_input.before('<label class="field-label">Text</label>');

          // for each item in the config, add a new annotator field
          // and configure appropriate load/save methods
          $.each(confs, function(index, config) {
            // update config with default field type
            config = $.extend({'type': 'input'}, config);

            // create new annotation editor field based on the config
            var field = editor.addField({
              // set input name based on field name
              id: 'annotator-' + config.name,
              // This is properly *placeholder*, so setting is as such
              // using label as fallback
              label: config.placeholder ? config.placeholder : config.label,
              type: config.type,
              // load the field for display when the editor is rendered
              load: function(field, annotation) {
                  // determine value to set in the input for this field;
                  // must be set to something to avoid carrying over
                  // values from other annotation instances
                  var display_val = '',
                    $input = $(field).find(config.type);

                  // retrieve field value from the annotation object
                  if (annotation[config.name] || annotation[config.name == 0]) {
                      // store the value on input element data
                      $input.data('value', annotation[config.name]);
                      // populate input value the annotation data
                      display_val = annotation[config.name];
                      // convert to comma-delimited if list is configured
                      if (config.list) {
                        display_val = display_val.join(', ') + ', ';
                      }
                  }
                  // set the input value
                  $input.val(display_val);
              },
              submit: function(field, annotation) {
                var $input = $(field).find(config.type);
                // send data version without worrying about display value
                annotation[config.name] = $input.data('value');
              },
              // store element config on the editor field in case we need it later
              config: config
            });

            var input = $(field).find(config.type);
            if (config.type == 'select' && config.choicesURL) {
              // For now, choices are loaded via same json data used
              // for autocomplete views
              $.getJSON(config.choicesURL, function(data) {
                console.log(data.results);
                  $.each(data.results, function(index, item) {
                   input.append($('<option>', {value: item.text, text: item.text}))
                 });
              });

              // update stored data value when the selected value changes
              input.on('change', function() {
                 input.data('value', this.value);
              });
            }

            // initialize autocomplete field if a url is configured
            if (config.autocompleteURL) {
              // find the input element for this field and configure
              // the autocomplete widget
              input.autocomplete({
                    minLength: 0,
                    // Retrieve values via ajax
                    source: function(request, response) {
                        term = interventions.last_term(request.term);
                        // autoCompleteUrl from conf function
                        $.get(config.autocompleteURL, {q: term},
                            function(data) {
                              response(interventions.data_for_jqui(data))
                            }
                        );
                    },
                    focus: function(event, ui) {
                      event.preventDefault();
                    },
                    open: function(event, ui) {
                      console.log('open');
                      // annotator purposely sets the editor at a very high z-index;
                      // set autocomplete still higher so it isn't obscured by annotator buttons
                      $('.ui-autocomplete')
                        .css('z-index', $('.annotator-editor').css('z-index') + 1);
                    },
                });

                // multi-item autocompletes need special handling to
                // add selected item to the list of existing values
                if (config.list) {
                  input.autocomplete({
                    select: function(event, ui) {
                      interventions.multival_select($(this), ui.item.value);
                      event.preventDefault();
                    }
                  });
                }

                // Trigger autocomplete start on focus
                input.bind('focus', function() {
                  $(this).autocomplete("search");
                });

            } // end config autocomplete

          });

      }
    }
};
