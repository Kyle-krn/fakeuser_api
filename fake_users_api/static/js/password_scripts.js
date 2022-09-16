$(function(){
    AjaxPassword()

    $(document).on('click', '#icon_copy', function(event){
        Copy($(".received_block__text span"))
        Alert("Copyied!")
    });

    $(document).on('click', '#icon_refresh', ClickRefresh)
    let deg = 0
    function ClickRefresh() {
        if (!$(".received_block__text span").queue().length){
            AjaxPassword();
            deg += 180;
            $(this).css('transform', `rotate(${deg}deg)`);
        };
    };

    $('.info-img').hover(
        function() {
            $(this).siblings('.preset__info').css("opacity", "1");
        },
        function() {
            $(this).siblings('.preset__info').css("opacity", "0");
        }
    );

    $('input:radio[name=preset],' +
      '.settings_password input,'  + 
      '#length_password__number,'  +
      '#length_password__range').on('change', function(){
          AjaxPassword()
      });

    $('#length_password__range').on('input keyup', function(){
        $('#length_password__number').val($(this).val());
    });
    
    $('#length_password__number').on('input keyup', function(){
        if ($(this).val() < 1) {
            $('#length_password__range,#length_password__number').val(1);
        } else if ($(this).val() > 50) {
            $('#length_password__range,#length_password__number').val(50);
        } else {
            $('#length_password__range').val($(this).val());
        };
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

});


function AjaxPassword() {
    let pass_block = $(".received_block__text span")
    let data = {
        lenght: $("#length_password__number").val(),
        easy_to_read: $('#radio__easy_to_read').is(':checked'), 
        characters: function() {
            let characters = []
            $.each($('.settings_password input'), function (index, value) {
                if ($(value).prop("checked") == true) characters.push($(value).attr("name"))     
            });
            return characters
        }()
    }
    GetAJAX('generators/ajax_password/', data).done(function(data){
        pass_block.animate({top: '-=100'}, 200, function(){
            $(".received_block__text span").text(data.password);
        })
        pass_block.animate({top: '+=200'}, 0).animate({top: '-=100'}, 200, function(){
            PasswordTextBlockWidth()
        })
    })
}


function PasswordTextBlockWidth() {
    let text_width = $("#password")
    let block_width = $('.received_block').width() - ($(".received_block__icons").width()+24 + 12 + 25) - 5
    console.log(`Text: ${text_width.width()} || Block: ${block_width}`)
    while (text_width.width() > block_width) {
        let FontSize = parseInt(text_width.css('font-size'))
        if (FontSize <= 18) break;
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
