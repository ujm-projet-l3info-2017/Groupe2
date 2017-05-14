

delete_project_success = function (name) {
  div = document.createElement ("div") ;
  div.innerHTML = '\
        <div id="success_notice" class="text-center">\
          <button id="success_info_alert" type="button" class="close">&times;</button>\
          <div class="alert alert-success">\
            <p>The project "' + name + '" has been deleted</p>\
          </div>\
        </div>\
  ' ;
  container = document.getElementById ("main_layout_container") ; 
  container.insertBefore (div, container.firstChild) ;
  document.getElementById ("success_info_alert").onclick = function () {
    $("#success_notice").hide () ;
  } ;
  document.getElementById ("project_"+name).style["display"] = "none" ;
}

delete_project_fail = function (name) {
  div = document.createElement ("div") ;
  div.innerHTML = '\
        <div id="fail_notice" class="text-center">\
          <button id="fail_info_alert" type="button" class="close">&times;</button>\
          <div class="alert alert-success">\
            <p>Fail<br />The project "' + name + '" could not be deleted</p>\
          </div>\
        </div>\
  ' ;
  container = document.getElementById ("main_layout_container") ; 
  container.insertBefore (div, container.firstChild) ;
  document.getElementById ("fail_info_alert").onclick = function () {
    $("#fail_notice").hide () ;
  } ;
}

delete_project = function (name, csrf) {
  if (!confirm("This will delete the project '" + name + "'"))
    return ;
  $.ajax ({
    type: 'POST',
    url: "/delete",
    async: true,
    data: { name: name , csrfmiddlewaretoken: csrf}, 
    dataType: "json",
    statusCode: {
      200: function () {delete_project_success (name)}, 
      422: function () {delete_project_fail (name)}
    }
  }).done(null);
}