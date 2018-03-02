#! /usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'yangxvhao'


from bs4 import BeautifulSoup
import json
import os
import random
import common_util as common

# apk安装包位置
path = r'/home/yangxvhao/apk/new'

# 要下载的apk名称所在文件
apk_file_path = r'/home/yangxvhao/apk/6.8/app.txt'


def downloads(*names):
    not_find_list = []
    if len(os.listdir(path)) != 0:
        print('下载文件夹必须为空文件夹！请新建文件夹或清空')
        exit(0)
    for name in names:
        if not download(name):
            not_find_list.append(name)
    if len(not_find_list) == 0:
        print('下载完成！')
    else:
        print('未找到的app:' + str(not_find_list))


def download(name):
    return mi_download(name) or sougou_download(name) or yingyongbao_download(name)


def mi_download(name):
    try:
        # 域名地址
        host = 'http://app.mi.com'
        root_url = 'http://app.mi.com/search?keywords='
        url = root_url + name
        response = common.url_get(url).content
        soup = BeautifulSoup(response, 'lxml')
        result_list = soup.select('ul.applist')[0].select('li')
        for result in result_list:
            app_name = result.h5.string
            if app_name == name:
                # 查找下载地址
                print('小米已找到app,[%s] 下载中......' % app_name)
                app_url = result.h5.a['href']
                detail_response = common.url_get(host + app_url).content
                detail_soup = BeautifulSoup(detail_response, 'lxml')
                download_url = host + detail_soup.select('a.download')[0]['href']

                # 下载apk文件
                return common.download_apk(path, app_name, download_url)
    except Exception as e:
        print(str(e))

    return False


def sougou_download(name):
    try:
        # 地址
        root_url = 'http://as.sogou.com/so?w=1459&uID=lWDsPu4FxJN1QlVw&pid=34&query='
        # 查找apk下载地址
        response = common.url_get(root_url + name)
        soup = BeautifulSoup(response.content, "lxml")
        result_list = soup.select('div.andriod_soft_item')
        for result in result_list:
            app_name = result.span.string
            if app_name == name:
                print('搜狗已找到app,[%s] 下载中......' % app_name)
                url_json_str = result.select('span.download_btn')[0].a['data-hd']
                app_url = json.loads(url_json_str)['sogouHighdownUrl']

                # 下载apk文件
                return common.download_apk(path, app_name, app_url)
    except Exception as e:
        print(str(e))
    return False


def yingyongbao_download(name):
    try:
        # 查找app下载地址
        response = common.url_get('http://mapp.qzone.qq.com/cgi-bin/mapp/mapp_search_result?keyword=%s&platform='
                                'touch&network_type=undefined&resolution=360x640&r=0.%s' %
                                (name, str(random.randint(0, 9999999999999999))))
        apps = json.loads(str(response.content, encoding="utf-8").replace(';', ''))['apps']
        for app in apps:
            app_name = app['name']
            if app_name == name:

                print('应用宝已找到app,[%s] 下载中......' % app_name)
                app_url = app['url']
                # 下载apk文件
                return common.download_apk(path, app_name, app_url)

    except Exception as e:
        print(str(e))
    return False


if __name__ == '__main__':
    downloads(*common.read_file(apk_file_path))
    # downloads('友借')
    # common.install(path)
