"""
接受粉丝发送的信息，并回复‘测试’，参考微信mp平台文档从web.py框架修改为django框架
"""
# -*- coding: utf-8 -*-
# filename: main.py


from .handle import Handle
from django.conf import settings


from django.conf.urls import url
from django.http import HttpResponse

def index(request):
    MyHandle = Handle()
    return HttpResponse(MyHandle.POST(request))



if __name__== '__main__':
	from django.core.management import execute_from_command_line
	execute_from_command_line(sys.argv)
