from django.db import models

# Create your models here.

class UserInfo(models.Model):

    username=models.CharField(max_length=20)
    userpasswd=models.CharField(max_length=20)
    usergender=models.CharField(max_length=20)
    userhobby=models.CharField(max_length=20)
    usersay=models.CharField(max_length=20)
    userpos=models.CharField(max_length=20)
    class META():
        db_table='userinfo'
class NovelInfo(models.Model):
    novelid=models.AutoField(max_length=20,primary_key=True)
    sort=models.CharField(max_length=255)
    novelname=models.CharField(max_length=255)
    author=models.CharField(max_length=255,default='')
    novel_type=models.CharField(max_length=255,default='')
    bookstrnum=models.CharField(max_length=255,default='')
    mark=models.CharField(max_length=255,default='')
    lastdate=models.CharField(max_length=255,default='')
    totalclick=models.CharField(max_length=255,default='')
    monthclick=models.CharField(max_length=255,default='')
    weekclick=models.CharField(max_length=255,default='')
    totolup=models.CharField(max_length=255,default='')
    monthup=models.CharField(max_length=255,default='')
    weekup=models.CharField(max_length=255,default='')

class ChapterInfo(models.Model):
    chapterid=models.AutoField(max_length=20,primary_key=True)
    chaptername=models.CharField(max_length=255)
    content=models.TextField()
    bookid=models.ForeignKey(NovelInfo)


