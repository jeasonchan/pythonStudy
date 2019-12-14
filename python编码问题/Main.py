# coding=utf-8
import os
import sys

if __name__ == '__main__':
    path: str = "哈哈哈哈"
    path2: str = "嘿嘿嘿".encode("utf8").decode("utf8")
    print(path, path2)

    print("\n=============================")
    print("系统默认编码是:", sys.getdefaultencoding(), "\n")

    filelist: list = os.listdir("C:\\CRroot\\documents\\")  # 此处返回的list中的中文是以GBK编码的，你可以通过查看cmd窗口属性看到。
    for path in filelist:
        # if os.path.isdir(path):
        print(path, os.path.isfile(path), type(path))

    fileStream = open(".\\GBK编码的中文文档.txt", "rb")
    print(fileStream.read())  # 输出是 b'\xd2\xbb\xbe\xe4\xd6\xd0\xce\xc4\na english\n'

    fileStream = open(".\\GBK编码的中文文档.txt", "rb")
    try:
        print(fileStream.read().decode("utf8"))
        # 输出是 'utf-8' codec can't decode byte 0xbe in position 2: invalid
        # start byte <class 'UnicodeDecodeError'>
    except Exception as message:
        print(message, type(message))

    fileStream = open(".\\GBK编码的中文文档.txt", "rb")
    print(fileStream.read().decode("gbk"))  # 输出是的是正确的GBK文档中的中文内容'

    s: str = "hahaah啊啊哈哈"
    print(type(s), s, len(s))
    s_unicode = u"hahaah啊啊哈哈" # 和上面的一样，只是显式声明，是一个unicode编码的字符穿
    print(type(s_unicode), s_unicode, len(s_unicode))

    s_bytes: bytes = s_unicode.encode()  # 字节串
    print(s_unicode.encode())
    print(s_bytes.decode("gbk"))
    print(s_bytes.decode("utf8"))
