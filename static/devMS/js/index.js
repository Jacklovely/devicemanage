//菜单的切换
function changeMenu(e){
	e = e || window.event;

		if(e.target.id == "searchDevices"){
			session = $.cookie('session');
			var host = window.location.host;
			var url = host + "/mobiledevice/index/0-0-0-0-0-0/1";
			window.location.href="http://" + url;

		}else if(e.target.id == "addDevices"){
			session = $.cookie('session');
			var host = window.location.host;
			var url = host + "/mobiledevice/adddevice/";
			window.location.href="http://" + url;
            // alert(e)
            // e.removeClass("setting_label");
            // e.addClass("setting_label menu_selected");
            // e.siblings().removeClass("setting_label menu_selected");
            // e.siblings().addClass("setting_label");

		}else if(e.target.id == "manDevices"){
			session = $.cookie('session');
			var host = window.location.host;
			var url = host + "/mobiledevice/manadevice/0-0-0-0-0-0/1";
			window.location.href="http://" + url;

		}else if(e.target.id == "checkDevices"){
			session = $.cookie('session');
			var host = window.location.host;
			var url = host + "/mobiledevice/checkDevice/";
			window.location.href="http://" + url
		}else if(e.target.id == "logMan"){
			session = $.cookie('session');
			var host = window.location.host;
			var url = host + "/mobiledevice/log/";
			window.location.href="http://" + url;
		}else if(e.target.id == "aboutPage"){
			session = $.cookie('session');
			var host = window.location.host;
			var url = host + "/mobiledevice/aboutPage/";
			window.location.href="http://" + url;

		}
}

