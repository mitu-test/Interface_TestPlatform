Interface_TestPlatform
-------
项目简介：
-------
Interface_TestPlatform是基于Python3.6+Django2.0+requests+ddt+unitest+HTMLTestRunner等开发的接口测试平台,支持用户登录、注册、密码找回；支持项目管理、模块管理、用例管理、任务管理等页面的增删改查功能，支持单个测试用例和批量测试用例的执行，并自动生成Html测试报告。

使用方法：
-------
1.安装Python3.6环境
-------
2.下载代码到本地并解压
-------
3.cmd到根目录下安装相关依赖包
-------
```
pip install -r requirements.txt
```
4.安装mysql数据库，进入mysite/settings.py配置数据库连接
-------

```DATABASES = {
‘default’: {
    # 'ENGINE': 'django.db.backends.sqlite3',
    # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    'ENGINE':'django.db.backends.mysql',     # 数据库类型，mysql
    'NAME':'interface_testplatform',            #  database名
    'USER':'root',               # 登录用户
    'PASSWORD':'123456',        #  登录用户名
    'HOST':'127.0.0.1',        # 数据库地址
    'PORT':'3306'              # 数据库端口
}
}
```
5.cmd到根目录下，生成数据库迁移记录
-------
```
python manage.py makemigrations
```
6.完成数据库迁移
-------
```
python manage.py migrate 
```
7.创建超级用户，用于后台管理
-------
```
python manage.py createsuperuser
```
8.运行启动django服务
-------
```
python manage.py runserver 127.0.0.1:8001
```
9.访问127.0.0.1:8001进入接口测试平台主页面
-------
项目管理：（支持项目的增删改查）

![](https://github.com/PyGuojun/Interface_TestPlatform/blob/master/image/project.png)

模块管理：（支持模块的增删改查）

![](https://github.com/PyGuojun/Interface_TestPlatform/blob/master/image/moudle.png)

用例管理：（支持用例的增删改查，以及单个用例执行，生成HTML报告）

![](https://github.com/PyGuojun/Interface_TestPlatform/blob/master/image/case.png)

用例新增1：

![](https://github.com/PyGuojun/Interface_TestPlatform/blob/master/image/case_add1.png)

用例新增2：

![](https://github.com/PyGuojun/Interface_TestPlatform/blob/master/image/case_add2.png)

单个用例运行，生成HTML报告：

![](https://github.com/PyGuojun/Interface_TestPlatform/blob/master/image/case_run.png)


任务管理：（支持任务的增删改查，以及任务执行，生成HTML报告）

![](https://github.com/PyGuojun/Interface_TestPlatform/blob/master/image/task.png)

任务新增：（PS:一个任务包含多个测试用例）

![](https://github.com/PyGuojun/Interface_TestPlatform/blob/master/image/task_add.png)

任务运行，生成HTML报告：

![](https://github.com/PyGuojun/Interface_TestPlatform/blob/master/image/task_run.png)
