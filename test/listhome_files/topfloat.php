var topNavFrom = 'topfloat';
var topNavWidth = '980';


var jsFileName = "topfloat.php";
var rName = new RegExp(jsFileName+"(\\?(.*))?$")
var jss=document.getElementsByTagName('script');
for (var i = 0;i < jss.length; i++){
  var j = jss[i];
  if (j.src&&j.src.match(rName)){
    var oo = j.src.match(rName)[2];
    if (oo&&(t = oo.match(/([^&=]+)=([^=&]+)/g))){
        for (var l = 0; l < t.length; l++){
            r = t[l];
            var tt = r.match(/([^&=]+)=([^=&]+)/);
            if (tt)  {
				if (tt[1]=='from')
					topNavFrom = tt[2];
				if (tt[1]=='width')
					topNavWidth = tt[2];
			}
        }
    }
	break;
  }
}

$.ajax({
	url: "//www.120ask.com/v/topfloat.php?from="+topNavFrom+"&width="+topNavWidth,
  xhrFields:{withCredentials : true},
	success:function(data){
		$('body').prepend(data);
		if($("#d_mymes_sum").text()=="(0)"){
			//获取我的消息数
			$.getJSON("//www.120ask.com/member/msgnum/?callback=?",function(data){
				getMsg(data);
			});
			//同步登录
			$.getJSON("//a.120ask.com/asksycact?jsoncallbak=?",function(e){});
		}
	}
});


//消息调用
/*********************************************************************/
function getMsg(data){
		if(!data){
			$("#d_mymes_sum").html("（0）");
			return false;
		}
		if(data['status']=="success"){
			$("#d_mymes_sum").html("（"+data['data']['all_total']+"）");
		}
}
/************************************************************/

function loginOut(){
	document.domain = '120ask.com';
	//退出
	var diva = document.getElementById("top_show_info");
	diva.innerHTML="<li>正在退出...</li>";
	$('#top_show_info').css("color","#3C8F00");

	var date=new Date();
	date.setTime(date.getTime()-10000);
	$.getJSON("//a.120ask.com/unifyreg?jsoncallback=?",{mark:'logout',outtype:'net'},function(msg){
		if(msg['result'] == 'yes'){
			var syn = msg['data']['getucjs'];
			$("#synLoginOut").html(syn);
			$("#yesLogin").css('display','none');
			$("#noLogin").css('display','block');
			
			$.getJSON('//sso.120ask.com/api/sync/logout?jsoncallback=?',{source:'ask'},function(d){});

			var topurl = window.top.location.href;

			var i = topurl.indexOf('.120ask.com/user');
			if( i >= 0 ){
				setTimeout(function(){window.top.location.href="http://www.120ask.com"},2000);
				return false;
			}
			setTimeout(function(){document.location.reload();},2000);
			return false;
		}
	})
	setTimeout(function(){document.location.reload();},2000);
}

function loginurl()
{
	var topurl = top.location.href;
	var url = '//sso.120ask.com/user/login?source=ask&forward='+topurl;
	top.location.href=url;
}

function get_reg_url_(){
	var topurl = top.location.href;
	var url = '//sso.120ask.com/user/register?source=ask&forward='+topurl;
	top.location.href=url;
}

function strdecode(str){
         return utf8to16(base64encode(str));
}

function utf8to16(str) {
     var out, i, len, c;
     var char2, char3;

     out = "";
     len = str.length;
     i = 0;
     while(i < len) {
         c = str.charCodeAt(i++);
         switch(c >> 4)
         {
           case 0: case 1: case 2: case 3: case 4: case 5: case 6: case 7:
             // 0xxxxxxx
             out += str.charAt(i-1);
             break;
           case 12: case 13:
             // 110x xxxx    10xx xxxx
             char2 = str.charCodeAt(i++);
             out += String.fromCharCode(((c & 0x1F) << 6) | (char2 & 0x3F));
             break;
           case 14:
             // 1110 xxxx   10xx xxxx   10xx xxxx
             char2 = str.charCodeAt(i++);
             char3 = str.charCodeAt(i++);
             out += String.fromCharCode(((c & 0x0F) << 12) |
                                            ((char2 & 0x3F) << 6) |
                                            ((char3 & 0x3F) << 0));
             break;
         }
     }

     return out;
}
var base64EncodeChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
function base64encode(str) {
     var out, i, len;
     var c1, c2, c3;

     len = str.length;
     i = 0;
     out = "";
     while(i < len) {
         c1 = str.charCodeAt(i++) & 0xff;
         if(i == len)
         {
             out += base64EncodeChars.charAt(c1 >> 2);
             out += base64EncodeChars.charAt((c1 & 0x3) << 4);
             out += "==";
             break;
         }
         c2 = str.charCodeAt(i++);
         if(i == len)
         {
             out += base64EncodeChars.charAt(c1 >> 2);
             out += base64EncodeChars.charAt(((c1 & 0x3)<< 4) | ((c2 & 0xF0) >> 4));
             out += base64EncodeChars.charAt((c2 & 0xF) << 2);
             out += "=";
             break;
         }
         c3 = str.charCodeAt(i++);
         out += base64EncodeChars.charAt(c1 >> 2);
         out += base64EncodeChars.charAt(((c1 & 0x3)<< 4) | ((c2 & 0xF0) >> 4));
         out += base64EncodeChars.charAt(((c2 & 0xF) << 2) | ((c3 & 0xC0) >>6));
         out += base64EncodeChars.charAt(c3 & 0x3F);
     }
     return out;
}

function openPage(webHost,i){
	window.open("http://"+webHost+".120ask.com/"+i);
}
