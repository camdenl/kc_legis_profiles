var isOpera = !!window.opera || navigator.userAgent.indexOf(' OPR/') >= 0;
// Opera 8.0+ (UA detection to detect Blink/v8-powered Opera)
var isFirefox = typeof InstallTrigger !== 'undefined'; // Firefox 1.0+
var isSafari = Object.prototype.toString.call(window.HTMLElement).indexOf('Constructor') > 0;
// At least Safari 3+: "[object HTMLElementConstructor]"
var isChrome = !!window.chrome && !isOpera; // Chrome 1+
var isIE = /*@cc_on!@*/ false || !!document.documentMode; // At least IE6

indicWaysText = ['.indic-ways-text1',
                     '.indic-ways-text2',
                     '.indic-ways-text3',
                     '.indic-ways-text4',
                     '.indic-ways-text5',
                     '.indic-ways-text6']
indicWays = ['.indic-ways1',
                '.indic-ways2',
                '.indic-ways3']

$(function () {
    //update other textareas and hidden paragraphs when one is updated
    $.each(indicWaysText, function (index, indic) {
        $(indic).keyup(function (e) {
            var text = this.value;
            $(indic).text(text);
        })
    });
    //check to see which browser is being used
    if (!isChrome) {
        //show the warning if it's not chrome
        $('#warning').show();
        if (isIE) {
            console.log('ie');
            $('#instr-ie').show();
            $('#instr-chrome').hide();
            $('#instr-firefox').hide();
        } else if (isFirefox) {
            console.log('firefox');
            $('#instr-firefox').show();
            $('#instr-ie').hide();
            $('#instr-chrome').hide();
        } else {
            console.log('Not the big three');
            $('#instr-chrome').show();
            $('#instr-firefox').hide();
            $('#instr-ie').hide();
        }


    } else {
        console.log('chrome');
        $('#instr-chrome').show();
        $('#instr-firefox').hide();
        $('#instr-ie').hide();
    }


});
var textBlanks = {
    0: {
        0: true,
        1: true
    },
    1: {
        0: true,
        1: true
    },
    2: {
        0: true,
        1: true
    }
}

function checkTextForBlanks() {
    var toReturn = true
    $.each(indicWays, function (idx, indic) {
        //get the text in the textarea for each indicator
        leftTextarea = $(indic + '.left').find('textarea');
        rightTextarea = $(indic + '.right').find('textarea');

        //if there is text in each box
        if (leftTextarea.text().length > 0 && rightTextarea.text().length > 0) {
            //mark them as non blanks
            textBlanks[idx][0] = false;
            textBlanks[idx][1] = false;
            //make sure they are different
            if (leftTextarea.text() == rightTextarea.text()) {
                alert('The examples must be different for ' + leftTextarea.attr('placeholder').split('addressing')[1]);
                toReturn = false;
                return false;
            }
        }

        // if they are both zero then ask for confimation
        else if (leftTextarea.text().length == 0 && rightTextarea.text().length == 0) {
            if (confirm("You didn't enter an example for" + leftTextarea.attr('placeholder').split('addressing')[1] + "; are you sure you want to continue?")) {
                //mark them as blanks and continue
                textBlanks[idx][0] = true;
                textBlanks[idx][1] = true;
                return true;

            } else {
                //exit the function
                textBlanks[idx][0] = true;
                textBlanks[idx][1] = true;
                toReturn = false;
                return false;
            }
        }
        // else one of the boxes is 0 and the other isn't, find out which one
        else {
            if (leftTextarea.text().length > rightTextarea.text().length) {
                textBlanks[idx][0] = false;
                textBlanks[idx][1] = true;
            } else {
                textBlanks[idx][0] = true;
                textBlanks[idx][1] = false;
            }
        }
    });
    return toReturn
}

function checkAllBlanks() {
    toReturn = true
    for (var indic in textBlanks) {
        for (var indic2 in textBlanks[indic]) {
            if (!textBlanks[indic][indic2]) {
                toReturn = false;
                break;
            }
        }
    }
    return toReturn;
}

function editBlanks() {
    for (var indic in textBlanks) {
        curIndic = textBlanks[indic]
            //theyre both blank
        if (curIndic[0] == true && curIndic[1] == true) {
            console.log(indicWays[indic]);
            $(indicWays[indic]).hide();
        }
        //the left one is blank
        else if (curIndic[0] == true && curIndic[1] == false) {
            $(indicWays[indic] + '.left').hide();
            $(indicWays[indic] + '.right').removeClass('right');
            $(indicWays[indic]).toggleClass('indic-ways-box-full');
        }
        //the right one is blank
        else if (curIndic[0] == false && curIndic[1] == true) {
            $(indicWays[indic] + '.right').hide();
            $(indicWays[indic] + '.left').removeClass('left');
            $(indicWays[indic]).toggleClass('indic-ways-box-full');
        }
    }

}

function collabTables() {
    //page can't be taller than this
    var maxHeight = 942;
    var tableRowHeight = 90;
    //split collaborative table to separate page if needed        
    $.each($('.collabs-table'), function (idx, table) {
        var $table = $(table)
        console.log($table)
        $currentPage = $table.closest('.page');
        //if the height is higher than the max height
        if ($currentPage.height() > maxHeight) {
            var numberOfRows = Math.ceil(($currentPage.height() - maxHeight) / tableRowHeight) * -1;
            $currentPage.after("<div class='page'>");
            $newRows = $table.find('tr').slice(numberOfRows);
            $newPage = $currentPage.next('.page');
            $newTable = $newPage.append("<table class= 'new-table'><tbody></tbody></table>");
            $newTable.find("tbody").append($newRows);
        }
    });
}
printed = false;

function checkDoc() {
    if (printed) {
        window.print();
        return;
    }
    if (checkTextForBlanks() == false) {
        return;
    }
    //if they're all blank then hide the header and boxes
    if (checkAllBlanks()) {
        $('#ways-header').hide();
        $('#indic-ways').hide();
        window.print();
        printed = true;
        return;
    }
    if (confirm("Please check the text you entered for errors, if you are ready to print the document then click 'OK'") == true) {
        editBlanks();
        //hide text areas, show paragraphs
        $.each(indicWaysText, function (index, indic) {
                var p = $('p' + indic);
                var textarea = $('textarea' + indic);
                p.show();
                textarea.hide();
            })
            //collabTables();
        if (isChrome) {
            window.print();
        } else {

        }
        printed = true;
    }
}

//toggle instruction visibility
$(function () {
    var $chromeToggle = $("#chrome-toggle")
    $chromeToggle.click(function () {
        if ($chromeToggle.text() === 'Show Instructions') {
            $chromeToggle.text('Hide Instructions');
        } else {
            $chromeToggle.text('Show Instructions');
        }
        $("#instr-chrome-text").toggle();
    });
    var $firefoxToggle = $("#firefox-toggle")
    $firefoxToggle.click(function () {
        if ($firefoxToggle.text() === 'Show Instructions') {
            $firefoxToggle.text('Hide Instructions');
        } else {
            $firefoxToggle.text('Show Instructions');
        }
        $("#instr-firefox-text").toggle();
    });
    var $ieToggle = $("#ie-toggle")
    $ieToggle.click(function () {
        if ($ieToggle.text() === 'Show Instructions') {
            $ieToggle.text('Hide Instructions');
        } else {
            $ieToggle.text('Show Instructions');
        }
        $("#instr-ie-text").toggle();
    });
});