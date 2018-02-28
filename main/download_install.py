#! /usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'yangxvhao'


from bs4 import BeautifulSoup
import json
import os
from pypinyin import lazy_pinyin
import requests
import random
import common_util as common

# apk安装包位置
path = '/home/yangxvhao/apk/6.9'

# 要下载的apk名称所在文件
apk_file_path = r'/home/yangxvhao/apk/6.8/app.txt'


def downloads(*names):
    not_find_list = []
    for name in names:
        if not download(name):
            not_find_list.append(name)
    print('未找到的app:' + str(not_find_list))


def download(name):
    return mi_download(name) or sougou_download(name) or yingyongbao_download(name)


def mi_download(name):
    try:
        #域名地址
        host = 'http://app.mi.com'
        root_url = 'http://app.mi.com/search?keywords='
        url = root_url + name
        response = requests.get(url).content
        soup = BeautifulSoup(response, 'lxml')
        result_list = soup.select('ul.applist')[0].select('li')
        for result in result_list:
            app_name = result.h5.string
            if app_name == name:
                # 查找下载地址
                print('小米已找到app,下载中......')
                app_url = result.h5.a['href']
                detail_response = requests.get(host + app_url).content
                detail_soup = BeautifulSoup(detail_response, 'lxml')
                download_url = host + detail_soup.select('a.download')[0]['href']

                # 下载apk文件
                apk_response = requests.get(download_url)
                apkfile = os.path.join(path, ''.join(lazy_pinyin(app_name)) + '.apk')

                with open(apkfile, "wb") as code:
                    code.write(apk_response.content)

                if os.path.exists(apkfile):
                    print('下载成功:' + app_name)
                    return True
    except Exception as e:
        print(str(e))

    return False


def sougou_download(name):
    try:
        # 地址
        root_url = 'http://as.sogou.com/so?w=1459&uID=lWDsPu4FxJN1QlVw&pid=34&query='
        # 查找apk下载地址
        response = requests.get(root_url + name)
        soup = BeautifulSoup(response.content, "lxml")
        result_list = soup.select('div.andriod_soft_item')
        for result in result_list:
            app_name = result.span.string
            # 下载apk
            if app_name == name:
                print('搜狗已找到app,下载中......')
                url_json_str = result.select('span.download_btn')[0].a['data-hd']
                app_url = json.loads(url_json_str)['sogouHighdownUrl']
                apk_response = requests.get(app_url)
                apk_file = os.path.join(path, ''.join(lazy_pinyin(app_name)) + '.apk')

                with open(apk_file, 'wb') as code:
                    code.write(apk_response.content)

                if os.path.exists(apk_file):
                    print(app_name + '下载成功！')
                    return True
    except Exception as e:
        print(str(e))
    return False


def yingyongbao_download(name):
    # 查找app下载地址
    try:
        response = requests.get('http://mapp.qzone.qq.com/cgi-bin/mapp/mapp_search_result?keyword=%s&platform=touch&network_type=undefined&resolution=360x640&r=0.%s' % (name, str(random.randint(0, 9999999999999999))))
        apps = json.loads(str(response.content, encoding="utf-8").replace(';', ''))['apps']
        for app in apps:
            app_name = app['name']
            if app_name == name:
                # 下载apk文件
                print('应用宝已找到app,下载中......')
                app_url = app['url']
                apk_file = os.path.join(path, ''.join(lazy_pinyin(app_name)) + '.apk')
                apk_response = requests.get(app_url).content
                with open(apk_file, 'wb') as file:
                    file.write(apk_response)
                if os.path.exists(apk_file):
                    print(app_name + '下载成功！')
                    return True

    except Exception as e:
        print(str(e))
    return False


if __name__ == '__main__':
    # downloads(False, *common.read_file(apk_file_path))
    downloads('友借','秒分')
    # common.install(path)
