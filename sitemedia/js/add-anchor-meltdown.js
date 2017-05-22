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

// Initial configuration of meltdown is contained in this function
// Changing any settings here will affect all instances of the widget
function addMeltDown() {
  $('.meltdown-widget').not('.grp-empty-form .meltdown-widget')
    .meltdown({openPreview: true});
}

$(document).ready(function() {
  // Add meltdown to any pre-existing anchor text fields on reference inlines
  addMeltDown()
  // Initialize the MutationObserver crossbrowser compatible
  var MutationObserver = window.MutationObserver || window.WebKitMutationObserver;
  // Handler function to look at mutationRecords for .meltdown-widget
  // and then bind meltdown events to them
  function handler (mutationRecords) {
    mutationRecords.forEach(function(mutation) {
      if (mutation.type == 'childList') {
        addMeltDown();
      }
    });
  }
  // Pass handler function to myObserver instance
  var myObserver = new MutationObserver (handler);
  // Bind MutationObserver instance to any meltdown-widget types
  $('.grp-items').each(function() {
      myObserver.observe(this, {childList: true});
  });

});
