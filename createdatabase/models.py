from django.db import models
from django.urls import reverse

# Create your models here.

class Users(models.Model):
    user_name=models.CharField('用户名',max_length=64,default='guest')
    password=models.CharField(max_length=64)
    role=models.CharField(max_length=32,default=2) #0代表超级管理员，1代表普通管理员，2代表guest
    registe_time=models.DateTimeField(auto_now=True)
    login_time=models.CharField(max_length=64,default='Null')
    icon=models.CharField(max_length=64,default='/icon/default.png') #用户头像地址
    session=models.CharField(max_length=64) #登录后生产的随机字符串
    comments=models.CharField(max_length=64,default='游客')
    login_name=models.CharField(max_length=64,default='Null')

    class Meta:
        db_table = 'users'

    def __unicode__(self):
            return self.user_name

    def __str__(self):
        return self.user_name

class Devices(models.Model):
    id=models.AutoField(primary_key=True)
    device_name=models.CharField(max_length=64) #设备名
    model=models.CharField(max_length=64,default='Null') #设备型号
    theNum=models.CharField(max_length=64)            #设备编号
    plateform=models.CharField(max_length=64,default='Null') #平台android或者ios
    brand=models.CharField(max_length=64,null=True) #品牌
    owner=models.CharField(max_length=64,default='测试')#分配出去的设备，行政借给谁了
    status=models.CharField(max_length=64,default=1)# 1:未借出的状态；2：借出；0：申请中
    borrower=models.CharField(max_length=64,null=True)#借阅者
    UUID=models.CharField(max_length=64,null=True)#设备的UUID
    comments=models.CharField(max_length=64,null=True)#备注
    category=models.CharField(max_length=64,default='Null')#设备分类
    check_dev=models.CharField(max_length=64,default=0)#盘点设备的字段,0是未盘点，1是已盘点
    version = models.CharField(max_length=64, default='Null')#系统版本
    old_dev=models.CharField(max_length=64,default=0)#0表示设备是好的，1表示设备报废
    add_time=models.DateTimeField(auto_now_add=True) #添加设备的时间
    borrow_time=models.CharField(max_length=32,null=True)#借出设备的时间

    class Meta:
        db_table = 'devices'

    def __unicode__(self):
            return self.device_name

    def __str__(self):
        return self.device_name

class Dev_imgs(models.Model):
    device_id=models.ForeignKey('Devices',to_field='id',on_delete=models.CASCADE,default='Null')
    path=models.ImageField("图片",blank=True)
    apply_path=models.ImageField("申请采购图片",blank=True)

    class Meta:
        db_table = 'dev_imgs'

    def get_absolute_url(self):
        return reverse('pic_upload:pic_detail', args=[str(self.id)])

    def __unicode__(self):
        return self.device_id

    def __str__(self):
        return self.device_id


