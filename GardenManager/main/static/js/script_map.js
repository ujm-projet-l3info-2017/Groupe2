

var map ;


getKey = function getKey () {
  return "AIzaSyCt2Sw46PUXm2hF_e4yrztN0ogH44yeTFk" ;
} ;

function takePicture (document, map) {
  var currentPosition = map.getCenter ();
  document.location.href =
    'https://maps.googleapis.com/maps/api/staticmap?' +
    'maptype=satellite' +
    '&center=' + currentPosition.lat () + ',' + currentPosition.lng () +
    '&zoom=' + map.getZoom () +
    '&size=640x400' +
    '&key=' + getKey ();
  /*
   * document.location.href='https://maps.googleapis.com/maps/api/staticmap?' +
   * 'maptype=hybrid?' +
   * 'sensor=false&center=' +
   * currentPosition.lat() + "," + currentPosition.lng() +
   * "&zoom=" + map.getZoom()+"&key=" + getKey() + "&size=600x400&" +
   * currentPosition.lat() + ',' + currentPosition.lng(); 
   */
} ;

function initialize () {
  // var lat = google.loader.ClientLocation.latitude;
  // var lng = google.loader.ClientLocation.longitude;
  var latlng = new google.maps.LatLng (46.227636, 2.213749);
  var options = {
    streetViewControl: false,
    center: latlng,
    zoom: 5,
    mapTypeId: google.maps.MapTypeId.HYBRID
  } ;
  map = new google.maps.Map (document.getElementById ("divMap"), options);
} ;

window.initMap = function () {
} ;
