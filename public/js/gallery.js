$(document).ready(function(){
    var $gallery = $('#gallery');
    $gallery.imagesLoaded(function(){
        $gallery.masonry({
        itemSelector : '.box',
        columnWidth : 260
      });
    });

});




