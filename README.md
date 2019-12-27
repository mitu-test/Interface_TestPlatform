Interface_TestPlatform
-------
项目简介：
-------
Mxonline是基于python3.6+Django 1.11.6+Xadmin开发的在线教育平台,支持用户登录、注册、密码找回、收藏、评论，全局搜索以及个人中心的展示；机构列表的排序、分页、筛选以及机构详情页面的展示；讲师列表的人气排序、分页以及讲师详情页面的展示；课程列表的排序、分页、筛选，热门课程推荐，以及课程详情页面的展示等功能；

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
    'NAME':'mxonline',            #  database名
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
python manage.py runserver 127.0.0.1:8000
```
9.访问127.0.0.1:8000进入教育平台主页
-------
![](https://github.com/PyGuojun/Mxonline/blob/master/image/my_logo.png)
