

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
  toggle_draw_mode () ;
  var currentPosition = map.getCenter ();
  document.getElementById ("google_map_image").src = 'https://maps.googleapis.com/maps/api/staticmap?' +
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
  toggle_draw_mode ("google_map_api_div_wrapper") ;
} ;

window.addEventListener ("load", function () {
  document.getElementById ("creation_plan_take_shot_button").onclick = takePicture
}, false) ;