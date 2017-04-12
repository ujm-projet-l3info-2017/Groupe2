

toggle_hidden = function (id) {
  if (typeof(id) == "string") {
    element = document.getElementById (id) ;
    element.style["display"] = element.style["display"] != "none" ? "none" : "inline";
  } else if (typeof(id) === "object") {
    for (i=0; i < id.length; i++) {
      toggle_hidden (id[i]) ;
    }
  }
  return false ;
}