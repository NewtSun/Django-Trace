from django.urls import path
from web.views import account

urlpatterns = [
    # 加name方便反向解析
    path('register/', account.register, name='register'),  # name='register'
    path('login/sms/', account.login_sms, name='login_sms'),
    path('send/sms/', account.send_sms, name='send_sms'),
]
