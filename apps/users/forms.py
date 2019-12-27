from django import forms
from captcha.fields import CaptchaField


class UserForm(forms.Form):
    """登录表单"""
    username = forms.CharField(required=True,label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(required=True,label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码',error_messages={"invalid": "验证码错误"},)


class RegisterForm(forms.Form):
    """注册表单"""

    username = forms.CharField(label="用户名", max_length=128, widget=forms.TimeInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码',error_messages={"invalid": "验证码错误"},)


class ResetPwdForm(forms.Form):
    """
    重置密码表单
    """
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TimeInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="新密码", max_length=256,widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认新密码",max_length=256,widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码', error_messages={"invalid": "验证码错误"},)