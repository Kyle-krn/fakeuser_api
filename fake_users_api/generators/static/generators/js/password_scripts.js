$('#length_password__range').on('input keyup', function(){
    $('#length_password__number').val($(this).val());
});

$('#length_password__number').on('input keyup', function(){
    if ($(this).val() < 1) {
        $(this).val(1);
        $('#length_password__range').val(1);
    } else if ($(this).val() > 50) {
        $(this).val(50);
        $('#length_password__range').val(50);
    } else {
        $('#length_password__range').val($(this).val());
    }
    ;
});

$('.info-img').hover(
    function() {
        $(this).siblings('.preset__info').css("display", "inline");
    },
    function() {
        $(this).siblings('.preset__info').css("display", "none");
    }
);


$('input:radio[name=preset]').click(function() {
    let checkbox = $("#checkbox_symbols, #checkbox_numbers");
    if ($(this).val() == 'easy_to_say') {
        checkbox.prop('disabled', true).prop('checked', false);
    } else if ($(this).val() == 'easy_to_read') {
        checkbox.prop('disabled', false);
    } else {
        checkbox.prop('disabled', false).prop('checked', true);
    }
  });

