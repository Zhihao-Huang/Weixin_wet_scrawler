# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 2019

@author: huangzhihao
"""

# -*- coding: utf-8 -*-
import requests
import time
import re

###评论数和点赞数的方法
def get_read_like_num(app_params):
    origin_url = "https://mp.weixin.qq.com/mp/getappmsgext?"
    headers2 = {
        "Cookie": app_params['appcookie'],
        # 添加Cookie避免登陆操作，cookie可以从fiddler获取，这里的"User-Agent"最好为手机浏览器的标识
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.27.400 QQBrowser/9.0.2524.400"
    }
    data2 = {
        "is_only_read": "1",
        "is_temp_url": "0",                
        "appmsg_type": "9", # 新参数，不加入无法获取like_num
    }
    my__biz= app_params["my__biz"]
    article_mid = app_params["article_mid"]
    article_sn = app_params["article_sn"]
    article_idx = app_params["article_idx"]
    appmsg_token = app_params["appmsg_token"]
    appmsgext_url = origin_url + "__biz={}&mid={}&sn={}&idx={}&appmsg_token={}&x5=1".format(my__biz, article_mid, article_sn, article_idx, appmsg_token)
    try:
        content = requests.post(appmsgext_url, headers=headers2, data=data2,timeout = 10).json()
        return(content["appmsgstat"]["read_num"], content["appmsgstat"]["like_num"])
    except:
        print("No response from article <mid"+article_mid+' sn'+article_sn+' idx'+article_idx+"> in 10s, pass.\n")
        return('NA', 'NA')
    #print(content["appmsgstat"]["read_num"], content["appmsgstat"]["like_num"])

def get_result(mpCookie,mptoken,fakeid,appCookie,appmsg_token,nickname,breakpage,articles_page_sum):
    ##breakpage 记录在第几页出错或终止，page记录当前页数, art_num记录当前文章总数
    breakpage = breakpage
    page = 0
    art_num = 0
    miss_article = []
    miss_page = []
    fout = open(nickname +'文章信息_起始页'+str(breakpage)+'.txt','w')
    fout.write('标题\t发布时间\t副标题简介\t链接\t阅读量\t点赞量\n')
    # 目标url
    url = "https://mp.weixin.qq.com/cgi-bin/appmsg"
    headers = {
        "Cookie": mpCookie,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
    }
    for i in range(articles_page_sum):
        data = {
            "token": mptoken,
            "lang": "zh_CN",
            "f": "json",
            "ajax": "1",
            "action": "list_ex",
            "begin": 5*(i+breakpage),
            #"begin": 180,
            "count": "5",
            "query": "",
            "fakeid": fakeid,
            "type": "9",
        }
        # 使用get方法进行提交
        try:
            #socket.setdefaulttimeout(10)
            content_json = requests.get(url, headers=headers, params=data,timeout = 10).json()
        except:
            print("No response from Page "+str(data['begin'])+" in 10s, pass.\n")
            miss_page.append(data['begin'])
        ##检查返回值是否正常
        try:
            dict_info =  content_json["app_msg_list"]
        except:
            print('获取url异常。')
            fout.close()
            break
        # 返回了一个json，里面是每一页的数据
        for item in dict_info:
            timestamp = item["update_time"]#转换成localtime
           # timestamp = 1540551261
            time_local = time.localtime(timestamp)
            #转换成新的时间格式(2016-05-05 20:28:54)
            dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
            # 提取每页文章的标题及对应的url
            #print(item["title"]+'\t'+ dt +'\t'+ item['digest']+'\t'+item["link"] +'\n')
            info = item["title"]+'\t'+ dt +'\t'+ item['digest']+'\t'+item["link"]
            #获取阅读量点赞量
            link = item['link']
            app_params = {
                "appcookie" : appCookie,
                "my__biz" : fakeid,
                "article_mid" : re.findall(r'mid=(.+?)&',link)[0],
                "article_sn" :  re.findall(r'sn=(.+?)&',link)[0],
                "article_idx" :  re.findall(r'idx=(.+?)&',link)[0],
                "appmsg_token" : appmsg_token
                }
            read_num,like_num = get_read_like_num(app_params)
            info2 = info+'\t'+str(read_num)+'\t'+str(like_num)+'\n'
            #可能会出现编码错误，先放在miss_article里。
            try:
                fout.write(info2)
            except:
                miss_article.append(info)
            art_num += 1
            print('Article: '+str(art_num)+". Release time: "+dt)
            time.sleep(10)
        page += 1
        print('Page: '+str(page)+"\n\n")
        ##小于2018年时，跳出循环
        if timestamp < 1514736000:
            break
        #time.sleep(60)
    fout.close()
    breakpage = page + 1
    f_info = open('breakpage.txt','w')
    page_info = "翻页断点： "+ str(breakpage-1) + "\n已爬文章数：" +str(art_num)
    print(page_info)
    f_info.write(page_info)
def main():
    """
    添加请求参数
    mpCookie,mptoken,fakeid从公众号的网页源代码获取
    mid、sn、idx分别对应每篇文章的url的信息，需要从url中进行提取
    appcookie从客户端打开的文章后，fiddler上获取
    appmsg_token 从客户端打开文章的源代码获取。
    """
    # 使用Cookie，跳过登陆操作,Cookie一天左右会变化，注意更新
    mpCookie = 
    mptoken = 
    appCookie = 
    appmsg_token = 
    fakeid = 
    #目标公众号名称
    nickname = 
    #从第几页开始爬
    breakpage = 0
    #众号文章总页数，用以迭代。总页数可以从公众号搜索栏的右下角获取。
    articles_page_sum = 2
    ##爬取并输出结果
    get_result(mpCookie,mptoken,fakeid,appCookie,appmsg_token,nickname,breakpage,articles_page_sum)
if __name__ == '__main__':
    main()
