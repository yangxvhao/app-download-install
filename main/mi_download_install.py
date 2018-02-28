#! /usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'yangxvhao'


import os
from bs4 import BeautifulSoup
import requests
import subprocess
from main import common_util as common

#apk安装包位置
path = '/home/yangxvhao/apk/6.8'

# 要下载的apk名称所在文件
apk_file_path = '/home/yangxvhao/apk/6.8/app.txt'

#域名地址
host = 'http://app.mi.com'
root_url = 'http://app.mi.com/search?keywords='


def download(is_install, *app_names):
    not_find_list = []
    if not os.path.exists(path):
        print('文件夹不存在')
        return
    for name in app_names:
        url = root_url + name
        response = requests.get(url).content
        soup = BeautifulSoup(response)
        result = soup.select('ul.applist')[0].select('li')[0]
        appname = result.h5.string
        app_url = result.h5.a['href']

        if appname == name:
            # 查找下载地址
            print('已找到app,下载中......')
            detail_response = requests.get(host + app_url).content
            detail_soup = BeautifulSoup(detail_response)
            download_url = host + detail_soup.select('a.download')[0]['href']
            # print('下载地址：' + download_url)

            # 下载apk文件
            apk_response = requests.get(download_url)
            apkfile = os.path.join(path, appname + '.apk')

            with open(apkfile, "wb") as code:
                code.write(apk_response.content)

            if os.path.exists(apkfile):
                print('下载成功:' + appname)

        else:
            not_find_list.append(name + ',')
    print('全部下载完成,未找到的app: %s' % not_find_list)

    if is_install:
        common.install(path)


if __name__ == '__main__':
    # download(False, *common.read_file(apk_file_path))
    download(True, '友借', '借几天')