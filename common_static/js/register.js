$(function(){
	var phonList = /^[1]([3-9])[0-9]{8}$/;


	//聚焦input
	$('input').eq(0).focus(function(){
		if($(this).val().length==0){
			$(this).parent().next("div").text("支持中文，字母，数字，'-'，'_'的多种组合");
		}
	});
	$('input').eq(1).focus(function(){
		if($(this).val().length==0){
		    $(this).parent().next("div").text("建议使用字母、数字和符号两种以上的组合，6-20个字符");
		}
	});
	$('input').eq(2).focus(function(){
		if($(this).val().length==0){
			$(this).parent().next("div").text("请再次输入密码");
		}
	});
	$('input').eq(3).focus(function(){
		if($(this).val().length==0){
			$(this).parent().next("div").text("验证完后，你可以使用该手机登陆和找回密码");
		}
	});
	$('input').eq(4).focus(function(){
		if($(this).val().length==0){
			$(this).parent().next().next("div").text("看不清？点击图片更换验证码");
		}
	});
	//input各种判断
	//用户名：
	$('input').eq(0).blur(function(){
		if($(this).val().length==0){
			$(this).parent().next("div").text("");
			$(this).parent().next("div").css("color",'#ccc');
		}else if($(this).val().length>0 && $(this).val().length<4){
			$(this).parent().next("div").text("长度只能在4-20个字符之间");
			$(this).parent().next("div").css("color",'red');
		}else if($(this).val().length>=4&& !isNaN($(this).val())){
			$(this).parent().next("div").text("用户名不能为纯数字");
			$(this).parent().next("div").css("color",'red');
		}else{
			$(this).parent().next("div").text("");
		}
	});
	//密码
	$('input').eq(1).blur(function(){
		if($(this).val().length==0){
			$(this).parent().next("div").text("");
			$(this).parent().next("div").css("color",'#ccc');
		}else if($(this).val().length>0 && $(this).val().length<6){
			$(this).parent().next("div").text("长度只能在6-20个字符之间");
			$(this).parent().next("div").css("color",'red');
		}else{
			$(this).parent().next("div").text("");
		}
	});
//	确认密码
	$('input').eq(2).blur(function(){
		if($(this).val().length==0){
			$(this).parent().next("div").text("");
			$(this).parent().next("div").css("color",'#ccc');
		}else if($(this).val()!=$('input').eq(1).val()){
			$(this).parent().next("div").text("两次密码不匹配");
			$(this).parent().next("div").css("color",'red');
		}else{
			$(this).parent().next("div").text("");
		}
	});
//	手机号
	$('input').eq(3).blur(function(){
		if($(this).val().length==0){
			$(this).parent().next("div").text("");
			$(this).parent().next("div").css("color",'#ccc');
		}else if((phonList.test($(this).val()))){
			$(this).parent().next("div").text("手机号格式不正确");
			$(this).parent().next("div").css("color",'red');
		}else{
			$(this).parent().next("div").text("");
		}
	});
//	 验证码刷新
	function code(){
		var str="qwertyuiopasdfghjklzxcvbnm1234567890QWERTYUIOPLKJHGFDSAZXCVBNM";
		var str1=0;
		for(var i=0; i<4;i++){
			str1+=str.charAt(Math.floor(Math.random()*62))
		}
		str1=str1.substring(1);
		$("#code").text(str1);
	}
	code();
	$("#code").click(code);
//	验证码验证
	$('input').eq(4).blur(function(){
		if($(this).val().length==0){
			$(this).parent().next().next("div").text("");
			$(this).parent().next().next("div").css("color",'#ccc');
		}else if($(this).val().toUpperCase()!=$("#code").text().toUpperCase()){
			$(this).parent().next().next("div").text("验证码不正确");
			$(this).parent().next().next("div").css("color",'red');
		}else{
			$(this).parent().next().next("div").text("");
		}
	});
	$('#username').focusout(function () {
		if ($(this).val().length > 0) {
			$.ajax({
				url: 'http://127.0.0.1:8000/user/validate_username/',
				type: 'get',
				data: {'name': $(this).val()},
				dataType: 'json',
				success:function (res) {
					res = JSON.parse(res);
					console.log(res.msg);
					$('#username').parent().next("div").text(res.msg);
					if (res.status != 200) {
						$('#username').parent().next("div").css('color', 'red');
					}else {
						$('#username').parent().next("div").css('color', '#00ff00');
					}
				}
			})
		}
	});
//	提交按钮
	$("#submit_btn").click(function(e){
		e.preventDefault();
		for(var j=0 ;j<5;j++){
			if($('input').eq(j).val().length==0){
				$('input').eq(j).focus();
				if(j==4){
					$('input').eq(j).parent().next().next("div").text("此处不能为空");
					$('input').eq(j).parent().next().next("div").css("color",'red');
					e.preventDefault();
					return;
				}
				$('input').eq(j).parent().next(".tips").text("此处不能为空");
				$('input').eq(j).parent().next(".tips").css("color",'red');
				e.preventDefault();
				return;
			}
		}

		if($("#xieyi")[0].checked){
			if ($('.tips').eq(1).text()==''&&$('.tips').eq(2).text()==''&&$('.tips').eq(3).text()==''&&$('.tips').eq(4).text()==''){
				var data = $("#add_user").serializeArray();
				var datas = {};
				for(var i = 0; i < data.length; i++){
					datas[data[i].name] = data[i].value;
				}
                $.ajax({
					url: 'http://127.0.0.1:8000/user/reg/',
					type: 'post',
					data: datas,
					dataType: 'json',
					success:function (res) {
						console.log(res);
						if (res.status == 200) {
							alert("注册成功");
							window.location.href = 'http://127.0.0.1:8000/'
						}
                    }
				});
			}else{
				alert("注册失败")
			}


		}else{
			$("#xieyi").next().next().next(".tips").text("请勾选协议");
			$("#xieyi").next().next().next(".tips").css("color",'red');
			e.preventDefault();
			return;
		}
	})

});