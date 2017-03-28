var map;
var key="AIzaSyCt2Sw46PUXm2hF_e4yrztN0ogH44yeTFk";
getKey = function getKey() { return key ; } ;

	function takePicture(document, map) {
		var currentPosition = map.getCenter();
		document.location.href="http://maps.google.com/maps/api/staticmap?maptype=hybrid?sensor=false&center=" +
currentPosition.lat() + "," + currentPosition.lng() +
"&zoom=" + map.getZoom()+"&key=" + getKey() + "&size=600x400&" +
currentPosition.lat() + ',' + currentPosition.lng();
	}
	function initialize(document) {
//		var lat = google.loader.ClientLocation.latitude;
//      var lng = google.loader.ClientLocation.longitude;
		var latlng = new google.maps.LatLng(46.227636, 2.213749);
		var options = {
			streetViewControl: false,
			center: latlng,
			zoom: 5,
			mapTypeId: google.maps.MapTypeId.HYBRID
		};
		map = new google.maps.Map(document.getElementById("divMap"), options);
	}
	window.initMap = function() {
		// ???
	}
