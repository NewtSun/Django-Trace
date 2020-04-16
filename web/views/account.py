"""
用户账户相关功能
"""
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from web.forms.account import RegisterModelForm, SendSmsForm


def register(request):
    form = RegisterModelForm()
    return render(request, 'register.html', {'form': form})


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
