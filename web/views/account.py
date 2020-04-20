"""
用户账户相关功能
"""
import datetime
import uuid
from io import BytesIO

from django.db.models import Q
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect

from utils.image_code import check_code
from web import models
from web.forms.account import RegisterModelForm, SendSmsForm, LoginSMSForm, LoginForm


def register(request):
    """注册"""
    if request.method == "GET":
        form = RegisterModelForm()
        return render(request, 'register.html', {'form': form})
    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        # 验证通过 写入数据库
        # form.save()
        # 验证通过，写入数据库（密码要是密文）
        # instance = form.save，在数据库中新增一条数据，并将新增的这条数据赋值给instance

        # 用户表中新建一条数据（注册）
        instance = form.save()

        # 创建交易记录
        # 方式一
        policy_object = models.PricePolicy.objects.filter(category=1, title="个人免费版").first()
        models.Transaction.objects.create(
            status=2,
            order=str(uuid.uuid4()),
            user=instance,
            price_policy=policy_object,
            count=0,
            price=0,
            start_datetime=datetime.datetime.now()
        )
        return JsonResponse({'status': True, 'data': '/login/'})
    return JsonResponse({'status': False, 'error': form.errors})


def send_sms(request):
    """发送短信"""
    print(request.GET)
    mobile_phone = request.GET.get('mobile_phone')
    tpl = request.GET.get('tpl')
    form = SendSmsForm(request, data=request.GET)
    if form.is_valid():
        # 发短信
        # 写Redis
        return JsonResponse({'status': True})
    # ValidationError会把只要校验不通过的信息都放在form.error里面
    return JsonResponse({'status': False, 'error': form.errors})


def login_sms(request):
    """短信登录"""
    if request.method == 'GET':
        form = LoginSMSForm()
        return render(request, 'lgoin_sms.html', {'form': form})
    form = LoginSMSForm(data=request.POST)
    if form.is_valid():
        # 用户输入正确，登录成功（这样的话少做一个查询）
        user_object = form.cleaned_data['mobile_phone']
        # 用户信息写入session
        request.session['user_id'] = user_object.id
        request.session.set_expiry(60 * 60 * 24 * 14)
        print(user_object)
        return JsonResponse({'status': True, 'data': '/index/'})
    return JsonResponse({'status': False, 'error': form.errors})


def login(request):
    """ 用户名和密码登录 """
    if request.method == 'GET':
        form = LoginForm(request)
        return render(request, 'login.html', {'form': form})
    form = LoginForm(request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        # user_object = models.UserInfo.objects.filter(username=username, password=password).first()
        #  (手机=username and pwd=pwd) or (邮箱=username and pwd=pwd)

        user_object = models.UserInfo.objects.filter(Q(email=username) | Q(mobile_phone=username)).filter(
            password=password).first()
        if user_object:
            # 登录成功为止1
            request.session['user_id'] = user_object.id
            request.session.set_expiry(60 * 60 * 24 * 14)

            return redirect('index')

        form.add_error('username', '用户名或密码错误')

    return render(request, 'login.html', {'form': form})


def image_code(request):
    """ 生成图片验证码 """

    image_object, code = check_code()

    request.session['image_code'] = code
    request.session.set_expiry(60)  # 主动修改session的过期时间为60s

    stream = BytesIO()
    image_object.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def logout(request):
    request.session.flush()
    return redirect('index')
