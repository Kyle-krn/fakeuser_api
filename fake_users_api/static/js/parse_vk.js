
let next_img;
function AjaxParseVk() {
    $.ajax({
        crossdomain: true,
        url: 'http://127.0.0.1:8000/parse/get_member_group/',         /* Куда отправить запрос */
        method: 'GET',             /* Метод запроса (post или get) */
        dataType: 'json',          /* Тип данных в ответе (xml, json, script, html). */
        success: function(data){   /* функция которая будет выполнена после успешного запроса.  */
            $("#vk_photo").attr("src", data.photo)
            next_img = new Image()
            next_img.src = data.next_photo
            console.log(next_img)
            
            
        }
    })

    
}

function Next() {
    $("#vk_photo").replaceWith(next_img)
}

AjaxParseVk()