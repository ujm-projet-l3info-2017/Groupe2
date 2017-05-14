

var map ;
var drawingManager ;
var polygones = {} ;
var coordinate_set = [] ;


polygone_complete = function (polygone) {
  coordonates = [] ;
  id = 0 ;
  polygone.getPaths ().forEach (function (a) {
    for (i=0 ; i < a.b.length ; i++) {
      coordonates.push ([a.b[i].lat (), a.b[i].lng ()]) ;
      id += a.b[i].lat () + a.b[i].lng () ;
    }
  }) ;
  create_bubble (coordonates, polygone, id) ;
}

rectangle_complete = function (rectangle) {
  coordonates = [] ;
  ne = rectangle.getBounds().getNorthEast() ;
  sw = rectangle.getBounds().getSouthWest() ;
  coordonates.push ([ne.lat(), ne.lng ()])
  coordonates.push ([ne.lat(), sw.lng ()])
  coordonates.push ([sw.lat(), sw.lng ()])
  coordonates.push ([sw.lat(), ne.lng ()])
  create_bubble (coordonates, rectangle, ne.lat()+ne.lng()+sw.lat()+sw.lng()) ;
}

create_bubble = function (coordonates, polygone, id) {
  coordonates = translate_coordonates_to_positions (coordonates) ;
  div = document.createElement ("div") ;
  div.className = "alert alert-info" ;
  div.id = id ;
  div.coordonates = coordonates ;
  div.polygone = polygone ;
  p = document.createElement ("p") ;
  span = document.createElement ("span") ;
  span.className = "pull-right" ;
  a = document.createElement ("a") ;
  a.className = "glyphicon glyphicon-remove" ;
  a.div_id = id ;
  a.onclick = function (event) {
    delete polygones[event.target.div_id] ;
    div = document.getElementById (event.target.div_id) ;
    div.polygone.setMap (null) ;
    div.remove () ;
  } ;
  span.appendChild (a) ;
  p.appendChild (span) ;
  div.appendChild (p) ;
  for (coordonate = 0 ; coordonate < coordonates.length ; coordonate++) {
    span = document.createElement ("span") ;
    span.innerText = coordonates[coordonate].join (' ; ') ;
    p.appendChild (span) ;
    p.appendChild (document.createElement ("br")) ;
  }
  document.getElementById ("polygones_div").appendChild (div) ;
  coordinate_set.push (coordonates) ;
  document.getElementById("coordinate_set").value = JSON.stringify(coordinate_set) ;
  polygones[id] = coordonates ;
}

function initialize () {
  var latlng = new google.maps.LatLng (46.227636, 2.213749);
  var options = {
    streetViewControl: false,
    center: latlng,
    zoom: 5,
    mapTypeId: google.maps.MapTypeId.HYBRID
  } ;
  map = new google.maps.Map (document.getElementById ("google_map_api_div"), options);
  drawingManager = new google.maps.drawing.DrawingManager ({
    drawingControl: true,
    drawingControlOptions: {
      position: google.maps.ControlPosition.TOP_CENTER,
      drawingModes: ['polygon', 'rectangle']
    }, circleOptions: {
      fillColor: '#ffff00',
      fillOpacity: 1,
      strokeWeight: 5,
      clickable: false,
      editable: true,
      zIndex: 1
    }
  });
  drawingManager.setMap (map) ;
  google.maps.event.addListener (drawingManager, 'polygoncomplete', polygone_complete);
  google.maps.event.addListener (drawingManager, 'rectanglecomplete', rectangle_complete);
} ;


translate_coordonates_to_positions = function (coordinates) {
  var positions = [[0, 0]]
  base = coordinates[0] ;
  for (i = 1; i < coordinates.length ; i += 1) {
    distance_y = getDistanceFromLatLonInKm (base[0], 0, coordinates[i][0], 0) * 1000. ; // from Km to m
    if (base[0] > coordinates[i][0])
      distance_y *= -1 ;
    distance_x = getDistanceFromLatLonInKm (0, base[1], 0, coordinates[i][1]) * 1000. ; // from Km to m
    if (base[1] < coordinates[i][1])
      distance_x *= -1 ;
    positions.push ([distance_x, distance_y])
  }
  return positions ;
}

/*
 * Taken from:
 *  https://stackoverflow.com/questions/18883601/function-to-calculate-distance-between-two-coordinates-shows-wrong
 *
 */
function getDistanceFromLatLonInKm (lat1, lon1, lat2, lon2) {
  var R = 6371; // Radius of the earth in km
  var dLat = deg2rad(lat2-lat1);  // deg2rad below
  var dLon = deg2rad(lon2-lon1); 
  var a = 
    Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) * 
    Math.sin(dLon/2) * Math.sin(dLon/2)
    ; 
  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
  var d = R * c; // Distance in km
  return d;
}

function deg2rad(deg) {
  return deg * (Math.PI/180)
}