from django.db import models

# Create your models here.
class UserInfo(models.Model):
    """定义用户数据库"""
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=32)
    uemail = models.CharField(max_length=30,null=True,blank=True)


    class Meta:
        db_table="UserInfo"
        verbose_name="用户信息"

    def __str__(self):
        return self.username



class UserToken(models.Model):
    user = models.OneToOneField(to="UserInfo", on_delete=models.CASCADE)
    token = models.CharField(max_length=64)

    class Meta:
        db_table="UserToken"
        verbose_name = "登录后生成的token"







