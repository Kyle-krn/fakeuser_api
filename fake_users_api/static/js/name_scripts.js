$(document).on('mousemove', '.result', function(e){
    let top = $(this).offset().top
    let left = $(this).offset().left
    let width = $(this).width()
    dialog_element.style.left =  (left + width - 56) + "px";
    dialog_element.style.top = top - 13 + "px";
  }).on('mouseenter', '.result', function(){
    $("#dialog_element").text("Copy")
    $("#dialog_element").stop().animate({
        backgroundColor: '#01B401'
    }, 0, function(){
        $("#dialog_element").stop().animate({
            'opacity': 1
        }, 200)
    })
    
  }).on('mouseleave', '.result', function(){
    // $("#dialog_element").css('opacity', '0')
    $("#dialog_element").stop().animate({
        'opacity': 0,
    }, 200)
  }).on('click', '.result', function(){
        Copy($(this));
        $("#dialog_element").text("Copied")
        $("#dialog_element").animate({
            backgroundColor: '#ADADAD'
        }, 200)
  })
  
  
$("#show_block, #show_text").click(function(){
    $("#show_block, #show_text").removeClass("active")
    $(this).addClass("active")
if ($(this).attr("id") == "show_block") {
    $("#results__bigger").css("display", "flex")
    $("#results__text").css("display", "none")
} else {
    $("#results__bigger").css("display", "none")
    $("#results__text").css("display", "flex")
}

})

function CopyTextArea(){
    Copy($("#textarea_name"));
    Alert("Copyied!");
}

$('#count_name').on('input keyup', function(){
    if ($(this).val() < 1) {
        $(this).val(1);
    } else if ($(this).val() > 100) {
        $(this).val(100);
    };
});

function AjaxName() {
    let format_name = $("#format_name").val()
    input_data = {
        count: $("#count_name").val(),
        lang: format_name == 6 || format_name == 7? 'eng': 'ru',
        sex: $("#sex_name").val()  
    }
    GetAJAX('generators/ajax_name/', input_data).done(function(data){
            $("#name__null").css("display", "none")
            InputName(data, format_name)
            $("#name__results").css("display", "flex")
            InputTime()
    })
}

function InputTime() {
    let date = Date()
    if (date.lastIndexOf('(') != -1) date = date.split('(')[0]
    $(".results__time").text(date)
}

function InputName(data, format) {
    $("#results__bigger").empty()
    let text_array = []; 
    $.each(data.names, function (index, value) {
        if (format == 0) {
         text = value.last_name + " " + value.first_name + " " + value.patronymic   
        } else if (format == 1 || format == 6) {
            text = text = value.first_name + " " + value.last_name
        } else if (format == 2) {
            text = text = value.last_name + " " + value.first_name
        } else if(format == 3) {
            text = value.last_name + " " + value.first_name[0] + ". " + value.patronymic[0] + '.'
        } else if (format == 4) {
            text = value.first_name + " " + value.last_name[0] + ". " + value.patronymic[0] + '.'
        } else if (format == 5 || format == 7) {
            text = value.first_name
        }
        text_array.push(text)
        $("#results__bigger").append($('<div class="result"></div>').text(text))
    })
    TextAreaNames(text_array)
}


$(document).on('focusin', '#textarea_params', function(){
    $(this).data('val', $(this).val());
    $("#textarea_params").blur()
}).on('change','#textarea_params', function(){
    let sep = GetTextAreaSep($(this).data('val'));
    let text = $("#textarea_name").text();
    TextAreaNames(text.split(sep));
});


function GetTextAreaSep(ta_param) {
    if (ta_param == 0) {
        separation = '\n'
    } else if (ta_param == 1) {
        separation = ', '
    } else if (ta_param == 2) {
        separation = '; '
    } else if (ta_param == 3) {
        separation = ','
    } else if (ta_param == 4) {
        separation = ';'
    }
    return separation
}

function TextAreaNames(text_array) {
    let ta_param = $("#textarea_params").val();
    separation = GetTextAreaSep(ta_param)
    $("#textarea_name").text(text_array.join(separation))
}