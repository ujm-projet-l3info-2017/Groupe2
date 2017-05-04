

var map ;
var drawingManager ;
var polygones = {} ;

/*
function toggle_draw_mode (id) {
  if (true)
    return ;
  if (arguments.length === 0) {
    toggle_draw_mode ("google_map_api_div_wrapper") ;
    toggle_draw_mode ("canvas-wrap") ;
    if (document.getElementById ("google_map_api_div_wrapper").style["display"] == "inline") {
      map_div = document.getElementById ("google_map_api_div") ;
      map_div.width -= 1 ;
      document.getElementById ("creation_plan_take_shot_button").innerText = "Keep this view" ;
    } else {
      document.getElementById ("creation_plan_take_shot_button").innerText = "Select the view" ;
      map_div = document.getElementById ("google_map_api_div") ;
      map_div.width += 1 ;
    }
  } else {
    element = document.getElementById (id) ;
    style = element.style["display"] == "inline" ? "none" : "inline" ;
    while (element.style["display"] !== style) {
      element.style["display"] = style ;
    }
  }
}

function takePicture () {
  if (true)
    return ;
  var map_div = document.getElementById ("google_map_api_div") ;
  var map_div_rect = map_div.getBoundingClientRect() ;
  var width = map_div_rect.width ;
  var height = map_div_rect.height ;
  var currentPosition = map.getCenter ();
  var drawing_canvas = document.getElementById ("drawing_canvas") ;
  drawing_canvas.width = width ;
  drawing_canvas.height = height ;
  image = new Image () ;
  image.src = 'https://maps.googleapis.com/maps/api/staticmap?' +
    'maptype=satellite' +
    '&center=' + currentPosition.lat () + ',' + currentPosition.lng () +
    '&zoom=' + map.getZoom () +
    '&size=' + width + 'x' + height +
    '&key=' + get_google_api_key () ;
  image.onload = function() {
    drawing_canvas.getContext ("2d").drawImage (image, 0, 0); 
  } ;
  toggle_draw_mode () ;
} ;

window.addEventListener ("load", function () {
  document.getElementById ("creation_plan_take_shot_button").onclick = takePicture
}, false) ;

*/


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
  coordonates.push ([sw.lat(), ne.lng ()])
  coordonates.push ([ne.lat(), ne.lng ()])
  coordonates.push ([ne.lat(), sw.lng ()])
  coordonates.push ([sw.lat(), sw.lng ()])
  create_bubble (coordonates, rectangle, ne.lat()+ne.lng()+sw.lat()+sw.lng()) ;
}

create_bubble = function (coordonates, polygone, id) {
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

