import random

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from utils.tencent.sms import send_sms_single


def send_sms(request):
    """ 发送短信
    ?tpl=login  -> 577946
    ?tpl=register -> 577945
    """
    tpl = request.GET.get('tpl')
    template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
    print(tpl, template_id)
    if not template_id:
        return HttpResponse('模板不存在')

    code = random.randrange(1000, 9999)
    res = send_sms_single('110', template_id, [code, ])
    if res['result'] == 0:
        return HttpResponse('成功')
    else:
        return HttpResponse(res['errmsg'])
