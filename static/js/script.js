// This example adds a search box to a map, using the Google Place Autocomplete
// feature. People can enter geographical searches. The search box will return a
// pick list containing a mix of places and predicted search terms.
var map, house, senate, addresses, housePolys, senatePolys, statePoly;
var p;

function initAutocomplete() {
    
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 7,
        center: {
            lat: 32.996589,
            lng: -84.277061
        },
        disableDefaultUI: true,
        zoomControl: true,
        maxZoom: 15,
        minZoom: 7,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    });
    map.set('styles', [
        {
            "featureType": "poi",
            "stylers": [
                {
                    "visibility": "off"
                    }
    ]
  }, {
            "featureType": "road",
            "elementType": "geometry",
            "stylers": [
                {
                    "visibility": "simplified"
                    }
    ]
  }, {
            "featureType": "water",
            "stylers": [
                {
                    "visibility": "simplified"
                    }
    ]
  }
]);
    // Create layer select control
    var layerSelect = document.getElementById('layer-select');
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(layerSelect);

    // Create the search box and link it to the UI element.
    var input = document.getElementById('pac-input');
    searchBox = new google.maps.places.SearchBox(input);
    map.controls[google.maps.ControlPosition.LEFT_TOP].push(input);

    house = new google.maps.Data();
    senate = new google.maps.Data();
    state = new google.maps.Data();

    house.loadGeoJson('static/geojson/lower.geojson', {
        idPropertyName: 'dist'
    }, function (features) {
        //make the house polygon to check search results
        housePolys = $.map(features, function (feat) {
            houseGeom = feat.getGeometry();
            housePoly = new google.maps.Polygon({
                paths: houseGeom.getAt(0).getArray(),
                visible: false
            });
            housePoly.setMap(map);
            return {
                id: feat.getId(),
                poly: housePoly
            };
        });
    });

    senate.loadGeoJson('static/geojson/upper.geojson', {
        idPropertyName: 'dist'
    }, function (features) {
        //make the senate polygon to check search results
        senatePolys = $.map(features, function (feat) {
            senateGeom = feat.getGeometry();
            senatePoly = new google.maps.Polygon({
                paths: senateGeom.getAt(0).getArray(),
                visible: false
            });
            senatePoly.setMap(map);
            return {
                id: feat.getId(),
                poly: senatePoly
            };
        });
    });

    state.loadGeoJson('static/geojson/ga_state.geojson', {
        idPropertyName: 'name'
    }, function (features) {
        //make the GA polygon to check search results
        $.each(features, function (index, feat) {
            gaGeom = feat.getGeometry();
            statePoly = new google.maps.Polygon({
                paths: gaGeom.getAt(0).getArray(),
                visible: false
            });
            statePoly.setMap(map);
            $('#work-in-progress').fadeOut(100);

        });
    });

    house.setStyle(styleFeature);
    senate.setStyle({
        clickable: false,
        visible: false
    });

    state.setStyle({
        clickable: false,
        visible: false
    });

    house.setMap(map);
    senate.setMap(map);
    state.setMap(map);


    // Bias the SearchBox results towards current map's viewport.
    map.addListener('bounds_changed', function () {
        searchBox.setBounds(map.getBounds());
    });

    house.addListener('mouseover', function (e) {
        e.feature.setProperty('state', 'hover');
    });
    house.addListener('mouseout', function (e) {
        e.feature.setProperty('state', 'normal');
    });
    senate.addListener('mouseover', function (e) {
        e.feature.setProperty('state', 'hover');
    });
    senate.addListener('mouseout', function (e) {
        e.feature.setProperty('state', 'normal');
    });
    house.addListener('click', createInfoBox);
    senate.addListener('click', createInfoBox);

    addresses = [];
    // [START region_getplaces]
    // Listen for the event fired when the user selects a prediction and retrieve
    // more details for that place.
    searchBox.addListener('places_changed', function () {
        //if there's no places, then don't do anything
        var places = searchBox.getPlaces();
        if (places.length == 0) {
            return;
        }

        //if there's more than one place (i.e. walmart stores), show error message and return
        if (places.length > 1) {
            $('#pac-input').attr('data-original-title', "Try to be more specific.");
            $('#pac-input').tooltip('show');
            setTimeout(function () {
                $('#pac-input').tooltip('hide');
            }, 2000);
            $('#pac-input').val('');
            return;
        }

        // Clear out the old addresses.
        addresses = [];

        //create a new bounds object for the place
        bounds = new google.maps.LatLngBounds();
        place = places[0];

        //check to make sure place is within Georgia
        if (!google.maps.geometry.poly.containsLocation(place.geometry.location, statePoly)) {
            $('#pac-input').attr('data-original-title', "Choose an address in Georgia.");
            $('#pac-input').tooltip('show');
            setTimeout(function () {
                $('#pac-input').tooltip('hide');
            }, 2000);
            $('#pac-input').val('');
            return;
        }

        // For place, get the icon, name and location.        
        var icon = {
            url: place.icon,
            size: new google.maps.Size(71, 71),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(17, 34),
            scaledSize: new google.maps.Size(25, 25)
        };

        //add place to array
        addresses.push(place);

        //find out which layer is selected, then trigger a click on that layer
        if ($("input[name='layer']:checked").val() === "house") {
            google.maps.event.trigger(house, 'click', place.geometry.location);
        } else {
            google.maps.event.trigger(senate, 'click', place.geometry.location);
        }
        addresses = [];

        if (place.geometry.viewport) {
            // Only geocodes have viewport.
            bounds.union(place.geometry.viewport);
        } else {
            bounds.extend(place.geometry.location);
        }
        map.fitBounds(bounds);
    });
    // [END region_getplaces]
}
google.maps.event.addDomListener(window, 'load', initAutocomplete);

var box;
var distr, distType;

function createInfoBox(event) {
    if (typeof box != "undefined") {
        box.setMap(null);
    }
    distType = $("input[name='layer']:checked").val();
    buttonString = '<button class="btn btn-primary" onClick="submitDistrict()">Use this district</button>';

    //box options
    var boxOptions = {
        boxClass: 'descrbox',
        disableAutoPan: true,
        isHidden: false,
        zIndex: 10,
        enableEventPropagation: false

    };

    //if an address has been entered
    if (addresses.length > 0) {
        //then get the marker
        address = addresses[0];

        //create the box, add the text, anchor it at address location
        box = new InfoBox(boxOptions);
        //find out which layer is selected, then create the content string
        if (distType === "house") {
            distr = getDistrict(event, 'house');
            box.setContent('The address you selected is in House District ' + distr + buttonString);
        } else {
            distr = getDistrict(event, 'senate');
            box.setContent('The address you selected is in Senate District ' + distr + buttonString);
        }

        box.setPosition(address.geometry.location);
        box.open(map);
    } else {

        //create the box, add the text, anchor it at address location
        box = new InfoBox(boxOptions);

        distr = event.feature.getId();
        //find out which layer is selected, then create the content string
        if (distType === "house") {
            box.setContent('You selected House District ' + distr + buttonString);
        } else {
            box.setContent('You selected Senate District ' + distr + buttonString);
        }

        box.setPosition(event.latLng);
        box.open(map);
    }

}

function getDistrict(location, type) {
    var distr;
    if (type === 'house') {
        $.each(housePolys, function (idx, obj) {
            if (google.maps.geometry.poly.containsLocation(location, obj.poly)) {
                distr = obj.id;
            }
        });
    }
    if (type === 'senate') {
        $.each(senatePolys, function (idx, obj) {
            if (google.maps.geometry.poly.containsLocation(location, obj.poly)) {
                distr = obj.id;
            }
        });
    }
    return distr;
}

//toggle house or senate layer
$(function () {
    $("#layer-select :input").change(function () {
        //senate layer selected
        if (this.id === 'senate') {
            house.setStyle({
                clickable: false,
                visible: false,
            });
            senate.setStyle(styleFeature);
            //house layer selected
        } else {
            house.setStyle(styleFeature);

            senate.setStyle({
                clickable: false,
                visible: false,
            });
        }
    });
});

//wire tooltips
$(function () {
    $('#pac-input').tooltip({
        title: 'Try to be more specific.',
        placement: 'bottom',
        trigger: 'manual',
        position: 'fixed'
    });
});

function styleFeature(feature) {
    var outlineWeight, zIndex;
    var color = 'black';
    if (feature.getProperty('state') === 'hover') {
        outlineWeight = zIndex = 2;
        color = 'yellow';
    } else {
        color = 'black';
        outlineWeight = .75;
        zIndex = 1;
    }

    return {
        clickable: true,
        visible: true,
        strokeWeight: outlineWeight,
        strokeColor: color,
        fillOpacity: 0.25,
        fillColor: 'light grey',
        zIndex: zIndex
    };
}

function submitDistrict() {
    console.log(distType, distr);
    var $newForm = $('<form>', {
            'action': '/map_submit',
            'method': 'post'
        })
        .append($('<input>', {
            'name': 'dist-type',
            'value': distType,
            'type': 'hidden'
        }))
        .append($('<input>', {
            'name': 'dist-number',
            'value': distr,
            'type': 'hidden'
        }));
    $newForm.appendTo("body").submit();
}
 