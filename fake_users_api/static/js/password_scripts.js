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

$('.settings_password input').on('change', function(){
    let allow_checked = false
    $.each($('.settings_password input'), function (index, value) {
        if ($(value).prop("checked") == true) allow_checked = true     
    });
    if (allow_checked == false) $(this).prop('checked', true)
});


$('input:radio[name=preset]').click(function() {
    let checkbox = $("#checkbox_symbols, #checkbox_numbers");
    if ($(this).val() == 'easy_to_say') {
        checkbox.prop('disabled', true).prop('checked', false);
        $("#checkbox_uppercase, #checkbox_lowercase").prop('checked', true)
    } else if ($(this).val() == 'easy_to_read') {
        checkbox.prop('disabled', false);
    } else {
        checkbox.prop('disabled', false).prop('checked', true);
    }
});

$('input:radio[name=preset],' +
  '.settings_password input,'  + 
  '#length_password__number,'  +
  '#length_password__range').on('change', function(){
    AjaxPassword()
});


$('.info-img').hover(
    function() {
        $(this).siblings('.preset__info').css("display", "inline");
    },
    function() {
        $(this).siblings('.preset__info').css("display", "none");
    }
);


$(document).on('click', '#icon_refresh', ClickRefresh)


let deg = 0
function ClickRefresh() {
    if (!$(".received_password_block__text").queue().length){
        AjaxPassword();
        deg += 180;
        $(this).css('transform', `rotate(${deg}deg)`);
    };
};


$(document).on('click', '#icon_copy', function(event){
    window.navigator.clipboard.writeText($("#password").text())
    $("#alert_copyied").fadeIn();
    setTimeout(() => { $("#alert_copyied").fadeOut(); }, 1500);
})


$(function(){
    AjaxPassword()
});

function AjaxPassword() {
    let pass_block = $(".received_password_block__text")
    let data = {
        password_length: $("#length_password__number").val(),
        easy_to_read: $('#radio__easy_to_read').is(':checked'), 
        characters: function() {
            let characters = []
            $.each($('.settings_password input'), function (index, value) {
                if ($(value).prop("checked") == true) characters.push($(value).attr("name"))     
            });
            return characters
        }()
    } 

    $.ajax({
        crossdomain: true,
        url: 'http://127.0.0.1:8000/generators/ajax_password/',         /* Куда отправить запрос */
        method: 'POST',             /* Метод запроса (post или get) */
        contentType: "application/json; charset=utf-8",
        dataType: 'json',          /* Тип данных в ответе (xml, json, script, html). */
        data: JSON.stringify(data),     /* Данные передаваемые в массиве */
        success: function(data){   /* функция которая будет выполнена после успешного запроса.  */
            pass_block.animate({top: '-=100'}, 200, function(){
                $("#password").text(data.password);
            })
            pass_block.animate({top: '+=200'}, 0).animate({top: '-=100'}, 200)
            PasswordTextBlockWidth()

        }
    })
    
    ;
}


function PasswordTextBlockWidth() {
    let text_width = $(".password.active")
    let block_width = $(".received_password_block").width() - $(".received_password_block__icons").width() - ($(".received_password_block").innerWidth() - $(".received_password_block").width())
    while (text_width.width() > block_width) {
        let FontSize = parseInt(text_width.css('font-size'))
        if (FontSize <= 20) break;
        FontSize--
        text_width.css('font-size', `${FontSize}px`)
    }

    while (text_width.width() < block_width) {
        let FontSize = parseInt(text_width.css('font-size'))
        if (FontSize >= 40) break;
        FontSize++
        text_width.css('font-size', `${FontSize}px`)
    }
}
