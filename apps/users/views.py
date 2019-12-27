from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from users.models import UserProfile
from users.forms import UserForm, RegisterForm, ResetPwdForm
from django.contrib.auth.hashers import make_password


# Create your views here.

@login_required(login_url='/users/login')
def index(request):
    """
    平台主页
    """
    return redirect('projects/list/')


def user_login(request):
    """
    用户登录
    """
    if request.user.is_authenticated:#如果已登录就直接跳到主页
        return HttpResponseRedirect(reverse("index"))

    if request.is_ajax():  # 请求ajax则返回新的image_url和key
        result = dict()
        result['key'] = CaptchaStore.generate_key()
        result['image_url'] = captcha_image_url(result['key'])
        return JsonResponse(result)
    if request.method == "POST":
        login_form = UserForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "users/login.html", {"login_form": login_form, "msg": "登录失败, 请检查用户名或者密码! "})
        else:
            return render(request, "users/login.html", {"login_form": login_form})
    else:
        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)
        login_form = UserForm()
        return render(request, "users/login.html",
                      {"login_form": login_form, "hashkey": hashkey, "image_url": image_url, })


def register(request):
    """
    用户注册
    """
    if request.is_ajax():  # 请求ajax则返回新的image_url和key
        result = dict()
        result['key'] = CaptchaStore.generate_key()
        result['image_url'] = captcha_image_url(result['key'])
        return JsonResponse(result)
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            if password1 != password2:
                msg = "两次输入的密码不同！"
                return render(request, "users/register.html", {'register_form': register_form, 'msg': msg})
            else:
                same_user = UserProfile.objects.filter(username=username)
                if same_user:  # 用户名唯一
                    msg = '用户名已经存在，请重新选择用户名！'
                    return render(request, "users/register.html", {'register_form': register_form, 'msg': msg})
                new_user = UserProfile()
                new_user.username = username
                new_user.password = make_password(password1)  # 使用加密密
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面
        else:
            return render(request, "users/register.html", {'register_form': register_form})

    else:
        register_form = RegisterForm()
        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)
        return render(request, "users/register.html",
                      {'register_form': register_form, "hashkey": hashkey, "image_url": image_url, })


@login_required(login_url='/users/login')
def user_logout(request):
    """
    用户退出
    """
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def reset_password(request):
    """
    密码重置
    """
    if request.is_ajax():  # 请求ajax则返回新的image_url和key
        result = dict()
        result['key'] = CaptchaStore.generate_key()
        result['image_url'] = captcha_image_url(result['key'])
        return JsonResponse(result)
    if request.method == "POST":
        reset_pwd_form = ResetPwdForm(request.POST)
        if reset_pwd_form.is_valid():
            username = reset_pwd_form.cleaned_data['username']
            password1 = reset_pwd_form.cleaned_data['password1']
            password2 = reset_pwd_form.cleaned_data['password2']
            if password1 != password2:
                msg = "两次输入的密码不同！"
                return render(request, "users/reset_password.html", {'reset_pwd_form': reset_pwd_form, 'msg': msg})
            else:
                user = UserProfile.objects.get(username=username)
                user.password = make_password(password1)
                user.save()
                logout(request)
                return redirect('/login/')  # 自动跳转到登录页面
    else:
        reset_pwd_form = ResetPwdForm()
        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)
        return render(request, "users/reset_password.html",
                      {'reset_pwd_form': reset_pwd_form, "hashkey": hashkey, "image_url": image_url, })


@login_required(login_url='/users/login')
def reset_password1(request):
    """
    登录后密码重置
    """
    if request.is_ajax():  # 请求ajax则返回新的image_url和key
        result = dict()
        result['key'] = CaptchaStore.generate_key()
        result['image_url'] = captcha_image_url(result['key'])
        return JsonResponse(result)
    if request.method == "POST":
        reset_pwd_form = ResetPwdForm(request.POST)
        if reset_pwd_form.is_valid():
            username = reset_pwd_form.cleaned_data['username']
            password1 = reset_pwd_form.cleaned_data['password1']
            password2 = reset_pwd_form.cleaned_data['password2']
            if password1 != password2:
                msg = "两次输入的密码不同！"
                return render(request, "users/reset_password.html", {'reset_pwd_form': reset_pwd_form, 'msg': msg})
            else:
                user = UserProfile.objects.get(username=username)
                user.password = make_password(password1)
                user.save()
                return redirect('/login/')  # 自动跳转到登录页面
    else:
        reset_pwd_form = ResetPwdForm()
        hashkey = CaptchaStore.generate_key()
        image_url = captcha_image_url(hashkey)
        return render(request, "base.html",
                      {'reset_pwd_form': reset_pwd_form, "hashkey": hashkey, "image_url": image_url, })
