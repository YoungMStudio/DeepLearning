#Python 3.6.3
#coding:UTF-8
#author:YoungMStudio
#date:2017-12-16
#Description:福利彩票双色球信息获取
#VisitUrl:http://kaijiang.zhcw.com/zhcw/html/ssq/list_1.html

import urllib.request
import urllib.error
from bs4 import BeautifulSoup	#采用BeautifulSoup 在CMD命令中使用pip install bs4安装
import os
import re

#伪装成浏览器登陆,获取网页源代码
def getPage(href): 
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }
    req = urllib.request.Request(
        url = href ,
        headers = headers
    )
    try:
        post = urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        print(e.code())
        print(e.reason())
    return post.read()

#初始化url双色球首页
url = 'http://kaijiang.zhcw.com/zhcw/html/ssq/list_1.html'  


#===============================================================================
#获取url总页数
def getPageNum(url):
    num =0
    page = getPage(url)
    soup = BeautifulSoup(page, "html.parser")	
    strong = soup.find('td',colspan='7')
    # print strong
    if strong:
        result = strong.get_text().split(' ')
        # print result
        list_num = re.findall("[0-9]{1}",result[1])
        # print list_num
        for i in range(len(list_num)):
            num = num*10 + int(list_num[i])
        return num
    else:
        return 0

#===============================================================================
#获取每页双色球的信息
def getText(url):

    #创建一个文件，用来写入彩票信息    
    fp = open("彩票信息.txt" ,"w")
    
    #从第一页到第getPageNum(url)页
    #for list_num in range(1,getPageNum(url)):	
    for list_num in range(1,2):
	
        #生成下一页链接    
        href = 'http://kaijiang.zhcw.com/zhcw/html/ssq/list_'+str(list_num)+'.html'
		#获取该页内容
        page = BeautifulSoup(getPage(href), "html.parser")       

        #匹配 <td align=center>这样的内容，返回一个div列表
        div_list = page.find_all('td',{'align':'center'})
        
        linetext = ''
        for div in div_list:
			#读者可以打印一下每个div
            #print('div:\n',div,type(div))
			#直接从div结构中读取标签内容
            text = div.get_text().strip('')
			#读者可以打印一下标签内容，应该为<div>XXX</div>中间的XXX，含div子标签
            #print( 'text:\n',text,type(text))
			#匹配日期
            list_num1 = re.findall('\d{4}-\d{2}-\d{2}',text)
			#匹配彩票期数
            list_num2 = re.findall('\d{7}',text)
			#匹配彩票号码			
            list_num3 = re.findall('\d{2}\n\d{2}\n\d{2}\n\d{2}\n\d{2}\n\d{2}\n\d{2}',text)
            #print('list_num3:\n',list_num3,type(list_num3))
            
            #将彩票信息写入文件，格式如下：
			#2017-12-12,2017146,01,19,25,26,27,33,10
            if len(list_num1) >0 :
                linetext += text
                continue
            elif len(list_num2) >0 :
                linetext += ',' + text
                continue
            elif len(list_num3) > 0:
                linetext += ',' + list_num3[0].replace('\n',',') + '\n'
                print('LineText:\n',linetext)
                fp.write(linetext)
                continue
            else:
                linetext=''
    fp.close()

#===============================================================================
if __name__=="__main__":

    pageNum = getPageNum(url)	
    getpagetext = getText(url)  

