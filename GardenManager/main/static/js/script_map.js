

var map ;

function takePicture () {
  var currentPosition = map.getCenter ();
  document.location.href =
    'https://maps.googleapis.com/maps/api/staticmap?' +
    'maptype=satellite' +
    '&center=' + currentPosition.lat () + ',' + currentPosition.lng () +
    '&zoom=' + map.getZoom () +
    '&size=640x400' +
    '&key=' + get_google_api_key () ;
} ;

function initialize () {
  var latlng = new google.maps.LatLng (46.227636, 2.213749);
  var options = {
    streetViewControl: false,
    center: latlng,
    zoom: 5,
    mapTypeId: google.maps.MapTypeId.HYBRID
  } ;
  map = new google.maps.Map (document.getElementById ("google_map_api_div"), options);
} ;

window.addEventListener ("load", function () {
  document.getElementById ("creation_plan_take_shot_button").onclick = takePicture
}, false) ;