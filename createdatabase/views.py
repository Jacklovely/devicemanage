from django.shortcuts import render,HttpResponse
from createdatabase import models

# Create your views here.
def createdatabase(request):
    # 开始创建数据库
    models.Users.objects.create(user_name='admin',
                                login_name='admin',
                                password='admin',
                                role='0',
                                registe_time='',
                                login_time='',
                                icon='',
                                session='',
                                comments='超级管理员')
    return HttpResponse('create database succeed !')


def test(request):
    deviceobj = models.Devices.objects.filter(**{})

    print(deviceobj)


    return HttpResponse('ok')