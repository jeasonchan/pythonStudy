# coding=utf-8
import os
import sys

if __name__ == '__main__':
    argvArray: list[str] = sys.argv
    print("sys.argv: {}".format(argvArray))

    fileName: str = "哈哈哈哈"
    path2: str = "嘿嘿嘿".encode("utf8").decode("utf8")
    print(fileName, path2)

    print("\n=============================")
    print("the current default encoding used by the Unicode implementation:", sys.getdefaultencoding(), "\n")

    currentPath: str = argvArray[0][0:argvArray[0].rfind("/") + 1]
    filelist: list = os.listdir(currentPath)  # 此处返回的list中的中文是以GBK编码的，你可以通过查看cmd窗口属性看到。
    for fileName in filelist:
        # if os.path.isdir(path):
        print(fileName, os.path.isfile(fileName), type(fileName))

    fileStream = open(".\\GBK编码的中文文档.txt", "rb")
    print(fileStream.read())  # 输出是 b'\xd2\xbb\xbe\xe4\xd6\xd0\xce\xc4\na english\n'

    fileStream = open(".\\GBK编码的中文文档.txt", "rb")
    try:
        print(fileStream.read().decode("utf8"))
        # 输出是 'utf-8' codec can't decode byte 0xbe in position 2: invalid
        # 因为fileStream这个是二进制流，试图以utf-8将二进制转码时，必然会错误，遇到utf-8中不会出现的二进制段
        # start byte <class 'UnicodeDecodeError'>
    except Exception as message:
        print(message, type(message))

    fileStream = open(".\\GBK编码的中文文档.txt", "rb")
    print(fileStream.read().decode("gbk"))  # 输出是的是正确的GBK文档中的中文内容'

    s: str = "hahaah啊啊哈哈"  # python3默认就是unicode编码
    print(type(s), s, len(s))
    s_unicode = u"hahaah啊啊哈哈"  # 和上面的一样，只是显式声明，是一个unicode编码的字符穿
    print(type(s_unicode), s_unicode, len(s_unicode))

    s_bytes: bytes = s_unicode.encode()  # 字节串转二进制，code有种二进制的意思，不写应该是默认使用utf-8
    print(s_unicode.encode())  # print输出这串字节数组时
    print(s_bytes.decode("gbk"))
    print(s_bytes.decode("utf8"))
