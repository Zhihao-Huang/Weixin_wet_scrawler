# Weixin_wet_scrawler
爬取微信公众号文章永久链接、阅读量、在看量等。
微信公众号爬虫
本程序目标是爬取公众号文章的永久链接，阅读量，在看量等。
 
一、需要的工具：
python3.6
Fiddler4
个人微信
个人订阅号。

二、需要输入的信息：
个人订阅号的cookie和token
个人微信号的cookie和appmsg_token
目标公众号的fakeid

三、输入信息获取方法：
1、	个人订阅号的cookie，token和目标公众号的fakeid
首先要注册一个个人订阅号，网页登录账号，首页左栏点击素材管理，点击新建图文素材，上栏界面有一个超链接，可以搜索其他公众号文章。点击目标公众号之前先按F12打开开发者模式，点击目标公众号，右边产生appmsg开头的选项，点击该选项，即可获取个人订阅号的Cookie，token和目标公众号的fakeid。
2、个人微信号的cookie和appmsg_token
获取个人微信号的cookie需要工具辅助，用fiddler抓包软件。Fiddler是免费软件，下载安装很方便。打开fiddler后开始监听，然后用电脑微信客户端打开公众号文章，fiddler里会出现一行含有/mp/jsreport选项，点击，在右边点击Raw，即可复制Cookie。
appmsg_token可以直接右键打开源代码搜索获取。
   
四、代码
见github链接：
https://github.com/Zhihao-Huang/Weixin_wet_scrawler/blob/master/Wet_scrawler.py

本方法参考博客：
https://blog.csdn.net/wnma3mz/article/details/78570580


