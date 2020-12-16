var host = window.location.host;

//申请设备，修改签借人
function applyFor(e) {
    e = e || window.event;
    //获取被点击元素的id对应的input元素的id
    inputId = "input_" + e.target.id;
    deviceId = e.target.id;
    device = document.getElementById(deviceId);
    dversion = device.getAttribute("dversion");

    if (document.getElementById(inputId).value == "") {
        alert("申请人不能为空！");
    } else {
        var borrower = document.getElementById(inputId).value;
        alert("请确定系统版本号是否为 "+dversion+" 吗？如果不是请联系管理员");
        $.ajax({
            type: "post",
            url: window.location.href,
            data: {deviceId: deviceId, borrower: borrower, method: "apply"},
            success: function (data) {
                var obj = JSON.parse(data);
                if (obj.status) {
                    location.reload();
                }else{
                    alert("申请失败");
                }
            }
        });
    }

}

//取消申请设备
function cancleApplyFor(e){
	e = e || window.event;
	//获取被点击元素的id
	deviceId = e.target.id;
	deviceName = $("#label_" + e.target.id).text();
	$.ajax({
        type: "get",
        url: "http://" + host + "/index.php/ManageDev/cancleApplyForDev",
        data: {"id":deviceId,"device_name":deviceName},
        success: function (result) {
          if(result == "scuess"){
            	//alert(result);
            	location.reload(); 
            }else{
           		alert("取消申请失败");
           	}
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

function searchDevs(e){
	e = e || window.event;
	id = e.target.id;
	// session = $.cookie('session');

	dev_plateform = $("#dev_plateform").val();
	dev_brand = $("#dev_brand").val();
	dev_version = $("#dev_version").val();
	dev_status = $("#dev_status").val();
	dev_category = $("#dev_category").val();
	borrower = $("#borrower").val();
	if (borrower ==''){
        borrower="0"
	}
	var url ="http://"+host+"/mobiledevice/manadevice/";
    window.location.href=url+dev_plateform+"-"+dev_brand+"-"+dev_version+"-"+dev_status+"-"+dev_category+"-"+borrower+"/1";
}

function exportDevs(deviceInfo){
      var deviceInfodata=[]

      for (i=0;i<deviceInfo.length;i++) {
          deviceInfodata.push(deviceInfo[i]["fields"])
      }
      var title=["设备名","设备型号","设备编号","平台(1:android2:ios)","品牌","所属者","状态(1:未借出2:已借出)",
          "签借人","UUID","备注", "分类(1:手机2:平板3:其他)","盘点设备(0:未盘点1:已盘点)","系统版本","设备保持状态(0:完好1:报废)","添加时间","借出时间"]
      exportExcel(deviceInfodata,"设备信息表",title)
}




//删除设备
function deleteDev(e){
	e = e || window.event;
	//获取被点击元素的id
    id= e.target.id;
	deviceId = id.substring(7);
	con=confirm("确定删除该设备么?");
	if(con == true){
		$.ajax({
	        type: "post",
	        url: window.location.href,
	        data: {"deviceId":deviceId,"method":"delDevice"},
	        success: function (data) {
	            var obj=JSON.parse(data)
                if(obj.status){
                    location.reload();
                }else{
                    alert("删除失败！");
                }
	      	  }
	       });
	}
}



//确认归还
function confirmReturned(e){

	e = e || window.event;
	//获取被点击元素的id
    id= e.target.id;
	deviceId= id.substring(7);
    var borrower=document.getElementById("input_"+deviceId).value

	$.ajax({
        type: "post",
        url: window.location.href,
        data: {"deviceId":deviceId,"method":"confirmReturned","borrower":borrower},
        success: function (data) {
          var obj=JSON.parse(data);
            	if(obj.status){
            		location.reload();
            	}else{
            		alert("归还失败");
            	}
      	  }
       });
      
}

function modifyDevice(e){
    e = e || window.event;
    id = e.target.id;
    deviceId=id.substring(7);
    url=host+"/mobiledevice/manadevice/deviceid="+deviceId
    window.location.href="http://" + url;

}








