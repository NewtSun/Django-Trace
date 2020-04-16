import random

from django import forms
from web import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from utils.tencent.sms import send_sms_single
from django_redis import get_redis_connection


class RegisterModelForm(forms.ModelForm):
    mobile_phone = forms.CharField(label='手机', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])
    password = forms.CharField(label='密码', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='重复密码', widget=forms.PasswordInput())
    code = forms.CharField(label='验证码', widget=forms.TextInput())

    class Meta:
        model = models.UserInfo
        fields = ['username', 'email', 'password', 'confirm_password', 'mobile_phone', 'code']

    # 智商税啊啊啊啊，这里的def在第一个class的里面，不是第二个的里面啊啊啊啊啊
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入%s' % (field.label, )


class SendSmsForm(forms.Form):
    mobile_phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_mobile_phone(self):
        """手机号校验钩子"""
        mobile_phone = self.cleaned_data['mobile_phone']

        # 判断短信模板是否有问题
        tpl = self.request.GET.get('tpl')
        template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
        print("获取不到吗"+self.data.get('tpl'))
        if not template_id:
            return ValidationError('短信模板错误')

        # 校验数据库中是否有手机号
        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if exists:
            raise ValidationError('手机号已存在')

        # 发短信 写Redis
        code = random.randrange(1000, 99999)
        sms = send_sms_single(mobile_phone, template_id, [code, ])
        if sms['result'] != 0:
            raise ValidationError("短信发送失败,{}".format(sms['errmsg']))

        # 验证码写入Redis
        conn = get_redis_connection()
        conn.set(mobile_phone, code, ex=60)

        return mobile_phone
