{% if edition %}
    var editionDay = {{ edition.date|date:"j" }};
    var editionMonth = {{ edition.date|date:"m" }};
    var editionYear = {{ edition.date|date:"Y" }};
{% else %}
    var editionDay = {% now "d" %};
    var editionMonth = {% now "m" %};
    var editionYear = {% now "Y" %};
{% endif %}
var firstEditionYear = 2011
var firstEditionMonth = 7
var firstEditionDay = 20


thirtyOne = [ 1, 3, 5, 7, 8, 10, 12 ];
thirty = [ 4, 6, 9, 11 ];


$(document).ready(function() {
    /* fill in years */
    for (var i = {% now "Y" %}; i > 2008; i--) {
        $('#years').append(i + '<br />');
    }
    
    
    /* fill in days */
    fillDays(editionDay, editionMonth, editionYear);
    
    
    $('#years').css('margin-top', -16 * ({% now "Y" %} - editionYear));
    if ($.browser.msie) {
        $('#months').css('margin-top', (-16 * (12 - editionMonth) - 2));
    }
    else {
        $('#months').css('margin-top', -16 * (12 - editionMonth));
    }

    /* Internet Explorer trick */
    if (navigator.appName == "Microsoft Internet Explorer" && document.getElementById('myImageFlow_images') == null)
        location.reload();
        
    /* remove bottom pad */
    $('#myImageFlow').css('height', '-=40');
});

function pad(num) {
    if (num.toString().length == 1)
        num = '0' + num;
    
    return num;
}

function yearUp() {
    if (editionYear != 2009
        && (editionYear == 2010 && editionMonth < 7) == false) {
        $('#years').animate({
            marginTop: '-=16px'
        }, 200);
        
        editionYear--;
        fillDays(editionDay, editionMonth, editionYear);
    }
}

function yearDown() {
    if (editionYear != {% now "Y" %}
        && (editionYear == {% now "Y" %} - 1 && editionMonth > {% now "m" %}) == false) {
        $('#years').animate({
            marginTop: '+=16px'
        }, 200);
        
        editionYear++;
        fillDays(editionDay, editionMonth, editionYear);
    }
}

function monthUp() {
    if (((editionMonth == 7 && editionYear == 2009) == false) /* earliest date in archive is 1-Jul-2009 */
        && editionMonth != 1) {
        $('#months').animate({
            marginTop: '-=16px'
        }, 200);
        
        editionMonth--;
        fillDays(editionDay, editionMonth, editionYear);
    }
}

function monthDown() {
    if (((editionMonth == {% now "m" %} && editionYear == {% now "Y" %}) == false)
        && editionMonth != 12) {
        $('#months').animate({
            marginTop: '+=16px'
        }, 200);
        
        editionMonth++;
        fillDays(editionDay, editionMonth, editionYear);
    }
}

function fillDays(day, month, year) {
    $('#days').empty();
    var numberOfDays = getNumberOfDays(month, year);
    
    var nowDate = false;
    if (editionMonth == {% now "m" %} &&
        editionYear == {% now "Y" %}) {
        nowDate = true;
    }

    for (var i = 1; i < numberOfDays + 1; i++) {
        if (editionYear <= firstEditionYear
            && editionMonth <= firstEditionMonth
            && i < firstEditionDay) {
            $('#days').append('<a href="http://ayna.az/' + year + '-' + pad(month) + '-' + pad(i) + '">' + i + '</a>');
        }
        
        else {
            if (nowDate && day == i) {
                $('#days').append('<a href="/' + year + '-' + pad(month) + '-' + pad(i) + '" class="current">' + i + '</a>');
            }
            else {
                $('#days').append('<a href="/' + year + '-' + pad(month) + '-' + pad(i) + '">' + i + '</a>');
            }
            
            if (nowDate && i == {% now "j" %})
                break;
        }
    }
}

function getNumberOfDays(month, year) {
    if ($.inArray(month, thirtyOne) > -1)
        return 31;
    else if ($.inArray(month, thirty) > -1)
        return 30;
    else if (year % 4 == 0)
        return 29;
    else
        return 28;
}
