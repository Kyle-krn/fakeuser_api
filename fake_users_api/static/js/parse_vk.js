
let parse_data;
let saved = false;
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
                    $("#vk_photo").attr("src", data.photo_400)
                    InitNextImg(data)    
                }
                $("#first_name").text(data.first_name)
                $("#last_name").text(data.last_name)
                
            });
            $("#parse_block__photo, #parse_block__name").animate({top: '+=1000'}, 0).animate({top: '-=500'}, 200);
            saved = false;
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




function GetGender(){
    let gender = $(".btn_block__gender .active").attr('name');
    return gender;
}

function SavePhotoAjax() {
    console.log(saved)
    let data = {
        user_id: parse_data.user_id,
        gender: GetGender()
    }

    if (data.gender == undefined) return Alert("Select gender!")

    if (saved == true) return Alert("Already saved!") 

    $.ajax({
        crossdomain: true,
        url: 'http://127.0.0.1:8000/parse/save_vk_photo/',         /* Куда отправить запрос */
        method: 'POST',             /* Метод запроса (post или get) */
        contentType: "application/json; charset=utf-8",
        dataType: 'json',          /* Тип данных в ответе (xml, json, script, html). */
        data: JSON.stringify(data),     /* Данные передаваемые в массиве */
        success: function(data){   /* функция которая будет выполнена после успешного запроса.  */
            Alert("Photo saved!")
            saved = true;
    }})
}