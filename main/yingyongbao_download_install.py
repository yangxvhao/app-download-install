#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'yangxvhao'

import requests
import json
import os
import sys

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
import main.common_util as common


# apk安装包位置
path = '/home/yangxvhao/apk/6.9'

# 要下载的apk名称所在文件
apk_file_path = '/home/yangxvhao/apk/6.8/app.txt'

# 地址
root_url = 'http://mapp.qzone.qq.com/cgi-bin/mapp/mapp_search_result?keyword='


def download(is_install, *appnames):
    not_find_list = []
    if not os.path.exists(path):
        print('文件夹不存在')
        return
    for name in appnames:
        # 查找app下载地址
        response = requests.get('http://mapp.qzone.qq.com/cgi-bin/mapp/mapp_search_result?keyword=' + name)
        response_json = json.loads(str(response.content, encoding="utf-8").replace(';', ''))['apps'][00]
        app_name = response_json['name']
        app_url = response_json['url']

        if app_name == name:
            # 下载apk文件
            print('已找到app,下载中......')
            apk_file = os.path.join(path, app_name + '.apk')
            apk_response = requests.get(app_url).content
            with open(apk_file, 'wb') as file:
                file.write(apk_response)
            if os.path.exists(apk_file):
                print(app_name + '下载成功！')

        else:
            not_find_list.append(app_name + ',')

    print('全部下载完成,未找到的app: %s' % not_find_list)

    if is_install:
        common.install(path)


if __name__ == '__main__':
    # download(False, *common.read_file(apk_file_path))
    download(False, '友借')