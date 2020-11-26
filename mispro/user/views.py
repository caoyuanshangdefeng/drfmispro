from django.shortcuts import render,HttpResponse
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.http import JsonResponse
from .models import UserInfo

# Create your views here.
class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model=UserInfo
        fields="__all__"
    def validate(self, attrs):
        '''
        validate 方法只有一个参数 data， 是所有字段的值
        由于 data 包含了所有字段的值，所以可以同时做多个条件判断，这里只做了一个
        '''
        print(1111)

        username = attrs['username']
        password = attrs['password']
        if bool(re.search(r'\d', username )):
            raise ValidationError('账户中不能出现数字')
        return attrs

class User_Register_View(APIView):

    '''
    user register
    '''
    def post(self,requset,*args, **kwargs):
        print(requset.data)
        print('版本',requset.version)
        ser = UserSerializers(data=requset.data)  # 验证，对请求发来的数据进行验证
        if ser.is_valid():
            print(111)  # post请求数据字典
            ser.save()
        else:
            print(222,ser.errors)  # form验证错误信息
        return HttpResponse("userCont")

def md5(user):
    import hashlib
    import time
    ctime = str(time.time())

    m = hashlib.md5(bytes(user,encoding='utf-8'))
    m.update(bytes(ctime,encoding='utf-8'))

    return m.hexdigest()



class User_Login_View(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        ret = {'code': 1000,
               'msg': None}
        username = request.data["username"]
        password = request.data["password"]
        print("username", username, "password", password)

        obj = models.UserInfo.objects.filter(username=username, password=password).first()

        print('odj',obj)


        if not obj:
            ret['code']=1001
            ret['msg']='用户名或者密码登陆错误'
        #为登陆用户创建一个token,通过MD5+时间戳+用户名
        token = md5(username)
        # UserToken要么创建要么更新,存在就更新不存在就创建
        models.UserToken.objects.update_or_create(user=obj,defaults={'token':token})
        ret['token'] = token

        return JsonResponse(ret)







# serializers.py
from rest_framework.serializers import ModelSerializer, CharField, ValidationError, SerializerMethodField
from . import models
import re
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
class LoginSerializer(ModelSerializer):
    # 定义用户名和密码两个仅支持反序列化的字段
    username = CharField(write_only=True)
    password = CharField(write_only=True)
    class Meta:
        model = models.UserInfo
        fields = ('username', 'password')

    # 在全局钩子中签发token
    def validate(self, attrs):
        user = self._many_method_login(**attrs)
        # 将数据存放到序列化对象中
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        self.user = user
        self.token = token

        return attrs

        # 多方式登录
    def _many_method_login(self, **attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        # 正则匹配,如果有@符号,则判定为邮箱登录
        if re.match(r'.*@.*', username):
            user = models.UserInfo.objects.filter(email=username).first()

            # 如果是11位数字且开头为1,判定为手机登录
        elif re.match(r'^1[0-9]{10}$', username):
            user = models.User.objects.filter(mobile=username).first()

        # 两个都不匹配的话,就判定为用户名登录
        else:
            user = models.UserInfo.objects.filter(username=username).first()

        # 如果用户不存在,就是信息有误
        if not user:
            raise ValidationError({'username': '账号有误'})

        # 如果用户存在,但是检测密码有问题,报错密码有误
        # if not user.check_password(password):
        #     raise ValidationError({'password': '密码有误'})

        return user


class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    # 以post的方式接受前台发送的数据
    def post(self, request, *args, **kwargs):
        # 将前台传来的数据传送到序列化对象中,完成校验
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        res={'msg':'login success',
             'username': serializer.user.username,
             'token': serializer.token}
        return JsonResponse(res)






























































































'''
django.db.utils.OperationalError: (1050, "Table '表名' already exists）解决方法
python manage.py migrate myapp --fake  


DJANGO DRF认证组件TOKEN判断用户登录状态

https://www.cnblogs.com/apollo1616/articles/10098096.html

DRF的json web token方式完成用户认证
https://www.pianshen.com/article/4467530603/


'''