
var interventions = {

    /* annotation viewer method, for customizing marginalia display;
   only handles annotator text */
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

    editorExtension: function(editor) {
        // update main annotation text field so label and placeholders
        // make sense for how it is being used in this project
        editor.fields[0].label = 'Annotation Text';
        // editor inputs have already been generated at this point
        var text_input = editor.element.find('textarea').first();
        // replace default placeholder text ('Comments...')
        text_input.attr('placeholder', 'Transcription of annotation text, if any');
        // add a label
        text_input.before('<label class="field-label">Text</label>');

    }

};
