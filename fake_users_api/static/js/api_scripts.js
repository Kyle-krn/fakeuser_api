$(".list").click(UserPanelClick)

function UserPanelClick() {
  $(".list").removeClass("active");
  $(this).addClass("active");
  let data = $(this).attr('data'); 
  UserPanelText(data)
}

function UserPanelText(data) {
    if (data == 'name') {
        $('#info__subtitle').text('Hi, my name is');
        $('#info__text').text(user_data.name.first_name + " " + user_data.name.last_name);
      } else if (data == 'email') {
        $('#info__subtitle').text('My email is')
        $('#info__text').text(user_data.email)
      } else if (data == 'bday') {
        $('#info__subtitle').text('My birthday is')
        $('#info__text').text(user_data.dob.date)
      } else if (data == 'address') {
        $('#info__subtitle').text('My address is')
        $('#info__text').text(user_data.location.street + " " + user_data.location.house)
      } else if (data == 'phone') {
        $('#info__subtitle').text('My phone is')
        $('#info__text').text(user_data.phone)
      } else if (data == 'password') {
        $('#info__subtitle').text('My password is')
        $('#info__text').text(user_data.login.password)
      }
}

$(document).ready(UserApiAjax());

$('.user__photo').click(UserApiAjax)

let user_data; 
function UserApiAjax() {
      GetAJAX(url="api/").done(function (data) {
        // $('span#uuid').text(data.results[0])
        user_data = data.results[0];
        $('#info__text').text(user_data.name.first_name + " " + user_data.name.last_name);
        $('#user_photo_id').attr('src', user_data.photo.medium);
        UserPanelText($('.list.active').attr('data'));
    })
}

$('#btn_code_jquery, #btn_code_js, #btn_code_python').click(function(){
  let active_id = $(this).attr('id')
  $('#btn_code_jquery, #btn_code_js, #btn_code_python').removeClass('active');
  $(this).addClass('active');
  $('.code__jquery, .code__js, .code__python').css('display', 'none')
  if (active_id == 'btn_code_jquery') {
    $('.code__jquery').css('display', 'block')
  } else if (active_id == 'btn_code_js') {
    $('.code__js').css('display', 'block')
  } else if (active_id == 'btn_code_python') {
    $('.code__python').css('display', 'block')
  }
})

$("#btn_code_copy").click(function(){
  let btn_code = $('#btn_code_jquery.active, #btn_code_js.active, #btn_code_python.active')
  active_id = btn_code.attr('id')
  if (active_id == 'btn_code_jquery') {
    Copy($('.code__jquery'))
  } else if (active_id == 'btn_code_js') {
    Copy($('.code__js'))
  } else if (active_id == 'btn_code_python') {
    Copy($('.code__python'))
  }
  Alert('Copyied!')
})

$('.collapse_btn').click(function(){
  let collapse_block = $(this).next();
  let maxHeight = parseInt(collapse_block.css('maxHeight'));
  let svg = $(this).children("svg")
  if (maxHeight) {
    collapse_block.css({'maxHeight': 0, 'padding': '0 16px'})
    svg.css('transform', 'rotate(0deg)')
  } else {
    collapse_block.css({'maxHeight': 151+(24*3), 'padding': '24px 16px'})
    svg.css('transform', 'rotate(180deg)')
  }
  })


$('.navigation__link').click(function(){
    let collapse_block = $('.navigation__block')
    let svg = $('#collapse_img_id')
    collapse_block.css({'maxHeight': 0, 'padding': '0 16px'})
    svg.css('transform', 'rotate(0deg)')

})
