$(document).ready(function() {
    $('.header__burger').click(function(event) {
        $('.header__burger,.header__menu').toggleClass('active');
        $('body').toggleClass('lock');

    });
});

jQuery('img.svg').each(function() {
    var $img = jQuery(this);
    var imgID = $img.attr('id');
    var imgClass = $img.attr('class');
    var imgURL = $img.attr('src');
  
    jQuery.get(imgURL, function(data) {
      var $svg = jQuery(data).find('svg');
      if (typeof imgID !== 'undefined') {
        $svg = $svg.attr('id', imgID);
      }
      if (typeof imgClass !== 'undefined') {
        $svg = $svg.attr('class', imgClass + ' replaced-svg');
      }
      $svg = $svg.removeAttr('xmlns:a');
      if (!$svg.attr('viewBox') && $svg.attr('height') && $svg.attr('width')) {
        $svg.attr('viewBox', '0 0 ' + $svg.attr('height') + ' ' + $svg.attr('width'))
      }
      $img.replaceWith($svg);  
    }, 'xml');
  
  });

function Copy(el) {
  window.navigator.clipboard.writeText(el.text())
}


function Alert(text) {
  $("#alert").text(text)
  $("#alert").fadeIn();
  setTimeout(() => { $("#alert").fadeOut(); }, 1500);
}

function GetAJAX(url, data) {
  return $.ajax({
    url: 'http://127.0.0.1:8000/' + url,
    traditional: true,
    data: data,
        dataType: 'json',
    })
}

$(window).on("scroll", function() {
  if ($(window).scrollTop() > 50) $('.header').addClass('fixed');
        else $('.header').removeClass('fixed');
  });

$(".radio_lang").on('change', function(){
    this.form.submit();
  })