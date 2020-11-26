# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：drf_mis_20201119 -> organization
@IDE    ：PyCharm
@Author ：zhangzhen
@Date   ：2020/11/25 17:08
@Desc   ：
=================================================='''
from rest_framework.views import APIView
from ..rbac_serializers.organization_serializer import  OrganizationSerializer

from django.shortcuts import HttpResponse

class OrganizationView(APIView):
    '''
    组织结构创建
    '''

    def post(self,request,*args,**kwargs):

        print(request.data)
        ser = OrganizationSerializer(data=request.data)  # 验证，对请求发来的数据进行验证
        if ser.is_valid():
            print(111)  # post请求数据字典
            ser.save()
        else:
            print(222, ser.errors)  # form验证错误信息
        return HttpResponse("userCont")
