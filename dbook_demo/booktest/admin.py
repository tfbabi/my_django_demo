#encoding:utf-8
from django.contrib import admin
from models import *
# Register your models here.

class ChapterInfoline(admin.TabularInline):
    model = ChapterInfo
    extra = 3
class UserInfoAdmin(admin.ModelAdmin):
    #展示详情
    list_display = ['id','username','userpasswd','usergender','userhobby','userhobby','userpos']
    #过滤器
    list_filter=['username',]
    #搜索框
    search_fields = ['username']
    #分页
    list_per_page = 20
class NovelInfoAdmin(admin.ModelAdmin):
    list_display = ['novelid','sort','novelname','author','novel_type','bookstrnum','totalclick','lastdate','totolup','mark','monthclick','monthup','weekclick','weekup']
    list_per_page = 20
    inlines = [ChapterInfoline]

class ChapterInfoAdmin(admin.ModelAdmin):
    list_display =['chapterid','chaptername','bookid_id']
    list_per_page = 20



admin.site.register(UserInfo,UserInfoAdmin)
admin.site.register(NovelInfo,NovelInfoAdmin)
admin.site.register(ChapterInfo,ChapterInfoAdmin)