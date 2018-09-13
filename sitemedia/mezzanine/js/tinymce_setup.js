(function($) {
    'use strict';

    // Map Django language codes to valid TinyMCE language codes.
    // There's an entry for every TinyMCE language that exists,
    // so if a Django language code isn't here, we can default to en.

    var language_codes = {
        'ar': 'ar',
        'ca': 'ca',
        'cs': 'cs',
        'da': 'da',
        'de': 'de',
        'es': 'es',
        'et': 'et',
        'fa': 'fa',
        'fa-ir': 'fa_IR',
        'fi': 'fi',
        'fr': 'fr_FR',
        'hr-hr': 'hr',
        'hu': 'hu_HU',
        'id-id': 'id',
        'is-is': 'is_IS',
        'it': 'it',
        'ja': 'ja',
        'ko': 'ko_KR',
        'lv': 'lv',
        'nb': 'nb_NO',
        'nl': 'nl',
        'pl': 'pl',
        'pt-br': 'pt_BR',
        'pt-pt': 'pt_PT',
        'ru': 'ru',
        'sk': 'sk',
        'sr': 'sr',
        'sv': 'sv_SE',
        'tr': 'tr',
        'uk': 'uk_UA',
        'vi': 'vi',
        'zh-cn': 'zh_CN',
        'zh-tw': 'zh_TW',
        'zh-hant': 'zh_TW',
        'zh-hans': 'zh_CN'
    };

    function custom_file_browser(field_name, url, type, win) {
        tinyMCE.activeEditor.windowManager.open({
            title: 'Select ' + type + ' to insert',
            file: window.__filebrowser_url + '?pop=5&type=' + type,
            width: 800,
            height: 500,
            resizable: 'yes',
            scrollbars: 'yes',
            inline: 'yes',
            close_previous: 'no'
        }, {
            window: win,
            input: field_name
        });
        return false;
    }

    // Stylesheets are being compiled using django-compressor
    // (https://github.com/django-compressor/django-compressor),
    // which generates a single .css file on page load and inserts it
    // into the page using a django template tag. We ensure this happens
    // by including the "compress" tag on the edit form template
    // (templates/admin/change_form.html).
    function get_editor_stylesheet() {
        // We don't know what the name of the compressed stylesheet will be,
        // but we know it will have "style" somewhere in the href attribute,
        // because the base .scss file is sitemedia/scss/style.scss.
        var mainSheet;
        $.each(document.styleSheets, function(_, sheet) {
            if (sheet.href && sheet.href.match(/style\.(.*)\.css/)) {
                mainSheet = sheet;
            }
        })
        // Use the default tinyMCE style if we couldn't find the site styles
        return mainSheet ? mainSheet.href : window.__tinymce_css;
    }

    // get the main stylesheet so that we can apply it to tinyMCE only
    var editor_css = get_editor_stylesheet();

    var tinymce_config = {
        height: '500px',
        language: language_codes[window.__language_code] || 'en',
        plugins: [
            "autolink lists advlist link image charmap print preview anchor",
            "searchreplace visualblocks code fullscreen",
            "insertdatetime media contextmenu paste"
        ],
        link_list: window.__link_list_url,
        relative_urls: false,
        browser_spellcheck: true,
        convert_urls: false,
        menubar: false,
        statusbar: false,
        toolbar: ("undo redo | styleselect | bold italic | " +
                  "bullist numlist | credits creditsection | link image | " +
                  "fullscreen code"),
        file_browser_callback: custom_file_browser,
        content_css: editor_css,
        body_id: 'editor', // necessary to view content page styles
        style_formats: [
          { title: 'h2', block: 'h2' },
          { title: 'h3', block: 'h3' },
          { title: 'p', block: 'p' },
          { title: 'footnotes', block: 'p', classes : 'footnote' },
          { title: 'blockquote', block: 'blockquote' },
          { title: 'Credits (role)', block: 'li', classes: 'credits__role'},
          { title: 'Credits (name)', block: 'li', classes: 'credits__name'},
        ],
        advlist_bullet_styles: "default",
        advlist_number_styles: "default",
        setup: function(editor) {
            function insertCreditSection() {
                editor.insertContent('<section class="credits"><ul class="credits__group"><li class="credits__role">Role</li><li class="credits__name">Name</li></ul></section>')
            }
            function insertCredit() {
                editor.insertContent('<ul class="credits__group"><li class="credits__role">Role</li><li class="credits__name">Name</li></ul>');
            }
            editor.addButton('creditsection', {
                text: 'Credit Section',
                tooltip: 'Create the credits display area.',
                onclick: insertCreditSection
            });
            editor.addButton('credits', {
                text: 'Credits',
                tooltip: 'Insert a preformatted credit with a role & name.',
                onclick: insertCredit
            });
        },
        valid_elements: "*[*]"  // Don't strip anything since this is handled by bleach.
    };

    function initialise_richtext_fields($elements) {
        if ($elements && typeof tinyMCE != 'undefined') {
            $elements.tinymce(tinymce_config);
        }
    }

    // Register a handler for Django's formset:added event, to initialise
    // any rich text fields in dynamically added inline forms.
    $(document).on('formset:added', function(e, $row) {
        initialise_richtext_fields($row.find('textarea.mceEditor'));
    });

    // Initialise all existing editor fields, except those with an id
    // containing the string "__prefix__". Those elements are part of the
    // hidden template inline rows used by Django's dynamic inlines, and they
    // shouldn't be initialised as editors.
    $(document).ready(function() {
        initialise_richtext_fields($('textarea.mceEditor').filter(function() {
            return (this.id || '').indexOf('__prefix__') === -1;
        }));
    });

})(window.django ? django.jQuery : jQuery);
