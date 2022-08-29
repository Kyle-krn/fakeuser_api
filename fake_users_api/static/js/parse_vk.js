
let parse_data; 
function AjaxParseVk(next = false) {
    $.ajax({
        crossdomain: true,
        url: 'http://127.0.0.1:8000/parse/get_member_group/',         /* Куда отправить запрос */
        method: 'GET',             /* Метод запроса (post или get) */
        dataType: 'json',          /* Тип данных в ответе (xml, json, script, html). */
        data: {},
        success: function(data){   /* функция которая будет выполнена после успешного запроса.  */
        parse_data = data;
        $("#count_data").text(data.count_data);
        if (data.count_data == 0) return;    
        $("#parse_block__photo").animate({top: '-=500'}, 200)
            $("#parse_block__name").animate({top: '-=500'}, 200, function() {
                if (next) {
                    $("#vk_photo").replaceWith(next_img)
                    InitNextImg(data)
                } else {
                    $("#vk_photo").attr("src", data.photo_url)
                    InitNextImg(data)    
                }
                $("#first_name").text(data.first_name)
                $("#last_name").text(data.last_name)
                
            });
            $("#parse_block__photo, #parse_block__name").animate({top: '+=1000'}, 0).animate({top: '-=500'}, 200);
        }
    })
}

let next_img;
function InitNextImg(data) {
    next_img = new Image();
    next_img.src = data.next_photo;
    next_img.id = 'vk_photo';
    next_img.className = 'parse_block__img';
}

$(document).ready(AjaxParseVk(false));


$("#female_btn, #male_btn").click(function() {
    $("#female_btn, #male_btn").removeClass("active")
    $(this).toggleClass("active")
});


