$(document).ready(function(){
    var $gallery = $('#gallery');
    $gallery.imagesLoaded(function(){
        $gallery.masonry({
        itemSelector : '.box',
        columnWidth : 240  // 5 columns
//        columnWidth: 300 // 4 columns
//        columnWidth: 400 // 3 columns
      });
    });
});




