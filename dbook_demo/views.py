#encoding:utf-8
from django.shortcuts import render,redirect
import os
# Create your views here.
from django.conf import settings
from django.http import HttpResponse,HttpResponseRedirect
from models import *
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

#注册页面 数据提交数据库
def register(request):
    #return render(request,'booktest/register.html')
    return render(request,'booktest/register.html')
#注册页面处理器
def zhuceHandle(request):
    uname=request.POST['username']
    upwd=request.POST['passwd']
    ugender=request.POST.get('gender')
    uhobby=request.POST.getlist('hobby')
    usay=request.POST['info']
    upos=request.POST['pos']
    if request.method == 'POST':
        user=UserInfo.objects.create(username=uname,userpasswd=upwd,usergender=ugender,userhobby=','.join(uhobby),usersay=usay,userpos=upos)
        user.save()
        #UserInfo.objects.get_or_create(username=uname,userpasswd=upwd,usergender=ugender,userhobby=','.join(uhobby),usersay=usay,userpos=upos)
        return HttpResponseRedirect("/")

    return HttpResponse("入库失败了 为啥 啊  啊")
#auth注册页
def zhuceHandle1(request):
    uname=request.POST['username']
    upwd=request.POST['passwd']
    User.objects.create_user(username=uname,password=upwd)
    return redirect("/")
#登录页
def login(request):
    return render(request,'booktest/login.html')

#登录处理器
def loginHandle(request):
    if request.method == 'POST':
        uname=request.POST['user']
        upwd=request.POST['password']
        if uname and upwd:
            uname = uname.strip()
            try:
                user=UserInfo.objects.get(username=uname)
            except:
                return HttpResponse("用户名不存在!")
                #return HttpResponseRedirect("/")
            if user.userpasswd == upwd:
                return HttpResponseRedirect('/index/')
            else:
                return HttpResponse("密码错")
        return HttpResponseRedirect("/")

#用django自带的auth模块重写登录处理器
def loginHandleAuth(request):
    if request.method == 'POST':
        uname=request.POST['user']
        upwd=request.POST['password']
        # 以下是使用auth模块，去数据库里查询用户信息，验证是否存在
        try:
            user=auth.authenticate(username=uname,password=upwd)
            auth.login(request,user)
        except:
        # 以下语句，其实还是将以上获得认证的用户ID保存在SESSION中，#用于后面每个页面根据此SESSION里的ID，获取用户信息验证，并给auth中间件使用
            return redirect('/')
        return redirect('/index/')
        # 用于以后在调用每个视图函数前，auth中间件会根据每次访问视图前请求所带的SEESION里面的ID，去数据库找用户对像，并将对象保存在request.user属性中
        # 中间件执行完后，再执行视图函数
    return render(request,'booktest/login.html')
#用户注销
def logout(request):
    auth.logout(request)
    return redirect('/')
#密码修改
@login_required
def setpwd(request):
    return render(request,'booktest/resetpwd.html')
@login_required
def setpwdHandle(request):
    uname=request.user
    upwd=request.POST['passwd']
    user = User.objects.get(username=uname)
    user.set_password(upwd)
    user.save()
    return redirect('/')
#登录后首页小说列表展示
@login_required
def index(request):
    uname=request.user
    chapter=NovelInfo.objects.all()
    paginator = Paginator(chapter,30)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    context={'chapter':chapter,'contacts':contacts,'uname':uname}
    return  render(request,'booktest/index.html',context)

@login_required
def index1(request):
    uname=request.user
    chapter=NovelInfo.objects.all()
    paginator = Paginator(chapter,30)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    context={'chapter':chapter,'contacts':contacts,'uname':uname}
    return  render(request,'booktest/bstrap_index.html',context)
#图片上传页
def uploadPic(request):
    return render(request,'booktest/uploadPic.html')
#图片上传处理器
def uploadHandle(request):
    fileObject=request.FILES['pic1']
    picName=os.path.join(settings.MEDIA_ROOT,fileObject.name)
    with open(picName,'wb') as pic:
        for liu in fileObject.chunks():
            pic.write(liu)
    return HttpResponse(picName)




#只展示章节标题无分页功能用book
@login_required
def book(request,booknum):
    book=NovelInfo.objects.get(novelid=booknum)
    chapter=ChapterInfo.objects.filter(bookid_id=booknum)
    context={'chapter':chapter,'book':book}
    return  render(request,'booktest/book.html',context)
@login_required
#展示小说章节标题并分页用listpage
def listpage(request,booknum):
    chapter=ChapterInfo.objects.filter(bookid_id=booknum)
    bookname=NovelInfo.objects.get(novelid=booknum)
    paginator = Paginator(chapter,40)
    page = request.GET.get('page')

    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    context={'chapter':chapter,'book':bookname,'contacts':contacts}
    return  render(request,'booktest/book.html',context)

#章节内容页展示
@login_required
def page(request,pagenum):
    chapter=ChapterInfo.objects.get(chapterid=pagenum)
    context={'chapter':chapter}
    return  render(request,'booktest/chapter.html',context)


def pagedemo(request):
    list=ChapterInfo.objects.all()
    #得到一个pageintor对象
    paginator = Paginator(list, 15)
    #得到一个page对象 第一页的
    page=paginator.page(1)
    context={'page':page}
    return  render(request,'booktest/pagedemo.html',context)

