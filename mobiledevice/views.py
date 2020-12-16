#引入python core包
from datetime import datetime
import json
import os

#引入django包
from django.shortcuts import render,HttpResponse,redirect
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.core import serializers
from django.core.paginator import Paginator

# 项目包
from createdatabase import models

from devicemanage.settings import BASE_LOG_DIR
from mobiledevice.forms import LoginForm,SignUpForm,DeviceForm,SearchDeviceForm

# Create your views here.
# 注册
def signup(request):
    if request.method == 'GET':
        signupform=SignUpForm()
        return render(request, 'signup.html', {'signup_form':signupform})
    elif request.method=='POST':
        signupform = SignUpForm(request.POST)
        u = request.POST.get('user_name')
        # l = request.POST.get('login_name')
        p = request.POST.get('password')
        rep=request.POST.get('repassword')


        usr_exist=models.Users.objects.filter(user_name=u)
        #判断用户已存在
        if usr_exist:
            return render(request, 'signup.html', {'signup_form': signupform,'error_message':'用户名已存在'})
        #判断密码是否相同
        elif p!=rep:
            return render(request, 'signup.html', {'signup_form': signupform, 'error_message': '两次密码不一致'})
        #提交数据库
        elif signupform.is_valid():
            signupform.cleaned_data.pop('repassword')
            models.Users.objects.create(**signupform.cleaned_data)
            # models.Users.objects.create(user_name=u,password=p)
            request.session['username'] = u
            request.session['is_login'] = True
            wlog('恭喜' + u + '，注册成功，成为系统用户！\n')
            return redirect('/mobiledevice/index/0-0-0-0-0-0/1')


    else:
        signupform = SignUpForm()
        return render(request, 'signup.html', {'signup_form': signupform})


# 登录，需要csrf
@csrf_protect
def login(request):
    if request.method=='GET':
        lf=LoginForm()
        return render(request,'login.html',{'login_form':lf})
    elif request.method=='POST':
        lf=LoginForm(request.POST)
        u=request.POST.get('user_name')
        p=request.POST.get('password')
        userobj=models.Users.objects.all().filter(user_name=u, password=p)
        if userobj:
            login_name = models.Users.objects.all().filter(user_name=u).values('login_name').first()
            request.session['username'] =login_name['login_name']
            request.session['is_login'] = True
            # request.session.set_expiry(10)  设置超时
            wlog('欢迎系统用户' + login_name['login_name'] + '登录系统!\n')
            return redirect('/mobiledevice/index/0-0-0-0-0-0/1')

        else:
          return render(request,'login.html',{'error_message':'用户或密码错误', 'login_form':lf})
    else:
        lf = LoginForm()
        return render(request, 'login.html', {'login_form': lf})


# 登录成功，查询列表
def index(request,**kwargs):
    if request.session.get('is_login'):
        searchDeviceform = SearchDeviceForm()

        if request.method == 'GET':
            condition={}
            for k,v in kwargs.items():
                if v!='0':
                    condition[k]=v
                    if k=='borrower':
                        condition_brrower = condition['borrower']
                        del condition['borrower']
                        # del condition['pindex']
                        deviceobj=models.Devices.objects.filter(**condition,borrower__contains=condition_brrower)  #__contains代表模糊查询
                        deviceobjlist = pageInfo(deviceobj, kwargs['pindex'])
                        deviceInfo=serializers.serialize("json",deviceobj)
                        return render(request, 'index.html', {'deviceobj':deviceobjlist,'searchDeviceform':searchDeviceform,'deviceInfo':deviceInfo})
            del condition['pindex']
            deviceobj=models.Devices.objects.filter(**condition)
            deviceobjlist = pageInfo(deviceobj, kwargs['pindex'])
            deviceInfo=serializers.serialize("json",deviceobj)
            return render(request, 'index.html', {'deviceobj':deviceobjlist,'searchDeviceform':searchDeviceform,'deviceInfo':deviceInfo})


        elif request.method == 'POST':
            ret={'status':True,'data':None}
            try:
                br = request.POST.get('borrower')
                deviceid = request.POST.get('id')
                nowtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                models.Devices.objects.filter(id=deviceid).update(borrower=br, borrow_time=nowtime,status='2')
                deviceQuery=models.Devices.objects.filter(id=deviceid).values_list('device_name','theNum','version').first()
                wlog(br + '借用了设备：' + deviceQuery[0] + '--->' + deviceQuery[1] + '------>系统版本为' + deviceQuery[2] + '\n')
            except Exception as e:
                ret['status']=False

            return HttpResponse(json.dumps(ret))

    else:
        return redirect('/mobiledevice/login/')


# 退出
def logout(request):
    u = request.session.get('username')
    wlog('%s退出了系统!\n'%u)
    request.session.clear()
    return redirect('/mobiledevice/login/')


#添加设备
def adddevice(request):
    if request.session.get('is_login'):
        if request.method=='GET':
            deviceform=DeviceForm()
            return render(request, 'adddevice.html', {'deviceform':deviceform})
        elif request.method=='POST':
            deviceform=DeviceForm(request.POST,request.FILES)
            if deviceform.is_valid():
                #向数据库devices表添加数据
                deviceform.cleaned_data.pop('path')
                deviceform.cleaned_data.pop('apply_path')
                deviceform.cleaned_data['borrower']=''
                deviceform.cleaned_data['borrow_time']=''
                deobj= models.Devices.objects.create(**deviceform.cleaned_data)
                #向数据库dev_imgs表添加数据
                img_url=request.FILES.get('path')
                apply_url=request.FILES.get('apply_path')
                models.Dev_imgs.objects.create(device_id_id=deobj.id,path=img_url,apply_path=apply_url)
                device_name = deviceform.cleaned_data.get('device_name')
                wlog(request.session.get('username') + '添加了设备：' + device_name+'\n')
                return redirect('/mobiledevice/index/0-0-0-0-0-0/1')
    else:
        return redirect('/mobiledevice/login/')

#查看设备详细信息
def deviceInfo(request,*args):
    device=models.Devices.objects.filter(id=args[0]).first()
    return render(request,'deviceInfo.html',{'device':device})

#管理设备
def manadevice(request,**kwargs):
    if request.session.get('is_login'):
        searchDeviceform = SearchDeviceForm()
        # condition_brrower = ''
        if request.method == 'GET':
            condition={}
            for k,v in kwargs.items():
                if v!='0':
                    condition[k]=v
                    if k=='borrower':
                        condition_brrower = condition['borrower']
                        del condition['borrower']
                        deviceobj=models.Devices.objects.filter(**condition,borrower__contains=condition_brrower)  #__contains代表模糊查询
                        deviceobjlist = pageInfo(deviceobj, kwargs['pindex'])
                        deviceInfo=serializers.serialize("json",deviceobj)
                        return render(request, 'manadevice.html',
                                      {'deviceobj': deviceobjlist, 'searchDeviceform': searchDeviceform,
                                       'deviceInfo': deviceInfo})
            del  condition['pindex']
            deviceobj=models.Devices.objects.filter(**condition)
            deviceInfo=serializers.serialize("json",deviceobj)
            deviceobjlist = pageInfo(deviceobj, kwargs['pindex'])
            return render(request, 'manadevice.html',
                      {'deviceobj': deviceobjlist, 'searchDeviceform': searchDeviceform,
                       'deviceInfo': deviceInfo})

        elif request.method == 'POST':
            br = request.POST.get('borrower')
            deviceid = request.POST.get('deviceId')
            deviceQuery=models.Devices.objects.filter(id=deviceid).values_list('device_name','theNum','version').first()

            try:
                ret={'status':True,'data':None}
                if request.POST.get('method')=='apply':
                    nowtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    models.Devices.objects.filter(id=deviceid).update(borrower=br, borrow_time=nowtime,status='2')
                    wlog(br+'借用了设备：'+deviceQuery[0]+'--->'+deviceQuery[1]+'------>系统版本为'+deviceQuery[2]+'\n')
                elif request.POST.get('method')=='confirmReturned':
                    models.Devices.objects.filter(id=deviceid).update(borrower=None,status='1',borrow_time=None)
                    wlog(br+'归还了设备：'+deviceQuery[0]+'--->'+deviceQuery[1]+'------>系统版本为'+deviceQuery[2]+'\n')
                elif request.POST.get('method')=='delDevice':
                    device_name=models.Devices.objects.filter(id=deviceid).values('device_name').first()
                    # 删除服务器图片
                    img_url=models.Dev_imgs.objects.filter(device_id_id=deviceid).values('path').first()
                    img_url=img_url['path']
                    if img_url:
                        delPic(img_url)
                        # 删除数据库信息
                        models.Devices.objects.filter(id=deviceid).delete()
                    else:
                        models.Devices.objects.filter(id=deviceid).delete()
                    wlog(request.session.get('username')+'删除了设备'+device_name['device_name']+'\n')
            except Exception as e:
                ret['status']=False

            return HttpResponse(json.dumps(ret))

    else:
        return redirect('/mobiledevice/login/')


# 修改设备信息
def modifydevice(request,*args):
    if request.session.get('is_login'):

        if request.method=='GET':
            deviceId = args[0]
            deviceObj=models.Devices.objects.filter(id=deviceId).first() #获取要修改的设备信息
            deviceDict=model_to_dict(deviceObj) #将设备信息转换成字典，因为下面initial的参数必须是字典类型
            devicePath = deviceObj.dev_imgs_set.values('path').first()#获取图片路径
            deviceApplyPath=deviceObj.dev_imgs_set.values('apply_path').first()#获取申请采购图片路径
            deviceform = DeviceForm(initial=deviceDict) #初始化表单，传入值
            return render(request,'modifydevice.html',{'deviceObj':deviceObj,'deviceform':deviceform,'path':devicePath['path'],'apply_path':deviceApplyPath['apply_path']})

        elif request.method=='POST':
            deviceform = DeviceForm(request.POST, request.FILES)
            did=request.POST.get('deviceid')
            if deviceform.is_valid():
                # 如果path为空，证明没有更新图片信息
                if deviceform.cleaned_data.get('path') == None and deviceform.cleaned_data.get('apply_path') == None:
                    changeinfo(deviceform, did)

                elif deviceform.cleaned_data.get('path') != None and deviceform.cleaned_data.get('apply_path') == None:
                # 更新图片信息
                    changeimg(request, did)
                # 更新其他设备信息
                    changeinfo(deviceform, did)


                elif deviceform.cleaned_data.get('path') == None and deviceform.cleaned_data.get('apply_path') != None:
                # 更新申请采购图片信息
                    changeapplyimg(request, did)
                # 更新其他设备信息
                    changeinfo(deviceform, did)
                else:
                # 更新图片信息
                    changeimg(request, did)
                # 更新申请采购图片信息
                    changeapplyimg(request, did)
                # 更新其他设备信息
                    changeinfo(deviceform, did)


            wlog(request.session.get('username') + '修改了设备' + deviceform.cleaned_data.get('device_name')+'\n')
            return redirect('/mobiledevice/manadevice/0-0-0-0-0-0/1')

    else:
        return redirect('/mobiledevice/login/')

# 查询日志
def checklog(request):
    loglist=rlog()
    return render(request,'log.html',{'logobj':loglist})

# 关于系统
def aboutPage(request):
    return render(request,'aboutPage.html')



#删除服务器上存储的图片
def delPic(img_url):
    d = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tu_jpg = os.path.join(d, "media/" + img_url)
    if os.path.isfile(tu_jpg):
        os.remove(tu_jpg)


#盘点设备
def checkDevice(request,*args):
    if request.session.get('is_login'):
        searchDeviceform = SearchDeviceForm()
        if request.method == 'GET':
            deviceobj=getDeviceObj(args[0])
            return render(request, 'checkdevice.html', {'deviceobj': deviceobj, 'searchDeviceform': searchDeviceform})
        elif request.method == 'POST':
            deviceid = request.POST.get('id')
            device_name = models.Devices.objects.filter(id=deviceid).values('device_name').first()
            try:
                ret={'status':True,'data':None}
                #盘点设备信息
                if request.POST.get('method')=='reSetDevice':
                    models.Devices.objects.filter(id=deviceid).update(check_dev='1')
                    wlog(request.session.get('username')+'盘点了设备'+device_name['device_name']+'\n')
                #重置设备信息
                elif request.POST.get('method')=='initialDevice':
                    deviceid=request.POST.get('id')
                    models.Devices.objects.filter(id=deviceid).update(check_dev='0')
                    wlog(request.session.get('username') + '重置了设备'+device_name['device_name']+'\n')
            except Exception as e:
                ret['status']=False

            return HttpResponse(json.dumps(ret))

    else:
        return redirect('/mobiledevice/login/')


#获取设备信息
def getDeviceObj(methodname):
    if methodname == 'getNoCheckedDevs':
        deviceobj = models.Devices.objects.filter(check_dev='0').all()
    elif methodname == 'getCheckedDevs':
        deviceobj = models.Devices.objects.filter(check_dev='1').all()
    elif methodname == 'initaillizeDevsStatus':
        models.Devices.objects.all().update(check_dev='0')
        deviceobj =models.Devices.objects.all()

    else:
        deviceobj = models.Devices.objects.all()

    return deviceobj



file_path=BASE_LOG_DIR+'/logread.txt'

#记录日志
def wlog(message):
    logfile=open(file_path,"a+", encoding='utf-8')
    logfile.seek(0)
    logLineNum=len(logfile.readlines())
    if logLineNum<50:
        logfile.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'----->'+message)
        if logLineNum ==49:
            logfile.close()
            save_old_file=file_path+'.'+datetime.now().strftime('%Y%m%d%H%M%S')
            os.rename(file_path,save_old_file)
            logfile = open(file_path, "a+")
            logfile.close()

#读取日志
def rlog():
    logfile=open(file_path,"r", encoding='utf-8')
    log_dic={}
    for key,value in enumerate(logfile,start=1):
        log_dic[key]=value
    return sorted(log_dic.items(),key=lambda item:item[0],reverse=True)


#修改页，更新除图片外，其他信息
def changeinfo(deviceform,did):
    deviceform.cleaned_data.pop('path')
    deviceform.cleaned_data.pop('apply_path')
    # 更新设备信息
    models.Devices.objects.filter(id=did).update(**deviceform.cleaned_data)

#修改页，更新图片信息
def changeimg(request,did):
    img_url_old = models.Dev_imgs.objects.filter(device_id_id=did).values('path').first()
    img_url_old = img_url_old['path']
    delPic(img_url_old)
    img_url = request.FILES.get('path')
    imgobj = models.Dev_imgs.objects.get(device_id_id=did)
    imgobj.path = img_url
    imgobj.save()

#修改页，更新申请图片信息
def changeapplyimg(request,did):
    apply_img_url_old = models.Dev_imgs.objects.filter(device_id_id=did).values('apply_path').first()
    apply_img_url_old = apply_img_url_old['apply_path']
    delPic(apply_img_url_old)
    apply_img_url = request.FILES.get('apply_path')
    applyimgobj = models.Dev_imgs.objects.get(device_id_id=did)
    applyimgobj.apply_path = apply_img_url
    applyimgobj.save()

#分页信息
def pageInfo(deviceobjlist,pindex):
    paginator = Paginator(deviceobjlist, 10)
    if pindex == "":  # django中默认返回空值，所以加以判断，并设置默认值为1
        pindex = 1
    else:# 如果有返回在值，把返回值转为整数型
        int(pindex)
    page_device_list=paginator.page(pindex)

    return page_device_list
