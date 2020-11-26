# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：drf_mis_20201119 -> organization_serializer
@IDE    ：PyCharm
@Author ：zhangzhen
@Date   ：2020/11/25 16:13
@Desc   ：
=================================================='''

from rest_framework import serializers
from ..models import Organization
from rest_framework.exceptions import ValidationError

class OrganizationSerializer(serializers.ModelSerializer):
    '''
    组织架构序列化

    '''
    type=serializers.ChoiceField(choices=Organization.organization_type_choices,default="company")

    class Meta:
        model=Organization
        fields='__all__'

    def validate(self, attrs):
        '''
        validate 方法只有一个参数 data， 是所有字段的值
        由于 data 包含了所有字段的值，所以可以同时做多个条件判断，这里只做了一个
        '''
        print(1111)
        print('attrs',attrs)

        # username = attrs['username']
        # password = attrs['password']
        # if bool(re.search(r'\d', username )):
        #     raise ValidationError('账户中不能出现数字')
        return attrs


