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
        # 返回了一个json，里面是每一页的数据
        for item in content_json["app_msg_list"]:
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
    apptoken从客户端打开的文章后，fiddler上获取
    appmsg_token 从客户端打开文章的源代码获取。
    """
    # 使用Cookie，跳过登陆操作,Cookie一天左右会变化，注意更新
    mpCookie = 'pgv_pvi=3051430912; RK=NJTgHLR1eM; ptcz=b3d6517af75af27a7c96f6cf71a5560088c4823f99fa5a8d71ab7b4ec0a357e7; pgv_pvid=3371384032; o_cookie=465626040; pac_uid=1_465626040; tvfe_boss_uuid=3841b6cb909d7b56; ua_id=gNffOGkUzvA7qlVFAAAAAF5vW00Fnip2-hO4YhcSUUQ=; mm_lang=zh_CN; noticeLoginFlag=1; openid2ticket_o817K1bYQc4rnK6Tmk3bZf58raO4=gPzMQ+0wGT4wqZYQPEE/lPbWvg+WJNF0DCc2cX0hz30=; pgv_si=s5634223104; cert=OAp6L0WYwV7iwPfC0sQSiLz0q0qS9OZs; sig=h01e3b3e459763468d3aac17c36a575101b216a14ede42eb32886554f463f92e069fd5e5f9c5aa14126; master_key=X/WjPkUvyY7aztS5nadXF9dF9jC6aNFscuDBlYamsDs=; pgv_info=ssid=s6291140483; _qpsvr_localtk=0.2825344850486893; uin=o0465626040; skey=@tXR9xbZqH; ptisp=cm; uuid=b485ebf692ff04bf816533565e6b6aca; data_bizuin=3586809587; bizuin=3586809587; data_ticket=6ZfI7Ba6v6lpMYCYCn4TbJ357gNf2659jx9NmzwiuHLB0Lbfb1n2MA+Cm6A/E2UK; slave_sid=QUVneW1NWnFLMFF5U0JzdmhvYm9EemVCTl8xU2tXTHZyYVNHVUZtVEY1eTdxbkRFMjJNYkdSeDRZc3pxMThHWG8xNzBacXRoSnpIcjVVNlBSaWh3RG54Q0JJR3RDeklZR21UY29mOExwZlpxUkFrQ09ZN0ZJVG1IVU9nR3ZEY0RpNUlLV3dqMHpocEtvMjRQ; slave_user=gh_224e78dd7523; xid=bc0d5a910541a1277f67c304b73621d8'
    mptoken = 1288978987
    appCookie = 'rewardsn=; wxuin=856784061; devicetype=Windows10; version=62060833; lang=zh_CN; pass_ticket=Du0QmpW30i+AabOvjGOw3nPAAc1d5hGbzMUSNySpEJ0dj6Wu+sNAZ013k3xNDl0j; wap_sid2=CL35xZgDElxobXYyRlROZ0RVUXBtV3FQMGwxX1NudVVPRTZkNFJDM05HRWl4NkdIZ05vbGhvRnZMRnlpV1Z0VUxySVgzeFI2R1p1R1ctWWdGNThNWW1MTGFzMU13ZmtEQUFBfjC77qHpBTgNQAE=; wxtokenkey=777'
    appmsg_token = '1017_saY89U7obW0xB2yeK9lBb3s490q40DVYCVdmOyV1-iU07eZpBHF5bulYLjnxt7GTM4xLI0S7OQMlU6rz'
    nickname = '找药宝典'
    fakeid = 'MzI3MjE2NzI4Mg=='
    #从第几页开始爬
    breakpage = 42
    #估算众号文章总页数，用以迭代
    articles_page_sum = 30
    ##爬取结果
    get_result(mpCookie,mptoken,fakeid,appCookie,appmsg_token,nickname,breakpage,articles_page_sum)
if __name__ == '__main__':
    main()
