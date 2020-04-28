from django.urls import path, include
from web.views import account
from web.views import home
from web.views import project
from web.views import manage

urlpatterns = [
    # 加name方便反向解析
    path('register/', account.register, name='register'),  # name='register'
    path('login/sms/', account.login_sms, name='login_sms'),
    path('login/', account.login, name='login'),
    path('image/code/', account.image_code, name='image_code'),
    path('send/sms/', account.send_sms, name='send_sms'),
    path('index/', home.index, name='index'),
    path('logout/', account.logout, name='logout'),

    path('project/list', project.project_list, name='project_list'),
    path('project/star/<project_type>/<project_id>/', project.project_star, name='project_star'),
    path('project/unstar/<project_type>/<project_id>/', project.project_unstar, name='project_unstar'),

    path('manage/<project_id>/', include([
        path('dashboard/', manage.dashboard, name='project.dashboard'),
        path('issues/', manage.issues, name='project.issues'),
        path('statistics/', manage.statistics, name='project.statistics'),
        path('file/', manage.file, name='project.file'),
        path('wiki/', manage.wiki, name='project.wiki'),
        path('setting/', manage.setting, name='project.setting'),
    ]))
]
