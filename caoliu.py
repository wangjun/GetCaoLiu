#!/usr/bin/env python
#coding=utf-8
# Author:Richard Liu
# Email: <richardxxx0x@gmail.com>

"""
下载草榴社区视频
"""
import os
import sys
import re
import requests
import argparse
import eventlet

confirm_yes = ['y','ye','yes']
headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml; " \
        "q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding":"text/html",
    "Accept-Language":"en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2",
    "Content-Type":"application/x-www-form-urlencoded",
    "User-Agent":"Mozilla/5.0 (X11; CrOS x86_64 6253.0.0) AppleWebKit/537.36 " \
    "(KHTML, like Gecko) Chrome/39.0.2151.4 Safari/537.36"
}

ss = requests.session()
ss.headers.update(headers)

class CaoLiu(object):
    def __init__(self, url=None):
        self.url = url
        
    def get_link(self):
        """
        输入url后，获取的视频src链接
        """
	try:
	        with eventlet.Timeout(10):
			r = ss.get(self.url)
		if r.ok:
		    link_search = re.search(r'src=(http.+?\&mp4=1)', r.content)
		    if link_search:
			link = link_search.group(1)
			# print link
			
		    # name_search = re.search(r'<title>(.*)\[\d+.*</title>', r.content)
		    # if name_search:
		    #     name = name_search.group(1)
		    #     print name
		    else:
			print "This page has no mp4 url"
			sys.exit()
		else:
		    print "Please check your network.Beacause these website need proxy.But the domain 5.yao.cl do not need"
		    sys.exit(1)
		
		"""
		获取真正的video链接
		"""
		r = ss.get(link)
		if r.ok:
		    link_search = re.search(r'file: "(http.+?\.mp4)', r.content)
		    if link_search:
			link = link_search.group(1)
			print "Video url is :",link
			confirm  = raw_input("Want to download video(y/n): ").lower()
			if confirm in confirm_yes:
				self.download(link)
			else:
				sys.exit(0)
                    else:
			print "This page has no mp4 url"
			sys.exit()
		else:
		    print "Get video real link failed"
		    sys.exit(2)
	except KeyboardInterrupt:
		sys.exit()

    def download(self,link):
        if args.axel:
            cmd = 'axel -a %s' % (link)
        else:
            cmd = 'wget %s' % (link)
        # status = os.system(cmd)
        os.system(cmd)
    def do(self):
        self.get_link()
        
def main(url):
    caoliu = CaoLiu(url)
    caoliu.do()
 
if __name__ == "__main__":
    """
    添加命令行参数
    """
    parser = argparse.ArgumentParser(description='Download videos from t66y.com or 5.yao.cl ')
    parser.add_argument('url', help='url of http://t66y.com or http://5.yao.cl')
    parser.add_argument('-a', '--axel', action='store_true', \
                    help='download with axel')
    parser.add_argument('-w', '--wget', action='store_true', \
                    help='download with wget')
    args = parser.parse_args()
    
    main(args.url)
