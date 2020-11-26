# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：drf_mis_20201119 -> urls
@IDE    ：PyCharm
@Author ：zhangzhen
@Date   ：2020/11/19 19:12
@Desc   ：
=================================================='''
from django.urls import re_path
from user import views
from django.conf.urls import url
from rest_framework_jwt.views import ObtainJSONWebToken, obtain_jwt_token, verify_jwt_token, refresh_jwt_token

urlpatterns = [
    # url(r'^login/$', obtain_jwt_token),
    # url(r'^verify/$', verify_jwt_token),
    # url(r'^refresh/$', refresh_jwt_token),

    re_path('(?P<version>[v1|v2]+)/register/', views.User_Register_View.as_view()),
    re_path('(?P<version>[v1|v2]+)/login/', views.User_Login_View.as_view()),
    re_path('(?P<version>[v1|v2]+)/login1/', views.LoginAPIView.as_view()),


    ]

