

$(document).ready ( function () {
  $(document.body).on ( "click", "tr[data-href]", function () {
    // alert ( this.dataset.href ) ;
    //console.log( this.dataset.href);
    submitform(this.dataset.href)
    // window.location.href = self.location.pathname ;
  } ) ;

  // $("#btn_new").click(function(){
  //   console.log( 'New Button clicked');
  //
  //   // $("#btn_sav").hide();
  //   $("#btn_sav").css("disabled");
  //
  // } ) ;

} ) ;



function submitform(el)
{
  console.log(el);
  document.getElementById('dtlForm').value = el;
  document.forms['detail_advisor'].submit(el);
}
;
