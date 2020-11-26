
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：drf_mis_20201119 -> urls
@IDE    ：PyCharm
@Author ：zhangzhen
@Date   ：2020/11/24 16:21
@Desc   ：
=================================================='''
from django.urls import re_path
from rbac.views import organization



urlpatterns = [
    # url(r'^login/$', obtain_jwt_token),
    # url(r'^verify/$', verify_jwt_token),
    # url(r'^refresh/$', refresh_jwt_token),

    re_path('(?P<version>[v1|v2]+)/organization/', organization.OrganizationView.as_view()),



    ]