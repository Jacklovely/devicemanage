var host = window.location.host;

//查询未盘点设备
function getNoCheckedDevs(){
	var url = "http://" + host + "/mobiledevice/checkDevice/getNoCheckedDevs";
	window.location.href=url
}

//查询已盘点
function getCheckedDevs(){
	var url = "http://" + host + "/mobiledevice/checkDevice/getCheckedDevs";
	window.location.href=url

}

//查询所有设备
function getAllDevs(){
	var url = "http://" + host + "/mobiledevice/checkDevice/";
	window.location.href=url
}


//重置设备状态
function initaillizeDevsStatus(){
	$.ajax({
        type: "get",
        url: "http://" + host + "/mobiledevice/checkDevice/initaillizeDevsStatus",
        data: {},
        success: function () {
        	  alert("重置成功，页面将跳转！");
        	  window.location.href="http://" + host + "/mobiledevice/checkDevice/getNoCheckedDevs";
      	  }
       });
}



//进入单个设备信息页面
function showDevInfo(e){
	e = e || window.event;
	id = e.target.id;
	deviceId = id.substring(5);
	window.location.href="http://" + host + "/mobiledevice/deviceInfo/" + deviceId;
}


//盘点单个设备
function confirmIsAt(e){
    e = e || window.event;
	id = e.target.id;
	deviceId = id.substring(9);
	$.ajax({
        type: "post",
        url: "http://" + host + "/mobiledevice/checkDevice/",
        data: {"id":deviceId,"method":"reSetDevice"},
        success: function (data) {
           obj= JSON.parse(data)
          if(obj.status){
        	  location.reload();
        }else{
               alert("操作失败，请重新尝试！");
           	}
      	  }
       });
}

//重置单个设备
function initaillizeTheDev(e){
	e = e || window.event;
	id = e.target.id;
	deviceId = id.substring(9);
	$.ajax({
        type: "post",
        url: "http://" + host + "/mobiledevice/checkDevice/",
        data: {"id":deviceId,"method":"initialDevice"},
        success: function (data) {
            obj=JSON.parse(data)
          if(obj.status ){
        	  location.reload();
        }else{
           		alert("操作失败，请重新尝试！");
           	}
      	  }
       });
}





