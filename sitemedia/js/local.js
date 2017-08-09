$(document).ready(function(){
    var $ribbon = $('.ribbon');
    if ($ribbon) {
        var faded = sessionStorage.getItem('fade-test-banner', true);
        if (! faded) {
            $('.ribbon-box').removeClass('fade');
        }
        $ribbon.on('click',function(){
            $('.ribbon-box').addClass('fade');
            sessionStorage.setItem('fade-test-banner', true);
        });
    }
});
