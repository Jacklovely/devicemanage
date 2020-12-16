var host=window.location.host
//返回列表页
$("#cancleModifyDev").click(function(event){
    var url="http://"+host
    window.location.href=url+"/mobiledevice/manadevice/0-0-0-0-0-0/1"
})

//预览图片
$("#id_path").on("change",function () {
    var file=this.files[0];
    if(this.files&&file)
    {
        var reader=new FileReader();

        reader.onload=function (e) {
            $("#previewPic").attr('src',e.target.result);
        }
        reader.readAsDataURL(file);
    }

})

$("#id_apply_path").on("change",function () {
    var file=this.files[0];
    if(this.files&&file)
    {
        var reader=new FileReader();

        reader.onload=function (e) {
            $("#previewApplyPic").attr('src',e.target.result);
        }
        reader.readAsDataURL(file);
    }

})