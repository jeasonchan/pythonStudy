#!/usr/bin/python3

import os
import sys
import argparse
import subprocess


print("input argv is {}".format(sys.argv))


# description参数可以用于插入描述脚本用途的信息，可以为空
parser = argparse.ArgumentParser(prog="unknown_tool",description="your script description")
parser.add_argument("--version","-v", action="version", version='%(prog)s 1.0')

# 添加--verbose标签，标签别名可以为-v，这里action的意思是当读取的参数中出现--verbose/-v的时候
# 参数字典的verbose建对应的值为True，而help参数用于描述--verbose参数的用途或意义。
# 将变量以标签-值的字典形式存入args字典
# 默认已经添加了--help和-h
parser.add_argument('--add', '-a', action='append', help='add a range or single value')
parser.add_argument('--remove', '-r', action='append', help='remove a range or single value')



parseredArgs = parser.parse_args()        


add_list=parseredArgs.add
if(add_list):
    print("add inputs:{}".format(add_list))

remove_list=parseredArgs.remove
if(remove_list):
    print("remove inputs:{}".format(remove_list))


result = subprocess.call("cat /home/jeason/projects/pythonStudy/MainForFirstCommit.py",shell=True)
print(result)
"""
输出：
# encoding=utf-8

if __name__ == "__main__":
    print("hello world")
0

最后还带了一个0，表示主函数return 0这个返回值

"""

statusCode,output=subprocess.getstatusoutput("cat /home/jeason/projects/pythonStudy/MainForFirstCommit.py")
print("statusCode:{}".format(statusCode))
print(output)
"""
statusCode:0
# encoding=utf-8

if __name__ == "__main__":
    print("hello world")
"""


result=os.system("cat /home/jeason/projects/pythonStudy/MainForFirstCommit.py")
print(result)
"""
输出：
# encoding=utf-8

if __name__ == "__main__":
    print("hello world")
0

最后还带了一个0，表示主函数return 0这个返回值

"""


# f 是一个对象
f = os.popen("cat /home/jeason/projects/pythonStudy/MainForFirstCommit.py")
print(f)
data = f.readlines()
f.close()
print(data)
"""
从f对象中readlines读取程序的标准输出，形成数组
['# encoding=utf-8\n', '\n', 'if __name__ == "__main__":\n', '    print("hello world")\n']
"""


