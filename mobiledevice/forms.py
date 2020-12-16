from django import forms
from django.forms import widgets,ModelChoiceField
from createdatabase.models import Devices

class LoginForm(forms.Form):
      user_name=forms.CharField(required=True,label="登录名",error_messages={'required':'登录名不能为空'},
                                widget=widgets.TextInput(attrs={'class':'form-control'}))
      password=forms.CharField(required=True,
                                label="密码",
                                error_messages={'required': '密码不能为空',
                                                'max_length':'密码最大8位',
                                                'min_length':'密码最小4位'},
                                max_length=8,
                                min_length=4,
                                widget=widgets.PasswordInput(attrs={'class': 'form-control','placeholder': '请输入4-8位密码',}),

                                )

class SignUpForm(forms.Form):
    user_name = forms.CharField(required=True, label="登录名", error_messages={'required': '登录名不能为空'},
                                widget=widgets.TextInput(attrs={'style':'font-size:16px;height:25px;'}))
    login_name = forms.CharField(required=True, label="用户名", error_messages={'required': '用户名不能为空'},
                                 widget=widgets.TextInput(
                                attrs={'class': 'form-control', 'style': 'font-size:16px;height:25px;'}))

    password = forms.CharField(required=True,
                               label="密码",
                               # help_text='请输入4-8位密码',
                               error_messages={'required': '密码不能为空',
                                               'max_length': '密码最大8位',
                                               'min_length': '密码最小4位'},
                               max_length=8,
                               min_length=4,
                               widget=widgets.PasswordInput(attrs={'class': 'pwd','placeholder': '请输入4-8位密码','style':'font-size:16px;height:25px;'}),
                               )

    repassword=forms.CharField(required=True,
                               label="确认密码",
                               # help_text='请输入4-8位密码',
                               error_messages={'required': '用户名不能为空',
                                               'max_length': '密码最大8位',
                                               'min_length': '密码最小4位'},
                               max_length=8,
                               min_length=4,
                               widget=widgets.PasswordInput(attrs={'class': 'repwd','placeholder': '请输入4-8位密码','style':'font-size:16px;height:25px;'}),
                               )

class DeviceForm(forms.Form):
    plate_list=((1,'android'),(2,'ios'),)
    category_list=((1,'手机'),(2,'平板'),(3,'其他'),)
    device_name = forms.CharField(required=True,label="设备名",error_messages={'required':'设备名不能为空'},
                                  widget=forms.TextInput(attrs={'id':'dev_name', 'class':'form-control input_style'}))  # 设备名

    model = forms.CharField(label="型号",widget=forms.TextInput(attrs={'id':'dev_model','class':'form-control input_style'}))  # 设备型号

    theNum = forms.CharField(required=True,label="编号",error_messages={'required':'设备编号不能为空'},
                             widget=forms.TextInput(attrs={'id':'dev_num','class':'input_style form-control'}))  # 设备编号

    plateform = forms.IntegerField(label="平台",
                                   widget=forms.Select(choices=plate_list,
                                     attrs={'id':'dev_plateform','class':'input_style form-control'}))  # 平台android或者ios
    brand = forms.CharField(label="品牌",
                            widget=forms.TextInput(attrs={'id':"dev_brand",'class':'input_style form-control'}))  # 品牌

    owner = forms.CharField(label="所属",
                            initial="测试",
                            widget=forms.TextInput(attrs={'id':"dev_owner",'class':'input_style form-control'}))  # 分配出去的设备，行政借给谁了

    category = forms.IntegerField(label="设备分类",
                                  widget=forms.Select(choices=category_list,attrs={'id':'dev_category','class':'input_style form-control'}))  # 设备分类

    version = forms.CharField(label="系统版本",
                              # help_text='格式如：9.0.0',
                              widget=forms.TextInput(attrs={'id':'de_version','class':'input_style form-control','placeholder': '格式如：9.0.0'}))  # 系统版本

    UUID = forms.CharField(label="uuid",
                           required=False,
                           widget=forms.TextInput(attrs={'id':'de_UUID','class':'label_style form-control','style':'width:400px;'}))  # uuid

    comments = forms.CharField(label="备注",
                               required=False,
                               widget=forms.Textarea(attrs={'id':'dev_comments','class':'input_style form-control','style':'width:400px;height:150px;'}))  # 备注

    path=forms.ImageField(label="设备图片",required=False)

    apply_path=forms.ImageField(label="申请采购图片",required=False)


class SearchDeviceForm(forms.Form):
    choice = ((0, '请选择'),)
    plate_list = ((1, 'android'), (2, 'ios'),)+choice

    brandobj_list =Devices.objects.values('brand').distinct()
    # brandobj_list=tuple(brandobj_list)+choice

    versionobj_list=Devices.objects.all().values('version').distinct()
    # versionobj_list=tuple(versionobj_list)+choice

    status_list=((1,'未借出'),(2,'已借出'),)+choice
    category_list=((1,'手机'),(2,'平板'),(3,'其他'),)+choice

    #开始form表单构建

    plateform = forms.IntegerField(label='平台：',
                                   widget=forms.Select(choices=plate_list,
                                     attrs={'id':'dev_plateform','class':'select_style form-control'},
                                        ))  # 平台android或者ios

    brand=forms.ModelChoiceField(label='品牌：',
                                 queryset=brandobj_list,
                                 empty_label='请选择品牌',
                                widget=forms.Select(attrs={'id':'dev_brand','class':'select_style form-control'}),)

    version=forms.ModelChoiceField(label='系统版本：',
                               queryset=versionobj_list,
                               empty_label='请选择版本',
                                widget=forms.Select(attrs={'id':'dev_version','class':'select_style form-control'}))

    status=forms.IntegerField(label='状态：',
                              widget=forms.Select(choices=status_list,
                              attrs={'id':'dev_status','class':'select_style form-control'}))

    category=forms.IntegerField(label='分类：',
                              widget=forms.Select(choices=category_list,
                              attrs={'id':'dev_category','class':'select_style form-control','style':'margin-left:0px;'}))

    borrower=forms.CharField(label='签借人：',
                             widget=forms.TextInput(
                             attrs={'id':'borrower','class':'form-control select_style','style':'margin-left: 15px;'}))

    def __init__(self, *args, **kwargs):
        super(SearchDeviceForm, self).__init__(*args, **kwargs)
        self.initial["plateform"]=0
        self.initial["brand"]=0
        self.initial["version"]=0
        self.initial["status"]=0
        self.initial["category"]=0
        self.fields['brand'].choices = [('0','请选择')]+[x for x in Devices.objects.values_list('brand','brand').distinct()]
        self.fields['version'].choices = [('0','请选择')]+[x for x in Devices.objects.all().values_list('version','version').distinct()]

