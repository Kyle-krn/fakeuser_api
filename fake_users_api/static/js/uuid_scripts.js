$(function(){
    AjaxReceivedUUID()
    $("#uuidv1_btn_id," + 
      "#uuidv4_btn_id," +
      "#empty_btn_id").click(function(){
        if ($(this).hasClass("active")) return;
        $("#uuidv1_btn_id,#uuidv4_btn_id,#empty_btn_id").removeClass("active")
        $(this).addClass('active')
        RefreshUUID()
    });

    $(document).on('click', '#icon_copy', function(event){
        Copy($(".received_block__text span"))
        Alert("Copyied!")
    });

    $(document).on('click', '#icon_refresh', ClickRefresh)
    let deg = 0
    function ClickRefresh() {
        if (!$(".received_block__text span").queue().length){
            RefreshUUID()
            deg += 180;
            $(this).css('transform', `rotate(${deg}deg)`);
        };
    };


    $('#uuid1_download_id, #uuid4_download_id').click(function(){
        let version = $(this).attr('data');
        let divs_uuid = $(`#uuid${version}_body_id`).children();
        let text = '';
        if (!divs_uuid.length) {
            let count = $(`#uuid${version}_input_id`).val()
            $.ajax({
                url: '/generators/ajax_uuid/',
                traditional: true,
                async: false,
                data: {count:count, version: version},
                dataType: 'json',
                success: function(data){
                    text = data.results.join('\n')
                }
                })
        } else {
            $.each(divs_uuid, function(index, value){
                text += value.textContent + '\n'
            })
        }
        this.href = 'data:text/plain;charset=utf-11,' + encodeURIComponent(text);
    })


    $('#uuid1_input_id, #uuid4_input_id').on('input keyup', function(){
        if ($(this).val() < 1) {
            $(this).val(1)
        } else if ($(this).val() > 100) {
            $(this).val(100)
        }
    })

    function RefreshUUID(){
        let active_id = $("#uuidv1_btn_id.active,#uuidv4_btn_id.active,#empty_btn_id.active").attr('id')
        if (active_id == "uuidv4_btn_id") {
            AjaxReceivedUUID(1, 4)
        } else if (active_id == "uuidv1_btn_id") {
            AjaxReceivedUUID(1, 1)
        } else {
            AnimateRecivedBlock()
        }
    }

})

function CopyUUIDBlock(version){
    Copy($(`#uuid${version}_body_id`))
    Alert("Copyied!")
}

function ClearUUIDBlock(version){
    $(`#uuid${version}__body__control_id`).css('display', 'none')
    $(`#uuid${version}_body_id`).empty()
    if (!$('#uuid1_body_id, #uuid4_body_id').text()) $('.generate__uuid').css('align-items', '')
}

function MultipleButton(version){
    let count = $(`#uuid${version}_input_id`).val()
    $(`#uuid${version}__body__control_id`).css('display', 'block')
    AjaxReceivedUUID(count, version, true)
}

function AjaxReceivedUUID(count=1, version=4, multiple=false){
    GetAJAX(url="/generators/ajax_uuid/", 
            data={count: count, version: version}).done(function (data) {
                if (multiple){
                    MultipleRecived(version, data.results)
                } else {
                    AnimateRecivedBlock(data.results[0]);
                }
    })
}

function AnimateRecivedBlock(result){
    if (result == undefined) result = "00000000-0000-0000-0000-000000000000"
    let received_block = $(".received_block__text span")
    received_block.animate({top: '-=100'}, 200, function(){
        $(".received_block__text span").text(result);
    })
    received_block.animate({top: '+=200'}, 0).animate({top: '-=100'}, 200)
}

function MultipleRecived(version, results){
    let multiple_block = $(`#uuid${version}_body_id`)
    multiple_block.empty()
    $('.generate__uuid').css('align-items', 'flex-start')
    $.each(results, function (index, value) {
        multiple_block.append($('<div class="uuid__result"></div>').text(value))
    })
}

