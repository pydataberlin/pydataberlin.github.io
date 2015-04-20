jQuery(document).ready(function($) {
  $('.speaker__toggle--abstract').click(function(event) {
    event.stopPropagation();
    event.preventDefault();

    $(this).parent().find('.speaker__abstract__text').toggle();
    $(this).parent().find('.speaker__bio__text').hide();
    
  });
  
  $('.speaker__toggle--bio').click(function(event) {
    event.stopPropagation();
    event.preventDefault();
    
    $(this).parent().find('.speaker__bio__text').toggle();
    $(this).parent().find('.speaker__abstract__text').hide();

  });
});