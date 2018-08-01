#!/usr/bin/env python
# -*- coding:utf-8 -*-

from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import *
import uuid

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        ret = {'code': 1000, 'data': None, 'error': None}
        username = request.data.get('username')
        password = request.data.get('password')
        user_obj = Account.objects.filter(username=username, password=password).first()
        if user_obj:
            token = str(uuid.uuid4())
            ret['data'] = token
            # 每登陆成功一次就更新一下token值
            UserAuthToken.objects.update_or_create(user=user_obj, defaults={'token':token})
        else:
            ret['code'] = 1001
            ret['error'] = '用户名或密码错误'
        return Response(ret)