
window.addEventListener ("load", function () {

  document.getElementById ("submit_delete_account_button").onclick = function () {
    $('#submit_delete_account')[0].click () ;
  } ;

  document.getElementById ("magic_sentence").onpast = function () {
    return false ;
  } ;

}) ;