#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json

from rest_framework.views import APIView
from django_redis import get_redis_connection
from rest_framework.response import Response

from api.models import *
from api.utils.response import BaseResponse
from api.utils.convert import regular

class ShoppingCarView(APIView):
    """购物车API"""
    conn = get_redis_connection('default')
    def get(self, request, *args, **kwargs):
        """获取用户个人的购物车信息"""
        ret = BaseResponse()
        total = 0
        lis = []
        for item in self.conn.keys('shopping_car_%s_*'%request.user.id):
            total += 1
            redis_value = self.conn.hgetall(item)
            lis.append(regular(redis_value))
        ret.data = {'total':total, 'myShopCart':lis}
        return Response(ret.__dict__)

    def post(self, request, *args, **kwargs):
        """创建一条购物车信息"""
        ret = BaseResponse()
        courseId = request.data.get('courseId')
        course_obj = Course.objects.get(pk=courseId)
        policy_id = int(request.data.get('policy_id'))
        redis_key = 'shopping_car_%s_%s'%(request.user.id, courseId)
        policy = {}
        default_policy = None
        for item in course_obj.price_policy.all():
            print(item.id)
            if policy_id == item.id:
                default_policy = policy_id
            policy[item.id] = {'name':item.get_valid_period_display(),'price':item.price}

        if not default_policy:
            ret.code = 1001
            ret.error = '创建失败，该课程没有相应的价格策略'
            return Response(ret.__dict__)

        redis_value = {'title':course_obj.name,
                       'image':course_obj.course_img,
                       'policy':json.dumps(policy),
                       'default_policy': default_policy}
        if self.conn.exists(redis_key):
            ret.data = '购物车中该套餐已更新成功'
        else:
            ret.data = '添加到购物车成功'
        self.conn.hmset(redis_key, redis_value)

        return Response(ret.__dict__)

    def put(self, request, *args, **kwargs):
        """更新购物车信息"""
        ret = BaseResponse()
        course_id = request.data.get('courseId')
        policy_id = request.data.get('policy_id')
        redis_key = 'shopping_car_%s_%s'%(request.user.id, course_id)
        redis_value = regular(self.conn.hgetall(redis_key))

        if policy_id not in redis_value['policy']:
            ret.error = 1003
            ret.error = '更新失败，没有该课程策略'
            return Response(ret.__dict__)
        redis_value[ 'default_policy'] = policy_id
        self.conn.hmset(redis_key, redis_value)
        ret.data = '更新成功'
        return Response(ret.__dict__)

    def delete(self, request, *args, **kwargs):
        """删除购物车信息"""
        ret = BaseResponse()
        keys = ['shopping_car_%s_%s'%(request.user.id, i) for i in request.data]
        self.conn.delete(*keys)
        ret.data = '删除成功'
        return Response(ret.__dict__)