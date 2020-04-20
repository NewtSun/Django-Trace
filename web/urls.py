from django.urls import path
from web.views import account
from web.views import home
from web.views import project

urlpatterns = [
    # 加name方便反向解析
    path('register/', account.register, name='register'),  # name='register'
    path('login/sms/', account.login_sms, name='login_sms'),
    path('login/', account.login, name='login'),
    path('image/code/', account.image_code, name='image_code'),
    path('send/sms/', account.send_sms, name='send_sms'),
    path('index/', home.index, name='index'),
    path('logout/', account.logout, name='logout'),

    path('project/list', project.project_list, name='project_list')
]
