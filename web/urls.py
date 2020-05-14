from django.urls import path, include
from web.views import account
from web.views import home
from web.views import project
from web.views import manage
from web.views import wiki

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
        path('wiki/', wiki.wiki, name='wiki'),
        path('wiki/add/', wiki.wiki_add, name="wiki_add"),
        path('wiki/catalog/', wiki.wiki_catalog, name="wiki_catalog"),
        path('wiki/delete/<wiki_id>/', wiki.wiki_delete, name="wiki_delete"),
        path('wiki/edit/<wiki_id>/', wiki.wiki_edit, name="wiki_edit"),

        path('dashboard/', manage.dashboard, name='project.dashboard'),
        path('issues/', manage.issues, name='project.issues'),
        path('statistics/', manage.statistics, name='project.statistics'),
        path('file/', manage.file, name='project.file'),
        path('setting/', manage.setting, name='project.setting'),
    ]))
]
