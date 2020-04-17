"""
用户账户相关功能
"""
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from web.forms.account import RegisterModelForm, SendSmsForm, LoginSMSForm


def register(request):
    """注册"""
    if request.method == "GET":
        form = RegisterModelForm()
        return render(request, 'register.html', {'form': form})
    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        # 验证通过 写入数据库
        form.save()
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
    form = LoginSMSForm()
    if form.is_valid(data=request.POST):
        # 用户输入正确，登录成功（这样的话少做一个查询）
        user_object = form.cleaned_data['mobile_phone']
        # 用户信息写入session
        print(user_object)
        return JsonResponse({'status': True, 'data': '/index/'})
    return JsonResponse({'status': False, 'error': form.errors})
