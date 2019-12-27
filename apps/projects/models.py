from django.db import models


# Create your models here.
class Projects(models.Model):
    """
    项目表
    """
    name = models.CharField(max_length=50, verbose_name="项目名称",unique=True)
    describe = models.TextField(default="",null=True,blank=True,verbose_name="项目简介")
    status = models.BooleanField(default=1,verbose_name="项目状态")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="添加时间")

    class Meta:
        verbose_name = '项目管理'
        verbose_name_plural = '项目管理'

    def __str__(self):
        return self.name


class Modules(models.Model):
    """
    模块表

    """
    project = models.ForeignKey(Projects, on_delete=models.CASCADE,verbose_name="所属项目")
    name = models.CharField(max_length=50, null=False,verbose_name="模块名称",unique=True)
    describe = models.TextField(default="",null=True,blank=True,verbose_name="模块简介")
    tester = models.CharField(max_length=200,verbose_name="测试人员")
    developer = models.CharField(max_length=100, blank=True, verbose_name="开发人员")
    status = models.BooleanField(default=1, verbose_name="模块状态")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="添加时间")

    class Meta:
        verbose_name = '模块管理'
        verbose_name_plural = '模块管理'

    def __str__(self):
        return self.name
