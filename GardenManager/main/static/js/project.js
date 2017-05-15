
var stage ;


window.addEventListener ("load", function () {

  document.getElementById ("edit_project_id").style["display"] = "none" ;

  document.getElementById ("add_selected_plant").onclick = add_selected_plant ;

  var width = 500;
  var height = 500;
  stage = new Konva.Stage({
    container: "canvas_container",
    width: width,
    height: height
  });
  /*
  function drawImage(imageObj) {
    var layer = new Konva.Layer();
    // darth vader
    var darthVaderImg = new Konva.Image({
      image: imageObj,
      x: stage.getWidth() / 2 - 200 / 2,
      y: stage.getHeight() / 2 - 137 / 2,
      width: 200,
      height: 137,
      draggable: true
    });
    // add cursor styling
    darthVaderImg.on('mouseover', function() {
      document.body.style.cursor = 'pointer';
    });
    darthVaderImg.on('mouseout', function() {
      document.body.style.cursor = 'default';
    });
    layer.add(darthVaderImg);
    stage.add(layer);
  }
  var imageObj = new Image();
  imageObj.onload = function() {
    drawImage(this);
  };
  imageObj.src = 'https://konvajs.github.io/assets/darth-vader.jpg';
  */
}) ;

add_selected_plant = function () {
  plant_selector = document.getElementById ("plant_selector") ;
  plant = JSON.parse (plant_selector.value) ;
  console.log (plant["sp"]) ;
  console.log (plant["sp"] * 10) ;
  plant_circle = new Konva.Circle ({
    radius : plant["sp"] * 10 || 5,
    x: 10,
    y: 10,
    fill: plant["color"],
    draggable: true
  })
  layer = new Konva.Layer () ;
  layer.add (plant_circle) ;
  stage.add (layer) ;
}