
window.addEventListener ("load", function () {

  var alert = document.getElementById ("global_info_alert") ;
  var submit_login_form_button = document.getElementById ("submit_login_form_button") ;
  var submit_register_form_button = document.getElementById ("submit_register_form_button") ;
  var register_user_password = document.getElementById ("register_user_password") ;
  var register_user_password_verif = document.getElementById ("register_user_password_verif") ;


  if (alert !== null)
    alert.onclick = function () {
      $("#flash_notice").hide () ;
    } ;

  if (submit_login_form_button !== null){
    submit_login_form_button.onclick = function () {
      $('#submit_login')[0].click () ;
    } ;
  }

  if (submit_register_form_button !== null) {
    submit_register_form_button.onclick = function () {
      $('#submit_register')[0].click () ;
    } ;
  }

  if (register_user_password !== null) {
    register_user_password.onchange = function () {
      $('#register_user_password_verif')[0].pattern = '^' + this.value + '$' ;
    } ;
  }

  if (register_user_password_verif !== null) {
    register_user_password_verif.onchange = function () {
      $('#formRegister').validate () ;
    } ;
    register_user_password_verif.oninput = function () {
      this.setCustomValidity('') ;
    } ;
    register_user_password_verif.oninvalid = function () {
      this.setCustomValidity('Password does not match') ;
    } ;
  }

}) ;