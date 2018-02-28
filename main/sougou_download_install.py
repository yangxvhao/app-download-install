#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'yangxvhao'


import requests
import json
import os
from bs4 import BeautifulSoup
from main import common_util as common


# apk安装包位置
path = '/home/yangxvhao/apk/6.8'

# 要下载的apk名称所在文件
apk_file_path = '/home/yangxvhao/apk/6.8/app.txt'

# 地址
root_url = 'http://as.sogou.com/so?w=1459&uID=lWDsPu4FxJN1QlVw&pid=34&query='


def download(is_install, *appnames):
    not_find_list = []
    if not os.path.exists(path):
        print('文件夹不存在')
        return
    for name in appnames:
        # 查找apk下载地址
        response = requests.get(root_url + name)
        soup = BeautifulSoup(response.content)
        result = soup.select('div.andriod_soft_item')[0]
        appname = result.span.string
        url_json_str = result.select('span.download_btn')[0].a['data-hd']
        app_url = json.loads(url_json_str)['sogouHighdownUrl']

        # 下载apk
        if appname == name:
            print('已找到app,下载中......')
            apk_response = requests.get(app_url)
            apk_file = os.path.join(path, appname + '.apk')

            with open(apk_file, 'wb') as code:
                code.write(apk_response.content)

            if os.path.exists(apk_file):
                print(appname + '下载成功！')

        else:
            not_find_list.append(appname + ',')

    print('全部下载完成,未找到的app: %s' % not_find_list)

    if is_install:
        common.install(path)


if __name__ == '__main__':
    download(False, *common.read_file(apk_file_path))
    download(True, '友借')