
window.addEventListener ("load", function () {

  var alert = document.getElementById ("global_info_alert") ;
  if (alert !== null)
    document.getElementById ("global_info_alert").onclick = function () {
      $("#flash_notice").hide () ;
    } ;

  document.getElementById ("submit_login_form_button").onclick = function () {
    $('#submit_login')[0].click () ;
  } ;

  document.getElementById ("submit_register_form_button").onclick = function () {
    $('#submit_register')[0].click () ;
  } ;

  document.getElementById ("register_user_password").onchange = function () {
    $('#register_user_password_verif')[0].pattern = '^' + this.value + '$' ;
  } ;

  document.getElementById ("register_user_password_verif").onchange = function () {
    $('#formRegister').validate () ;
  } ;
  document.getElementById ("register_user_password_verif").oninput = function () {
    this.setCustomValidity('') ;
  } ;
  document.getElementById ("register_user_password_verif").oninvalid = function () {
    this.setCustomValidity('Password does not match') ;
  } ;

}) ;