# -*- coding: utf-8 -*-
# @Time    : 2018/11/30 19:33
# @Author  : yannis
# @Email   : tfbabi@163.com
# @File    : urls.py
# @Software: PyCharm

from django.conf.urls import url
import views
urlpatterns = [
    url(r'^$', views.login),
    url(r'^index/$', views.index),
    url(r'^index1/$', views.index1),
    url(r'^uploadPic/$', views.uploadPic),
    url(r'^uploadHandle/$', views.uploadHandle),
    url(r'^register/$', views.register),
    url(r'^zhuceHandle/$', views.zhuceHandle),
    url(r'^zhuceHandle1/$', views.zhuceHandle1),
    #auth模块验证
    url(r'^loginHandle/$', views.loginHandleAuth),
    #数据库自定义用户表查询验证
    #url(r'^loginHandle/$', views.loginHandle),
    #只展示无分页功能用book
    #url(r'^book(?P<booknum>\d+)/$', views.book),
    #既展示章节又自动分页 listpage
    url(r'^book(?P<booknum>\d+)/$', views.listpage),
    url(r'^book\d+/(?P<pagenum>\d+)/$', views.page),
    url(r'^logout/$', views.logout),
    #pagedemo
    url(r'^pagedemo/$', views.pagedemo),
    url(r'setpwdHandle/$',views.setpwdHandle),
    url(r'setpwd/$',views.setpwd),
]