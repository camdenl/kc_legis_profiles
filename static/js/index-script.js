function validateLegisForm() {
    var dist = $('#district-number').val();
    var type = $('#district-select').val();
    var checked = $("input[name='indic-check-legis']:checked").length;
    //its a valid integer above 0
    if (Math.floor(dist) == dist && $.isNumeric(dist) && dist > 0) {
        //make sure the senate and house district numbers are valid
        if (type === 'Senate' && dist > 56) {
            //raise the tooltip with the error message
            $('#district-number').attr('data-original-title', "There are only 56 Senate districts in Georgia.")
            $('#district-number').tooltip('show');
            setTimeout(function () {
                $('#district-number').tooltip('hide');
            }, 2000);
            $('#district-number').val('');
            return false
        } else if (type === 'House' && dist > 180) {
            $('#district-number').attr('data-original-title', "There are only 180 House districts in Georgia.")
            $('#district-number').tooltip('show');
            setTimeout(function () {
                $('#district-number').tooltip('hide');
            }, 2000);
            $('#district-number').val('');
            return false
        } else if (checked < 3 || checked > 3) {
            $('#checkboxes-label-legis').attr('data-original-title', "Please select only three indicators.")
            $('#checkboxes-label-legis').tooltip('show');
            setTimeout(function () {
                $('#checkboxes-label-legis').tooltip('hide');
            }, 2000);
            return false;
        }
        //we have a winner!
        else {
            return true;
        }

    } else {
        //raise the tooltip with the error message
        $('#district-number').attr('data-original-title', "Please enter a valid number above 0, there are 56 Senate districts and 180 House districts in Georgia.")
        $('#district-number').tooltip('show');
        setTimeout(function () {
            $('#district-number').tooltip('hide');
        }, 2000);
        $('#district-number').val('');
        return false;
    }

}

function validateCountyForm() {
    //check county indicator checkboxes
    var checked = $("input[name='indic-check-county']:checked").length;
    if (checked < 3 || checked > 3) {
        $('#checkboxes-county-label').attr('data-original-title', "Please select only three indicators.")
        $('#checkboxes-county-label').tooltip('show');
        setTimeout(function () {
            $('#checkboxes-county-label').tooltip('hide');
        }, 2000);
        return false;
    }
    //check to make sure a county has been selected
    else if ($('#county-selector').val().length < 1) {
        alert("Please select a county first.");
        return false;
    }
    //we have a winner!
    else {
        return true;
    }

}


//wire up tooltips and checkboxes
$(function () {
    $('[data-toggle="tooltip"]').tooltip({
        position: 'fixed',
        trigger: 'manual'
    });
    $('#checkboxes').checkboxes('max', 3);
})

var coNames = [
    {
        "county": "Appling"
  },
    {
        "county": "Atkinson"
  },
    {
        "county": "Bacon"
  },
    {
        "county": "Baker"
  },
    {
        "county": "Baldwin"
  },
    {
        "county": "Banks"
  },
    {
        "county": "Barrow"
  },
    {
        "county": "Bartow"
  },
    {
        "county": "Ben Hill"
  },
    {
        "county": "Berrien"
  },
    {
        "county": "Bibb"
  },
    {
        "county": "Bleckley"
  },
    {
        "county": "Brantley"
  },
    {
        "county": "Brooks"
  },
    {
        "county": "Bryan"
  },
    {
        "county": "Bulloch"
  },
    {
        "county": "Burke"
  },
    {
        "county": "Butts"
  },
    {
        "county": "Calhoun"
  },
    {
        "county": "Camden"
  },
    {
        "county": "Candler"
  },
    {
        "county": "Carroll"
  },
    {
        "county": "Catoosa"
  },
    {
        "county": "Charlton"
  },
    {
        "county": "Chatham"
  },
    {
        "county": "Chattahoochee"
  },
    {
        "county": "Chattooga"
  },
    {
        "county": "Cherokee"
  },
    {
        "county": "Clarke"
  },
    {
        "county": "Clay"
  },
    {
        "county": "Clayton"
  },
    {
        "county": "Clinch"
  },
    {
        "county": "Cobb"
  },
    {
        "county": "Coffee"
  },
    {
        "county": "Colquitt"
  },
    {
        "county": "Columbia"
  },
    {
        "county": "Cook"
  },
    {
        "county": "Coweta"
  },
    {
        "county": "Crawford"
  },
    {
        "county": "Crisp"
  },
    {
        "county": "Dade"
  },
    {
        "county": "Dawson"
  },
    {
        "county": "Decatur"
  },
    {
        "county": "DeKalb"
  },
    {
        "county": "Dodge"
  },
    {
        "county": "Dooly"
  },
    {
        "county": "Dougherty"
  },
    {
        "county": "Douglas"
  },
    {
        "county": "Early"
  },
    {
        "county": "Echols"
  },
    {
        "county": "Effingham"
  },
    {
        "county": "Elbert"
  },
    {
        "county": "Emanuel"
  },
    {
        "county": "Evans"
  },
    {
        "county": "Fannin"
  },
    {
        "county": "Fayette"
  },
    {
        "county": "Floyd"
  },
    {
        "county": "Forsyth"
  },
    {
        "county": "Franklin"
  },
    {
        "county": "Fulton"
  },
    {
        "county": "Gilmer"
  },
    {
        "county": "Glascock"
  },
    {
        "county": "Glynn"
  },
    {
        "county": "Gordon"
  },
    {
        "county": "Grady"
  },
    {
        "county": "Greene"
  },
    {
        "county": "Gwinnett"
  },
    {
        "county": "Habersham"
  },
    {
        "county": "Hall"
  },
    {
        "county": "Hancock"
  },
    {
        "county": "Haralson"
  },
    {
        "county": "Harris"
  },
    {
        "county": "Hart"
  },
    {
        "county": "Heard"
  },
    {
        "county": "Henry"
  },
    {
        "county": "Houston"
  },
    {
        "county": "Irwin"
  },
    {
        "county": "Jackson"
  },
    {
        "county": "Jasper"
  },
    {
        "county": "Jeff Davis"
  },
    {
        "county": "Jefferson"
  },
    {
        "county": "Jenkins"
  },
    {
        "county": "Johnson"
  },
    {
        "county": "Jones"
  },
    {
        "county": "Lamar"
  },
    {
        "county": "Lanier"
  },
    {
        "county": "Laurens"
  },
    {
        "county": "Lee"
  },
    {
        "county": "Liberty"
  },
    {
        "county": "Lincoln"
  },
    {
        "county": "Long"
  },
    {
        "county": "Lowndes"
  },
    {
        "county": "Lumpkin"
  },
    {
        "county": "Macon"
  },
    {
        "county": "Madison"
  },
    {
        "county": "Marion"
  },
    {
        "county": "McDuffie"
  },
    {
        "county": "McIntosh"
  },
    {
        "county": "Meriwether"
  },
    {
        "county": "Miller"
  },
    {
        "county": "Mitchell"
  },
    {
        "county": "Monroe"
  },
    {
        "county": "Montgomery"
  },
    {
        "county": "Morgan"
  },
    {
        "county": "Murray"
  },
    {
        "county": "Muscogee"
  },
    {
        "county": "Newton"
  },
    {
        "county": "Oconee"
  },
    {
        "county": "Oglethorpe"
  },
    {
        "county": "Paulding"
  },
    {
        "county": "Peach"
  },
    {
        "county": "Pickens"
  },
    {
        "county": "Pierce"
  },
    {
        "county": "Pike"
  },
    {
        "county": "Polk"
  },
    {
        "county": "Pulaski"
  },
    {
        "county": "Putnam"
  },
    {
        "county": "Quitman"
  },
    {
        "county": "Rabun"
  },
    {
        "county": "Randolph"
  },
    {
        "county": "Richmond"
  },
    {
        "county": "Rockdale"
  },
    {
        "county": "Schley"
  },
    {
        "county": "Screven"
  },
    {
        "county": "Seminole"
  },
    {
        "county": "Spalding"
  },
    {
        "county": "Stephens"
  },
    {
        "county": "Stewart"
  },
    {
        "county": "Sumter"
  },
    {
        "county": "Talbot"
  },
    {
        "county": "Taliaferro"
  },
    {
        "county": "Tattnall"
  },
    {
        "county": "Taylor"
  },
    {
        "county": "Telfair"
  },
    {
        "county": "Terrell"
  },
    {
        "county": "Thomas"
  },
    {
        "county": "Tift"
  },
    {
        "county": "Toombs"
  },
    {
        "county": "Towns"
  },
    {
        "county": "Treutlen"
  },
    {
        "county": "Troup"
  },
    {
        "county": "Turner"
  },
    {
        "county": "Twiggs"
  },
    {
        "county": "Union"
  },
    {
        "county": "Upson"
  },
    {
        "county": "Walker"
  },
    {
        "county": "Walton"
  },
    {
        "county": "Ware"
  },
    {
        "county": "Warren"
  },
    {
        "county": "Washington"
  },
    {
        "county": "Wayne"
  },
    {
        "county": "Webster"
  },
    {
        "county": "Wheeler"
  },
    {
        "county": "White"
  },
    {
        "county": "Whitfield"
  },
    {
        "county": "Wilcox"
  },
    {
        "county": "Wilkes"
  },
    {
        "county": "Wilkinson"
  },
    {
        "county": "Worth"
  }
]

//populate the county selector
$(function () {
    $.each(coNames, function (index, obj) {
        // append an option to the county-variable select
        $('#county-selector')
            .append($('<option>', {
                value: obj.county,
                text: obj.county
            }));
    });
    // wire up the selector
    $('#county-selector').selectpicker();
    $('#county-selector').addClass('small-screen').selectpicker('setStyle');
    if (/Android|webOS|iPhone|iPod|BlackBerry/i.test(navigator.userAgent)) {
        $('#county-selector').selectpicker('mobile');
    }
});
//wire up the buttons
$(function () {
    $('#legis-btn').click(function () {
        $('#back-btn-div').show();
        $('#nav-buttons').hide();
        $('#legis-form').show();
    })
    $('#county-btn').click(function () {
        $('#back-btn-div').show();
        $('#nav-buttons').hide();
        $('#county-form').show();
    })
    $('#back-btn').click(function () {
        $('#back-btn-div').hide();
        $('#nav-buttons').show();
        $('#county-form').hide();
        $('#legis-form').hide();
    })
    if ($('#house-boolean').data().name.length > 0) {
        $('#legis-btn').click();
    }
});