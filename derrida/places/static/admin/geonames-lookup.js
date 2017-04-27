$(document).on('select2:select', function(evt) {
    var data = evt.params.data;
    // update link display and target
    $('#geonames_uri').text(data.id).attr('href', data.id);
    // set latitude and longitude values from geonames data
    $('input[name="latitude"]').val(data.lat);
    $('input[name="longitude"]').val(data.lng);
    // update map based on new coordinates
    update_map();
});

var map, marker;

function init_map() {
    // initialize the map for the first time
    if ($('#geonames_map').length) {
        map = L.map('geonames_map');
        L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
            attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
            maxZoom: 18,
            id: 'mapbox.streets',
            // get mapbox access token; passed in via hidden form field
            accessToken: $('input[name="mapbox_token"]').val(),
        }).addTo(map);
        // set map to display current coordinates
        update_map();
    }
}

function update_map() {
    // grab current lat, long coordinates from the form
    var long = $('input[name="longitude"]').val(),
        lat =  $('input[name="latitude"]').val();
    // display map if coordinates are set
    if (lat && long && !(lat == 0.0 && long == 0.0)) {
        $('#geonames_map').show();
        map.setView([lat, long], 5);
        if (typeof marker !== 'undefined') {
            map.removeLayer(marker);
        }
        marker = L.marker([lat, long]).addTo(map);
    } else {        // otherwise, hide it
        $('#geonames_map').hide();
    }
}


$(document).ready(function() {
    init_map();
});