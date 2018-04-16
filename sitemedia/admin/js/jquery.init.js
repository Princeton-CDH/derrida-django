// override the init.js provided by django-autocomplete-light
// to make sure jQuery is available for select2
// (seems to be a grappelli compatibility issue)

var django = django || {};

var jQuery = jQuery || django.jQuery;
if (!django.jQuery) {
    django.jQuery = jQuery;
}
var $ = jQuery;

var yl = yl || {};
yl.jQuery = django.jQuery

// this file also prevents django.jQuery.noConflict
// there's got to be a better way ...var yl = yl || {};




