"""
用户账户相关功能
"""
from django.shortcuts import render
from web.forms.account import RegisterModelForm


def register(request):
    form = RegisterModelForm()
    return render(request, 'register.html', {'form': form})
