// initial parameters
var chapterAnimation = 0;
var animationSpeed = 6;
var extremumLeft = 0;
var extremumRight = 0;

$(document).ready(function() {
	// check if scroller is needed
	if ($('#chapter-wrapper').width() < $('#chapterList').width()) {
		// extremum positions
		extremumLeft = removePx($('#chapterList').css('margin-left'));
		// extremumRight = 20 + $('#chapterList').width() - $('#chapter-wrapper').width() - 40;
		extremumRight = -($('#chapterList').width() - $('#chapter-wrapper').width() + 20);
		
		$('#arrow-left').hover(
			function () {
				chapterAnimation = setInterval('moveLeft()', animationSpeed);
			}, 
			function () {
				clearInterval(chapterAnimation);
			}
		);
		
		$('#arrow-right').hover(
			function () {
				chapterAnimation = setInterval('moveRight()', animationSpeed);
			}, 
			function () {
				clearInterval(chapterAnimation);
			}
		);
	}
	else {
		$('#arrow-left').hide();
		$('#arrow-right').hide();
		$('#chapterList').css('margin', 'auto');
	}
});

function moveLeft() {
	if (extremumRight < removePx($('#chapterList').css('margin-left')))
		$('#chapterList').css('margin-left', '-=1px');
}

function moveRight() {
	if (extremumLeft > removePx($('#chapterList').css('margin-left')))
		$('#chapterList').css('margin-left', '+=1px');
}

// remove 'px' from positioning values
function removePx(s) {
	return parseInt(s.replace('px', ''));
}