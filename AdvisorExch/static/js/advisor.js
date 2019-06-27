

$(document).ready ( function () {
  $(document.body).on ( "click", "tr[data-href]", function () {
    // alert ( this.dataset.href ) ;
    //console.log( this.dataset.href);
    submitform(this.dataset.href)
    // window.location.href = self.location.pathname ;
  } ) ;
} ) ;

function submitform(el)
{
  console.log(el);
  document.getElementById('dtlForm').value = el;
  document.forms['detail_advisor'].submit(el);
}
