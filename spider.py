# -*- coding: utf-8 -*-
# @Time    : 2018/11/1 11:19
# @Author  : yannis
# @Email   : tfbabi@163.com
# @File    : spider.py
# @Software: PyChar

###########
#编码。显示console的编码为utf-8
#乱码的产生只有一种可能性，实际的编码与显示的编码不一致，一般情况下会用utf-8称为我们显示的编码


##########
from common_mode.db_demo.PyMysql import dbUtil
from common_mode.log_demo import Advanced_Usage
import requests
import re
from bs4 import BeautifulSoup
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from multiprocessing import Process,Pool,Queue
from threading import Thread

head={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36','Referer':'http://www.23us.so/'}
logger=Advanced_Usage.Logging().My_Logger('download.txt')

#db cursor
cursor=dbUtil.dbUtil('127.0.0.1','root','ski.root','dbook_demo')
#cursor=dbUtil.dbUtil('127.0.0.1','root','ski.root','test5')
#cursor.insert('test5',{})

def getSortList(booktype=1,page=1):
    res=requests.get('https://www.23us.so/list/%s_%s.html' %(booktype,page),headers=head)
    html=res.content        #返回的数据编码为utf-8
    #html=html.decode('gbk')    #解码decode  把一种编码转换成unicode编码
    #html=html.encode('utf-8')  #编码encode  把unicode转换成另一种编码
    #reg1=r'<td class="L"><a href="(.*?[title])">(.*?)</a></td>'
    reg1=r'<td class="L"><a href="(.*?[title])">(.*?)</a></td>.*?<td class="C">(.*?)</td>.*?class="R">(.*?)</td>'
    reg2=r'<em id="pagestats">1\/(\d+)</em>'
    reg3=r'<td class="L"><a href="(.*?[title])">(.*?)</a></td>.*?<td class="C">(.*?)</td>'
    return re.findall(reg1,html,re.S)
    #return re.findall(reg2,html)[0]
def get_max_page(booktype=1):
    html = requests.get('https://www.23us.so/list/%s_1.html' %(booktype,),headers=head).content
    reg=r'<em id="pagestats">1\/(\d+)</em>'
    return re.findall(reg,html)[0]
def getNovelContent(url):
    html = requests.get(url,headers=head).content
    reg=r'<dd><div class="fl"><a.*?href="(.*?)"><img.*?<td>.*?>(.*?)</a></td>'
    reg=re.compile(reg,re.S)
    url=re.findall(reg,html)[0]
    return url
def getNovelInfo1(url):
    html = requests.get(url,headers=head).content
    tree=etree.HTML(html)
    mark=tree.xpath('//table[1]/tr[2]/td[1]/text()')[0].encode('utf-8')
    lastdate=tree.xpath('//table[1]/tr[2]/td[3]/text()')[0].encode('utf-8')
    totalclick=tree.xpath('//table[1]/tr[3]/td[1]/text()')[0].encode('utf-8')
    monthclick=tree.xpath('//table[1]/tr[3]/td[2]/text()')[0].encode('utf-8')
    weekclick=tree.xpath('//table[1]/tr[3]/td[3]/text()')[0].encode('utf-8')
    totolup=tree.xpath('//table[1]/tr[4]/td[1]/text()')[0].encode('utf-8')
    monthup=tree.xpath('//table[1]/tr[4]/td[2]/text()')[0].encode('utf-8')
    weekup=tree.xpath('//table[1]/tr[4]/td[3]/text()')[0].encode('utf-8')
    h=dict(mark=mark,lastdate=lastdate,totalclick=totalclick,monthclick=monthclick,weekclick=weekclick,totolup=totolup,monthup=monthup,weekup=weekup)
    return h
def getNovelList(url):
    html = requests.get(url,headers=head).content
    reg=r'<td class="L"><a href="(.*?)">(.*?)</a></td>'
    chapterlist=re.findall(reg,html)
    return chapterlist
def getChapterContent(url):
    html = requests.get(url,headers=head).content
    #html = requests.get(url,headers=head).content
    #reg=r'<dd id="contents">([\s\S]*?)</dd>'
    #reg=r'style5();</script>([\s\S]*?)<script type="text/javascript">'#简单的re处理换行
    #reg=re.compile(reg,re.S)   #python的简单方法:编译【编译成re支持的对象】正则表达式 re.S表示正则表达式可以匹配多行
    soup=BeautifulSoup(html,'lxml')
    content = soup.find_all('dd',id='contents')
    return content[0].get_text()
    #return re.findall(reg,html)[0]
def write_to_txt(content,path):
    with open(path,'a+') as f:
        f.write(content)



def BookPageHandel(page):
    logger.info("+++"*40+"第%d个栏目,第%s页开始打印..." %(sort,page))
    for bookhref,bookname,bookauthor,bookstrnum in getSortList(sort,page):
        logger.info(">>>"*40+"书籍名称:%s || 书籍开始地址:%s" %(bookname,bookhref))
        mark=getNovelInfo1(bookhref)['mark']
        lastdate=getNovelInfo1(bookhref)['lastdate']
        totalclick=getNovelInfo1(bookhref)['totalclick']
        monthclick=getNovelInfo1(bookhref)['monthclick']
        weekclick=getNovelInfo1(bookhref)['weekclick']
        totolup=getNovelInfo1(bookhref)['totolup']
        monthup=getNovelInfo1(bookhref)['monthup']
        weekup=getNovelInfo1(bookhref)['weekup']
        novelUrl = getNovelContent(bookhref)[0]
        novelType = getNovelContent(bookhref)[1]

        cursor.insert('booktest_novelinfo',{'sort':page,'novelname':bookname,'author':bookauthor,'novel_type':novelType,'bookstrnum':bookstrnum,'mark':mark,'lastdate':lastdate,'totalclick':totalclick,'monthclick':monthclick,'weekclick':weekclick,'totolup':totolup,'monthup':monthup,'weekup':weekup})
        cursor.commit()
        global lastrowid
        lastrowid=cursor.getLastInsertId()
        logger.info("<<<"*40+"书籍章节地址:%s" %novelUrl)
        return novelUrl
        #ubname=bookname.decode('utf-8')

        #f=open("book/"+ubname+".txt",'a+')
def BookHandle(novelUrl):
    for ChapterUrl,Chaptername in getNovelList(novelUrl):
        #ubname=bookname.decode('utf-8')

        logger.info("###"*40+"开始下载章节名称:%s || 章节地址%s" %(Chaptername,ChapterUrl))
        #f.write("###"*40+"章节名称:%s 章节地址%s" %(Chaptername,ChapterUrl)+"\r\n")
        ChapterContet=getChapterContent(ChapterUrl)

        cursor.insert('booktest_chapterinfo',{'chaptername':Chaptername,'content':ChapterContet,'bookid_id':lastrowid,})
        cursor.commit()
        #f.write(ChapterContet.encode('utf-8')+'\r\n')
        #f.close()


if __name__ == "__main__":
    for sort in range(1,10):
        max_num=get_max_page(sort)
        for page in range(1,int(max_num)):
            novelUrl = BookPageHandel(page)
            BookHandle(novelUrl)



