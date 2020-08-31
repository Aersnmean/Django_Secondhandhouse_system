
var code ; //在全局定义验证码
//产生验证码  
function createCode(){  
     code = "";   
     var codeLength = 4;//验证码的长度  
     var checkCode = document.getElementById("code");   
     var random = new Array(0,1,2,3,4,5,6,7,8,9,'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R',  
     'S','T','U','V','W','X','Y','Z');//随机数  
     for(var i = 0; i < codeLength; i++) {//循环操作  
        var index = Math.floor(Math.random()*36);//取得随机数的索引（0~35）  
        code += random[index];//根据索引取得随机数加到code上  
    }  
    checkCode.value = code;//把code值赋给验证码  
}  
//校验验证码  
function validate(){
    var data = $('#formlogin').serializeArray();
    var datas = {};
    for (var i = 0; i < data.length; i++) {
        datas[data[i].name] = data[i].value.replace(/(^s*)|(s*$)/g, "");
    }
    var inputCode = $('#authcode').val().replace(/(^s*)|(s*$)/g, "").toUpperCase(); //取得输入的验证码并转化为大写
    var loginmsg = document.getElementById("login-msg");
    if (datas['username'].length == 0) {
        loginmsg.innerText = "请输入用户名！";
    }
    else if(datas['password'].length == 0) {
        loginmsg.innerText = "请输入密码！";
    }
    else if(inputCode.length <= 0) { //若输入的验证码长度为0
        loginmsg.innerText = "请输入验证码！";
    }         
    else if(inputCode != code ) { //若输入的验证码与产生的验证码不一致时
        loginmsg.innerText = "验证码错误！";
        createCode();//刷新验证码  
        $('#authcode').val('');//清空文本框
    }         
    else { //输入正确时
        $.ajax({
            url: 'http://127.0.0.1:8000/user/log/',
            type: 'get',
            data: datas,
            dataType: 'json',
            success: function (res) {
                res = JSON.parse(res);
                if (res.status == 200){
                    window.location.reload();
                }else if (res.status == 405) {
                    $('#nloginpwd').val('');
                    $('#aa').val('');
                   loginmsg.innerText = res.msg;
                }
            }
        })
    }
}

function showlog() {
    $('#login-page, #allb').show();
    $('#username').focus();
}

function hidelog() {
    $('#login-page, #allb').hide();
}

function showreg() {
    window.open("http://127.0.0.1:8000/page/register.html/");
}

function is_login() {
    let name = $('.main_header_right ul li a').eq(2).text();
    if (name) {
        let li = $('.main_header_right ul li');
        li.eq(0).hide();
        li.eq(1).hide();
        li.eq(2).show();
        li.eq(3).show();
    }
}

function login_first(url) {
    let name = $('.main_header_right ul li a').eq(2).text();
    if (!name) {
        showlog();
    }
    else {
        window.open(url);
    }
}

function login_backhome() {
    let name = $('.main_header_right ul li a').eq(2).text();
    if (!name) {
        showlog();
    }
}

function logout() {
    $.ajax({
        url: 'http://127.0.0.1:8000/user/logout/',
        type: 'get',
        data: null,
        dataType: 'json',
        success: function (res) {
        }
    });
    window.location.reload();
}

// 检测是否登录
is_login();
// 显示验证码
$('#nloginpwd').on('focus', function () {
    createCode();
    $('#o-authcode').slideDown();
});


$("body").keydown(function() {
    if ($('#allb').css('display') != 'none') {
        if (event.keyCode == "13") {
            validate();
        }
    }
});

