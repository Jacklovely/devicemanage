"""devicemanage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from mobiledevice import views

urlpatterns = [
    path(r'login/', views.login),
    path(r'signup/',views.signup),
    path(r'logout/',views.logout),
    path(r'adddevice/',views.adddevice),
    re_path(r'index/(?P<plateform>\d+)-(?P<brand>\w+)-(?P<version>\d*\.*\d*\.*\d)-(?P<status>\d+)-(?P<category>\d+)-(?P<borrower>\w*)/(?P<pindex>\d+)',views.index),
    re_path(r'manadevice/(?P<plateform>\d+)-(?P<brand>\w+)-(?P<version>\d*\.*\d*\.*\d)-(?P<status>\d+)-(?P<category>\d+)-(?P<borrower>\w+)/(?P<pindex>\d+)',views.manadevice),
    re_path(r'manadevice/deviceid=(\d+)',views.modifydevice),
    re_path(r'checkDevice/(\w*)',views.checkDevice),
    path(r'log/',views.checklog),
    path(r'aboutPage/',views.aboutPage),
    re_path(r'deviceInfo/(\d+)',views.deviceInfo),

]




