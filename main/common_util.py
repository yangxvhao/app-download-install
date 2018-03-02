#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import requests
import subprocess

from requests.adapters import HTTPAdapter
from pypinyin import lazy_pinyin

__author__ = 'yangxvhao'


def url_get(url):
    try:
        request = requests.Session()
        # 设置超时重试次数为3
        request.mount('http://', HTTPAdapter(max_retries=3))
        request.mount('https://', HTTPAdapter(max_retries=3))
        return request.get(url, timeout=3)
    except requests.RequestException as e:
        print('下载错误，请检查网络或稍后重试！')
    except requests.URLRequired as e:
        print('网站改版！')


def read_file(path):
    try:
        name_list = []
        if os.path.exists(path):
            f = open(path, 'r')
            for line in f.readlines():
                name_list.append(line.strip())
            return name_list
        else:
            print('文件不存在')
    except Exception as e:
        print(e)


def download_apk(path, apk_name, apk_url):
    try:
        apk_response = url_get(apk_url)
        apk_file = os.path.join(path, ''.join(lazy_pinyin(apk_name)) + '.apk')

        with open(apk_file, "wb") as code:
            code.write(apk_response.content)

        if os.path.exists(apk_file):
            print('下载成功:' + apk_name)
            return True
    except Exception as e:
        print(e)


def install(path):
    not_install_list = []
    try:
        file_list = os.listdir(path)
        if len(file_list) == 0:
            print('没有要安装的文件,请确认文件是否存在.')
            exit(0)
        print('安装中.....')
        for file in file_list:
            filepath = os.path.join(path, file)
            if os.path.exists(filepath):
                status, output = subprocess.getstatusoutput('adb install ' + filepath)
                fail_str = output.split('\n')[-1]
                if fail_str == 'Success':
                    print('%s 安装成功' % file)
                else:
                    not_install_list.append('%s : %s,' % (file, fail_str))
        if len(not_install_list) == 0:
            print('安装完成!!!')
        else:
            print('安装失败的app: %s ' % not_install_list)
    except Exception as e:
        print(e)


if __name__ == '__main':
    install('')
