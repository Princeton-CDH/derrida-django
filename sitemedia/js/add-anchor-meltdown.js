/*
  Load Meltdown.js on appropriate fields.
    - Can also be used to specify any custom settings for Meltdown on init.
    - See https://github.com/iphands/Meltdown#options
    - Uses MutationObservers to check for added references
    NOTE: Grappelli loads a __prefix__ infixed hidden copy of inlines that interferes
    with adding Meltdown on a mutation event. Meltdown listeners are bound to
    the element which then has its id changed--causing all the right elements
    to be there but bound to the wrong element.

    The filter to avoid putting Meltdown on the hidden copy in the first place
    fixes this.
*/

// Initial configurations
$(document).ready(function() {
  // The filter avoids adding a meltdown widget to the hidden inline textarea
  var hidden = $('.meltdown-widget').filter('textarea[name*="__prefix__"]')[0]
  $('.meltdown-widget').filter('textarea[name!='+hidden.name+']').
    meltdown({openPreview: true});
  // Looking for changes to anything with that class
  var observedNodes = $('.grp-items');
  var MutationObserver = window.MutationObserver || window.WebKitMutationObserver;
  // Pass handler function to myObserver instance
  var myObserver = new MutationObserver (handler);
  var config = {childList: true}
  // Bind MutationObserver instance to any meltdown-widget types
  observedNodes.each(function() {
      myObserver.observe(this, config);
  });
  // Handler function to look at mutationRecords for .meltdown-widget
  // and then bind meltdown events to them
  function handler (mutationRecords) {
    mutationRecords.forEach(function(mutation) {
      if (mutation.type == 'childList') {
      $('.meltdown-widget').filter('textarea[name!='+hidden.name+']')
        .meltdown({openPreview: true});
      }
    });

}

});
