var loadImageData = function () {
	if (document.URL.match(/\d{4}\/\d{2}\/\w*/g) == null)
		return
	
	$.ajax({
		url: document.URL + '/metadata',
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
    var result = "";
    switch (date.getDate()) {
        case 1:
        case 21:
        case 31:
            result = 'st';
            break;
        case 2:
        case 22:
            result = 'nd';
            break;
        case 3:
        case 23:
            result = 'rd';
            break;
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