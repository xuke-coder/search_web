# search_web
search web page for fun

用python 爬虫工具去爬知乎网页，并存储
之后，在nginx上建一个搜索服务器，可以搜索关键字，php脚本查找爬出来的网页内容，并显示搜索出来的网页链接及快照

spider目录为爬虫源码目录
使用：(目前爬虫程序只支持python3)
python3 ./spider/main.py
之后会在配置的目录中存储爬到的网页

web目录为nginx要使用的php脚本目录，其中有一个nginx.conf是配置文件

