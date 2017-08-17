$(document).on('select2:select', function(evt) {
    if ($(evt.target).hasClass('viaf-lookup')) {
        console.log('viaf selected!');
        console.log(evt);
        // when a VIAF id is selected, update viaf link
        var data = evt.params.data;
        $('#viaf_uri').attr('href', data.id).text(data.id);
        // Clear birth and death so they will be set from VIAF record on save
        $('input[name="birth"]').val('');
        $('input[name="death"]').val('');
    }
});

$(document).ready(function() {
        console.log('ready!');
    // add a way to clear selected viaf id
    var span = $('<span>').attr('class', 'grp-tools');
    var del = $('<a>')
        .attr('id', 'viaf_id-delete')
        .attr('class', 'grp-icon grp-delete-handler')
        .attr('title', 'Clear VIAF ID');
    del.on('click', function() {
        $('select[name="viaf_id"]').select2().val(null).trigger("change");
        $('#viaf_uri').attr('href', '').text('');
        $('input[name="birth"]').val('');
        $('input[name="death"]').val('');
    });
    span.append(del)
    span.insertAfter($('#viaf_uri'));
    if ($('#viaf_uri').text() == '') {
        del.hide();
    }
});
