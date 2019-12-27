from django.db import models
from projects.models import Modules


# Create your models here.


class InterfaceCase(models.Model):
    """接口用例"""
    module = models.ForeignKey(Modules, on_delete=models.CASCADE, verbose_name="所属模块")
    name = models.CharField(max_length=50, null=False, verbose_name="用例名称")
    api = models.CharField(max_length=100, verbose_name="接口路径")

    method = models.CharField(null=False, verbose_name="请求方法",
                              choices=(("0", "GET"), ("1", "POST"), ("2", "DELETE"), ("3", "PUT")), default="0",
                              max_length=10)
    header = models.TextField(null=False, verbose_name="请求头")
    param_type = models.CharField(null=False, verbose_name="参数类型", choices=(("0", "form-data"), ("1", "json"),
                                                                            ("2", "params")), default="0",
                                  max_length=10)
    param_body = models.TextField(null=False, verbose_name="参数内容")

    assert_type = models.CharField(null=False, verbose_name="断言类型", choices=(("0", "包含"), ("1", "匹配")), default="0",
                                   max_length=10)
    assert_body = models.TextField(null=False, verbose_name="断言内容")
    describe = models.TextField(default="", null=True, blank=True, verbose_name="用例描述")
    status = models.BooleanField(default=1, verbose_name="状态")
    maker = models.CharField(max_length=200, null=True, blank=True, verbose_name="创建者")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name = '接口用例'
        verbose_name_plural = '接口用例'

    def __str__(self):
        return self.name


class TestTask(models.Model):
    """测试任务"""
    name = models.CharField(max_length=50, null=False, verbose_name="任务名称")
    describe = models.TextField(default="", null=True, blank=True, verbose_name="任务描述")
    status = models.CharField(max_length=50,verbose_name="状态", choices=(("0", "未执行"), ("1", "执行中"),("2", "执行完成")),default="0")
    cases = models.TextField(verbose_name="关联用例", default="")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name = '测试任务'
        verbose_name_plural = '测试任务'

    def __str__(self):
        return self.name


class TestResult(models.Model):
    """
    测试结果
    """
    task = models.ForeignKey(TestTask, on_delete=models.CASCADE, verbose_name="任务名称")
    name = models.CharField(verbose_name="名称", max_length=100, blank=False, default="")
    error = models.IntegerField(verbose_name="错误用例")
    failure = models.IntegerField(verbose_name="失败用例")
    skipped = models.IntegerField(verbose_name="跳过用例")
    tests = models.IntegerField(verbose_name="总用例数")
    run_time = models.FloatField(verbose_name="运行时长")
    result = models.TextField(verbose_name="详细", default="")
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        verbose_name = '测试任务'
        verbose_name_plural = '测试任务'

    def __str__(self):
        return self.name
