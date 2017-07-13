

/**
 * Return an intervention plugin with render and editor extension
 * methods based on the configuration passed in.
 */
function annotatorInterventions(confs) {

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
     * Retrieve an annotation field value and convert for display.
     * Returns empty string if no value is set, converts to comma
     * delimited if multiple is true.
     * @param annotation
     * @param field_name
     * @param multiple (defaults to false)
     * @param value (default value for field)
     */
    field_display_value: function(annotation, field_name, multiple=false, value=false) {
      var display_val = '';
      if (value) {
        display_val = value;
      }
       if (annotation[field_name] || annotation[field_name] == 0) {
          display_val = annotation[field_name];
          // convert to comma-delimited if list is configured
          if (multiple) {
            display_val = display_val.join(', ') + ', ';
          }
        }
        return display_val;
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

    renderExtension: function(annotation, item) {
      $.each(confs, function(index, config) {
        // skip tags; tag display already handled by marginalia
        if (config.name == 'tags') {
          return;
        }
        var div, span, display_val;
        // find or create div to display the field
        div = item.find('.annotator-' + config.name);
        // if it does not exist, create it
        if (div.length == 0) {
          div = $('<div/>').addClass('annotator-' + config.name);
          // add the label for this field
          div.append($('<label/>').html(config.label));
          div.append($('<span/>'));
          // insert before tag/footer
          div.insertBefore(item.find('.annotator-tags'));
        }

        span = div.find('span');

        // if field is present on the annotation, show it
        display_val = interventions.field_display_value(annotation,
          config.name, config.list);
        if (display_val) {
          span.html(display_val);
          div.show()
        } else {
          div.hide();
        }

      });

      return item;
    },

    /**
     * Generate and return an annotator editor extension based on the
     * specified set of fields.
     * @param confs
     */
     editorExtension: function(editor) {
          // update built-in annotation text field so label and placeholders
          // make sense for how it is being used in this project
          // TODO: could these overrides be included in the config?
          editor.fields[0].label = 'Annotation Text';
          // editor inputs have already been generated at this point
          var text_input = editor.element.find('textarea').first();
          // replace default placeholder text ('Comments...')
          text_input.attr('placeholder', 'Transcription of annotation text, if any');
          // add a label
          text_input.before('<label>Text</label>');

          // for each item in the config, add a new annotator field
          // and configure appropriate load/save methods
          $.each(confs, function(index, config) {
            // update config with default field type
            config = $.extend({'type': 'input'}, config);
            // create new annotation editor field based on the config
            var field = editor.addField({
              // set input name based on field name
              id: 'annotator-' + config.name,
              // set input placeholder, using label as fallback
              label: config.placeholder ? config.placeholder : config.label,
              type: config.type,
              // load the field for display when the editor is rendered
              load: function(field, annotation) {
                  // determine value to set in the input for this field;
                  // must be set to something to avoid carrying over
                  // values from other annotation instances
                  var $input = $(field).find(config.type);

                  // store the field value in native form on input element data
                  $input.data('value', annotation[config.name]);

                  // set the input value
                  $input.val(interventions.field_display_value(annotation,
                    config.name, config.list, config.value));
              },
              submit: function(field, annotation) {
                // get the value from the form input and set it on the
                // annotation object
                var $input = $(field).find(config.type);

                // multi-valued fields, selects, and autocompletes store
                // values as a list in the data attribute
                if (config.list || config.type == 'select' || config.autocompleteURL) {
                   // send data version without worrying about display value
                  annotation[config.name] = $input.data('value');
                } else {
                  // text fields do not use data attribute for storage
                  annotation[config.name] = $input.val();
                }
              },
              // store element config on the editor field in case we need it later
              config: config
            });

            var input = $(field).find(config.type);
            // add a label for the new input
            input.before($('<label/>').html(config.label));

            // load select choices if configured
            if (config.type == 'select') {
              // check first for a list of choices passed in
              if (config.choices) {
                $.each(config.choices, function(index, item) {
                   input.append($('<option>', {value: item, text: item}))
                 });
              // otherwise, load choices via url
              } else if (config.choicesURL) {
                // For now, choices are loaded via same json data used
                // for autocomplete views
                $.getJSON(config.choicesURL, function(data) {
                    $.each(data.results, function(index, item) {
                     input.append($('<option>', {value: item.text, text: item.text}))
                   });
                });
              }

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
  };

  return interventions;
}
