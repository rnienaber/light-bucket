var loadImageData = function () {
    var url = document.URL;
    var path = url.match(/\/\d{4}\/\d{2}\/\w*/g);
    if(path == null)
		return;

	url = path[0] + '/metadata'
	var success = function (data) {
        applyImageData(data);
        var $gallery = $('#gallery');
        $gallery.imagesLoaded(function () {
            $gallery.masonry({itemSelector: '.box'});
        });
    };
	
	$.get(url, success)
	
};

var applyImageData = function (data) {
    $('.photo-box').each(function () {
        var box = $(this);
        var img = box.find('img').attr('src').match(/\d{4}\/\d{2}\/\w\S+/g)[0];

        var date = new Date(data[img]['date']);
        box.find(".date").text(getDateForDisplay(date));
        box.find(".title").text(data[img]['title']);
        box.find(".comment").text(data[img]['comment']);
        box.find(".subject").text(data[img]['subject']);
        box.find(".keywords").text(data[img]['keywords']);

        var person_in_image = data[img]['person_in_image'];
        if(person_in_image != undefined){
            var people = person_in_image.split(',');
            var peopleNames = people.join(', ');
            box.find(".person_in_image").text(peopleNames);
        }

        var latitude = data[img]['latitude'];
        var longitude = data[img]['longitude'];

        if(latitude && longitude){
            var anchor = box.find(".geotag");
            anchor.attr('href', "https://maps.google.co.uk/maps?q="+latitude+","+longitude);
            box.find(".geotag").show();
        }else{
            box.find(".geotag").hide();
        }

    });

    $('.photo-edit-box').each(function () {
            var box = $(this);
            var img = box.find('img').attr('src').match(/\d{4}\/\d{2}\/\w\S+/g)[0];

            box.find(".title").val(data[img]['title']);
            box.find(".comment").text(data[img]['comment']);
            box.find(".subject").val(data[img]['subject']);
            box.find(".keywords").val(data[img]['keywords']);
            box.find(".latitude").val(data[img]['latitude']);
            box.find(".longitude").val(data[img]['longitude']);
            box.find(".person_in_image").val(data[img]['person_in_image']);
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
	
    var name = month[date.getMonth()];
    return date.getDate() + result + " "+name+"  at "+date.toISOString().substr(11, 5);
};

function update_exif(event) {
	event.preventDefault();
	var form = $(this).parents('form');
	
	$.post(form.data('update-url'), form.serialize());
	
	return false;
}

$('.photo-edit-box').ajaxStart(function() {
    $(".saving").show();
});

$('.photo-edit-box').ajaxComplete(function() {
    $(".saving").hide();
});



$(document).ready(function () {
    loadImageData();
    var $gallery = $('#gallery');
    $gallery.imagesLoaded(function () {
        $gallery.masonry({itemSelector: '.box'});
    });
    $(".fancybox").fancybox({helpers: {title: {type: 'inside'}}});
	
	$(".update-exif input:submit").click(update_exif);
	
});


var month = new Array();
    month[0]="Jan";
    month[1]="Feb";
    month[2]="Mar";
    month[3]="Apr";
    month[4]="May";
    month[5]="June";
    month[6]="July";
    month[7]="Aug";
    month[8]="Sept";
    month[9]="Oct";
    month[10]="Nov";
    month[11]="Dec";

//$gallery.imagesLoaded(function(){
//    $gallery.masonry({
//    itemSelector : '.box'
////        columnWidth : 240  // 5 columns
////        columnWidth: 300 // 4 columns
////        columnWidth: 400 // 3 columns
//  });
//});