

var map ;

function toggle_draw_mode (id) {
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
    console.log (" make " + id + " " + style)
    while (element.style["display"] !== style) {
      element.style["display"] = style ;
    }
  }
}

function takePicture () {
  var map_div = document.getElementById ("google_map_api_div") ;
  var map_div_rect = map_div.getBoundingClientRect() ;
  var width = map_div_rect.width ;
  var height = map_div_rect.height ;
  var currentPosition = map.getCenter ();
  var drawing_canvas = document.getElementById ("drawing_canvas") ;
  drawing_canvas.width = width ;
  drawing_canvas.height = height ;
  document.getElementById ("google_map_image").src = 'https://maps.googleapis.com/maps/api/staticmap?' +
    'maptype=satellite' +
    '&center=' + currentPosition.lat () + ',' + currentPosition.lng () +
    '&zoom=' + map.getZoom () +
    '&size=' + width + 'x' + height +
    '&key=' + get_google_api_key () ;
  toggle_draw_mode () ;
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
  toggle_draw_mode ("google_map_api_div_wrapper") ;
} ;

window.addEventListener ("load", function () {
  document.getElementById ("creation_plan_take_shot_button").onclick = takePicture
}, false) ;