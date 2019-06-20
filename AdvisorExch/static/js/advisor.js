

$(document).ready ( function () {
  $(document.body).on ( "click", "tr[data-href]", function () {
    // alert ( this.dataset.href ) ;
    window.location.href = self.location.pathname  + this.dataset.href ;
  } ) ;
} ) ;
