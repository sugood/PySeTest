# Project  : PySeTest
# FileName : MyHTMLTestRunner.py
# Author   : sugood
# DateTime : 2020/10/13 13:04
# Github   : https://github.com/sugood/PySeTest
# Version  : 1.0.0

from HTMLTestRunner import HTMLTestRunner
import os,sys
import unittest
import time

#dirname=当前目录位置，filename=该py名称
dirname,filename=os.path.split(os.path.abspath(sys.argv[0]))

#通过defaultTestLoader来加载当前目录下所有名称为test开头的py
discover = unittest.defaultTestLoader.discover(dirname, pattern='test*.py', top_level_dir=None)

# 获取系统当前时间
now = time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))
day = time.strftime('%Y-%m-%d', time.localtime(time.time()))

# 定义个报告存放路径，支持相对路径
tdresult = "./"+ day

if os.path.exists(tdresult): # 检验文件夹路径是否已经存在
    filename = tdresult + "/" + now + "_result.html"
    fp = open(filename, 'wb')
    # 定义测试报告
    runner = HTMLTestRunner(stream=fp,
                            title='网页自动化测试报告',
                            description='执行情况：',
                            tester='sugood')

    # 运行测试用例
    runner.run(discover)
    fp.close()  # 关闭报告文件
else:
    os.mkdir(tdresult) # 创建测试报告文件夹
    filename = tdresult + "/" + now + "_result.html"
    fp = open(filename, 'wb')
    # 定义测试报告
    runner = HTMLTestRunner(stream=fp,
                            title='网页自动化测试报告',
                            description='执行情况：',
                            tester='sugood')

    # 运行测试用例
    runner.run(discover)
    fp.close()  # 关闭报告文件