var host = 'http://127.0.0.1:8000';
// var host = 'http://www.huahua.com:8000';
// 获取cookie
// var username=getCookie('username')
function getCookie(name) {
    try {
        let r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
        return r ? r[1] : undefined;
	}catch(e) {
        console.log(e)   //Error: 出错啦！ at <anonymous>:2:8
    }
}
// 提取地址栏中的查询字符串
function get_query_string(name) {
    let reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
    let r = window.location.search.substr(1).match(reg);
    if (r != null) {
        return decodeURI(r[2]);
    }
    return null;
}
// 生成uuid
function generateUUID() {
    let d = new Date().getTime();
    if(window.performance && typeof window.performance.now === "function"){
        d += performance.now(); //use high-precision timer if available
    }
    let uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        let r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
    return uuid;
}

function get_carts(){
    var url = host + '/carts/simple/';
    let i=0
    axios.get(url,{
        responseType: 'json',
    }).then(response => {
        i = response.data.cart_total_count;
        $('#show_count').text(i)
    }).catch(error => {console.log(error.response);})
    return i
}

$(function(){
    var flag = true;
    var url = window.location.href
    var hour = new Date().getHours();//时
    var minute = new Date().getMinutes();//分
    var nowtime=(hour >= 10 ? hour:'0' + hour) + ':' + (minute >=10 ? minute:'0' + minute);
    var answers=[
            '您好，有什么可以帮到您的？',
            '欢迎光临<span style="color: #FA7181">huahua.com花里有话鲜花网</span>，我是机器人客服小花，很高兴为您服务！我们提供很多精美的鲜花、礼品款式，适用于各类鲜花赠送场景，24小时均可自助下单哦~',
            '<span style="font-weight: bold;margin-right: 8px;font-size: 15px;margin-bottom: 10px">常见问题:</br></span><a style="color: #FA7181">配送范围有哪些？</a></br><a style="color: #FA7181">送花是否可以选择具体配送时间？</a></br><a style="color: #FA7181">下单后多久可以送到？</a></br><a style="color: #FA7181">收到的鲜花是否跟网站图片一致？</a></br>建议您点击了解具体政策。',
            '抱歉，您咨询的问题我还在学习中，无法为您解答。'
        ];
    var toolTop = condition(url)
	toggleTool(toolTop); 	// 当-到达recomed时 显示电梯导航   调用 toggleTool 函数
    $('#fixedtool a').mouseenter(function(){
		var index = $(this).index();
		$(this).css("backgroundColor", "#F5F5F5");
		$("#fixedtool a span").eq(index).addClass("fonts_current")
		$("#fixedtool a").eq(index).addClass("fonts_current")
	}).mouseleave(function(){
		var index = $(this).index();
		$(this).css("backgroundColor", "#FFF");
		$("#fixedtool a span").eq(index).removeClass("fonts_current")
		$("#fixedtool a").eq(index).removeClass("fonts_current")
	});
    $('.contact').mouseenter(function (){
        $(".contact_show").css("display","block")
    }).mouseleave(function (){
        $(".contact_show").css("display","none")
    })
    function condition(url){
        if (url === 'http://127.0.0.1:8000/' ){
            return $(".function").offset().top
        }else if(url.slice(0,28)==='http://127.0.0.1:8000/detail'){
            return 0
        }else {return 999999}
    }

    function toggleTool(index) {
        if ($(document).scrollTop() >= index) {
            $("#fixedtool").fadeIn();
        } else {
            $("#fixedtool").fadeOut();
        };
    }
    $(window).scroll(function() {
        toggleTool(toolTop);
    })
    $(".reback").click(function() {
		flag = false;
		var current = $(".shortcut").offset().top;
        // 页面动画滚动效果
        $("body, html").stop().animate({
            scrollTop: current
        }, function() {
            flag = true;
        });
	});
    $('.servicer').click(function (){
        $('.server').addClass('aaa')
        setTimeout(function (){answer(answers[2])}, 900);
        setTimeout(function (){answer(answers[1])}, 1000);
	    setTimeout(function (){answer(answers[0])}, 1400);
    })
    $('.ser_close').click(function (){
        $('.server').removeClass('aaa')
    })
    function answer(str) {
        var answer='<div class="ser_con"><div class="ser_con_hd">机器人客服—小花<span>'+nowtime +
                '</span></div><div><div class="ser_chat_con"><p>'+str+'</p></div></div></div><div class="clearfix"></div>'
		$('.serbody').append(answer);
		$('.serbody').scrollTop($('.serbody')[0].scrollHeight);
	}
	$('.sendBtn').on('click',function() {
		var news = $('#dope').val();
		if (news == '') {
			alert('不能为空');
		}
		else {
			$('#dope').val('');
			var str = '';
			str += '<div class="user_con">' +
				'<div class="user_con_hd">'+username+'<span>'+nowtime+'</span></div>' +
				'<div class="user_con_bd"><div class="user_chat_con"><p>'+ news + '</p></div></div></div>';
			$('.serbody').append(str);
			$('.serbody').scrollTop($('.serbody')[0].scrollHeight);
			setTimeout(function (){answer(answers[3])}, 1000);
		}
	})
})
