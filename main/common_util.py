#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import subprocess

__author__ = 'yangxvhao'


def read_file(path):
    name_list = []
    if os.path.exists(path):
        f = open(path, 'r')
        for line in f.readlines():
            name_list.append(line.strip())
        return name_list
    else:
        print('文件不存在')


def install(path):
    not_install_list = []
    filelist = os.listdir(path)
    print('安装中.....')
    for file in filelist:
        filepath = os.path.join(path, file)
        if os.path.exists(filepath):

            status,output = subprocess.getstatusoutput('adb install ' + filepath)

            if output.split('\n')[-1] != 'Success':
                not_install_list.append(file + ',')
    print('安装完成，安装失败的app: %s ' % not_install_list)


if __name__ == '__main':
    install('')