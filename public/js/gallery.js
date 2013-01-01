var loadImageData = function () {
    var url = document.URL;
    var path = url.match(/\d{4}\/\d{2}\/\w+/g)[0];
    console.log(path);

    $.ajax({
        url: '/api/photo_metadata?path=' + path,
        success: function (data) {
            applyImageData(data);
            var $gallery = $('#gallery');
            $gallery.imagesLoaded(function () {
                $gallery.masonry({itemSelector: '.box'});
            });
        }
    });
};

var applyImageData = function (data) {
    $('.photo-box').each(function () {
        var box = $(this);
        var img = box.find('img').attr('src').match(/\d{4}\/\d{2}\/\w\S+/g)[0];

        var date = new Date(data[img]['date']);
        box.find(".date").text(getDateForDisplay(date));
    });
};

var getDateForDisplay = function (date) {
    var result = "th";
    switch (date.getDate()) {
        case 1:
        case 21:
        case 31:
            result = 'st';
        case 2:
        case 22:
            result = 'nd';
        case 3:
        case 23:
            result = 'rd';
        default:
            result = 'th';
    }
    return date.getDate() + result + " at "+date.toTimeString().substr(0,5);
};

$(document).ready(function () {
    loadImageData();
    var $gallery = $('#gallery');
    $gallery.imagesLoaded(function () {
        $gallery.masonry({itemSelector: '.box'});
    });
    $(".fancybox").fancybox({helpers: {title: {type: 'inside'}}});
});













//$gallery.imagesLoaded(function(){
//    $gallery.masonry({
//    itemSelector : '.box'
////        columnWidth : 240  // 5 columns
////        columnWidth: 300 // 4 columns
////        columnWidth: 400 // 3 columns
//  });
//});



