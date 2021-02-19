#!/usr/bin/python
# coding=utf-8

import os
import sys
import argparse
import subprocess


class Const:
    toolName = "jeason_tool"
    toolVersion = "1.0"

    peopleRanges = "peopleRanges"
    ageRanges = "ageRanges"
    unknownRange = "unknown"

    start = "start"
    end = "end"
    queryCommandTemplate = "exe1 \"string_params\""
    configCommandTemplate = "exe2 -a value={}"
    EXIT_WITH_SUCCESS = "EXIT WITH SUCCESS"
    EXIT_WITH_CANCEL = "EXIT WITH CANCEL"
    EXIT_WITH_ERROR = "EXIT WITH ERROR"


class ModifyType:
    __enum = [Const.peopleRanges, Const.ageRanges, Const.unknownRange]

    @staticmethod
    def getModifyType(inputStr):
        """

        :param inputStr: str
        :return: str
        """
        ret = inputStr
        for eachType in ModifyType.__enum:
            if eachType.lower() == inputStr.lower():
                return eachType

        return ret


class Util:
    @staticmethod
    def trans2BinaryTuple(numberStr):
        numberStr = str(numberStr).strip()
        if (numberStr.isdigit()):
            return (numberStr, numberStr)
        else:
            raise Exception("{} is not numeric".format(numberStr))

    @staticmethod
    def add_range(items, start, end):
        """
        add a new range

        """

        if len(items) == 0:
            items = []
            items.append({"start": str(start), "end": str(end)})
            return items
        idx = 0
        for item in items:
            istart = long(item["start"])
            iend = long(item["end"])
            if istart > end:
                items.insert(idx, {"start": str(start), "end": str(end)})
                break
            idx = idx + 1
        if idx == len(items):
            items.append({"start": str(start), "end": str(end)})
        idx = 0
        iitem = []
        while idx < len(items) - 1:
            c_end = long(items[idx]["end"])
            n_start = long(items[idx + 1]["start"])
            if n_start - c_end <= 1:
                d = {"start": items[idx]["start"], "end": items[idx + 1]["end"]}
                items.pop(idx + 1)
                items.pop(idx)
                items.insert(idx, d)
                continue
            iitem.append(items[idx])
            idx = idx + 1
        if idx == len(items) - 1:
            iitem.append(items[idx])

        return iitem

    @staticmethod
    def remove_range(items, start, end):
        """
        remove a  range

        """
        if len(items) == 0:
            print("range is empty")
            exit(-1)

        idx = 0
        while idx < len(items):
            istart = long(items[idx]["start"])
            iend = long(items[idx]["end"])
            if (start >= istart) and (end <= iend):
                part1_end = start - 1
                part2_start = end + 1
                items.pop(idx)
                i = idx
                if part1_end >= istart:
                    items.insert(i, {"start": str(istart), "end": str(part1_end)})
                    i = i + 1
                if iend >= part2_start:
                    items.insert(i, {"start": str(part2_start), "end": str(iend)})
                break
            idx = idx + 1

        return items


class Logger:
    """
    用来记日志，但是发现python已经自带的日志记录模块了
    """
    def __int__(self):
        pass

    def append(self, content):
        print(content)


import json
import types


class MyRange:
    def __init__(self, modifyType, commandStr):
        self.__modifyType = ModifyType.getModifyType(modifyType)

        # obj json string
        self.__objectJsonStr = commandStr

        self.__indexOfLeft = -1
        self.__indexOfRight = -1

        # list[dict]
        self.__rangeList = []

        self.__initRangeList()

    def __initRangeList(self):
        indexOfTarget = self.__objectJsonStr.find(self.__modifyType)
        if indexOfTarget < 0:
            raise Exception("No {} config found!".format(self.__modifyType))

        self.__indexOfLeft = self.__objectJsonStr.find("[", indexOfTarget)
        self.__indexOfRight = self.__objectJsonStr.find("]", indexOfTarget)
        originalRangeStr = self.__objectJsonStr[self.__indexOfLeft:self.__indexOfRight + 1]
        originalRange = json.loads(originalRangeStr)

        for eachDict in originalRange:
            self.__rangeList.append(eachDict)

        # print(self.__rangeList)

    def getModifyType(self):
        return self.__modifyType

    def getRangeList(self):
        return self.__rangeList

    def getCoveredRange(self, portStr):
        ret = {}
        for eachDict in self.__rangeList:
            currentNumber = int(portStr)
            leftNumber = int(eachDict[Const.start])
            rightNumber = int(eachDict[Const.end])
            if leftNumber <= currentNumber <= rightNumber:
                ret = eachDict
                break
        return ret

    def addRange(self, range):
        """
        add a point or a range
        :param range:str|(str,str)
        :return:None
        """
        rangeType = type(range)

        if rangeType == types.TupleType:
            self.__addRange(range)
        elif rangeType == types.StringType:
            self.__addRange(Util.trans2BinaryTuple(range))
        else:
            raise Exception("unknown rangeType {}".format(rangeType))

    def __addRange(self, rangeTuple):
        """
        add a range
        :param rangeTuple:(str,str)
        :return:None
        """
        # print(rangeTuple)
        rangeTuple = tuple(rangeTuple)
        self.__rangeList = Util.add_range(self.__rangeList, long(rangeTuple[0]), long(rangeTuple[1]))

    def removeRange(self, range):
        """
       remove a point or a range
       :param range:str|(str,str)
       :return:None
       """
        rangeType = type(range)

        if (rangeType == types.TupleType):
            self.__removeRange(range)
        elif (rangeType == types.StringType):
            self.__removeRange(Util.trans2BinaryTuple(range))
        else:
            raise Exception("unknown rangeType {}".format(rangeType))

    def __removeRange(self, rangeTuple):
        """
        remove a range
        :param rangeTuple:(str,str)
        :return:
        """

        rangeTuple = tuple(rangeTuple)
        self.__rangeList = Util.remove_range(self.__rangeList, long(rangeTuple[0]), long(rangeTuple[1]))

        pass

    def getNewObjJsonStr(self):
        return self.__objectJsonStr[0:self.__indexOfLeft] + \
               json.dumps(self.__rangeList).replace(" ", "") + self.__objectJsonStr[self.__indexOfRight + 1:-1]


# ==========================================================================================
# ==========================================================================================
# ==========================================================================================
# ==========================================================================================
# ==========================================================================================

print("input argv is {}".format(sys.argv))

parser = argparse.ArgumentParser(prog=Const.toolName,
                                 description="add and remove {} and {}".format(Const.peopleRanges, Const.ageRanges))
parser.add_argument("--version", "-v", action="version", version='%(prog)s {}'.format(Const.toolVersion))
parser.add_argument('--type', '-t', action="store", choices=[Const.peopleRanges, Const.ageRanges], required=True)
parser.add_argument('--add', '-a', nargs="+", action='store',
                    help='add a range or single value or several values and ranges, such as: \n {} -a 123 456 ;\n {} -a 123,456 666,789 ;\n {} -a 123 456 666,789'.format(
                        Const.toolName, Const.toolName, Const.toolName))
parser.add_argument('--remove', '-r', nargs="+", action='store',
                    help='remove a range or single value or several values and ranges, such as: \n {} -r 123 456 ;\n {} -r 123,456 666,789 ;\n {} -r 123 456 666,789'.format(
                        Const.toolName, Const.toolName, Const.toolName))

parseredArgs = parser.parse_args()

modifyTarget = parseredArgs.type
print("type inputs:{}".format(modifyTarget))

# such as ['123', '456,456']
add_list = parseredArgs.add
if add_list:
    print("add inputs:{}".format(add_list))

# such as ['123', '456,456']
remove_list = parseredArgs.remove
if remove_list:
    print("remove inputs:{}".format(remove_list))

resultFile = None
try:

    resultFile = os.popen(Const.queryCommandTemplate)
    resultStrArray = resultFile.readlines()
    print("query command result:\n{}".format(resultStrArray))

    if len(resultStrArray) < 3:
        raise Exception("result too short!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    result = resultStrArray[2]

finally:
    if resultFile:
        resultFile.close()

indexOfObjStart = result.find("{")
indexOfObjEnd = result.rfind("}")
paramRange = MyRange(modifyTarget, result[indexOfObjStart:indexOfObjEnd + 1])

print("{}\nfrom :\n{}".format(paramRange.getModifyType(), paramRange.getRangeList()))
if add_list:
    for index in range(0, len(add_list)):
        each = add_list[index]
        if each.find(",") < 0:
            paramRange.addRange(each)
        else:
            tempArray = each.split(",")
            paramRange.addRange((tempArray[0], tempArray[1]))

if remove_list:
    for index in range(0, len(remove_list)):
        each = remove_list[index]
        if each.find(",") < 0:
            paramRange.removeRange(each)
        else:
            tempArray = each.split(",")
            paramRange.removeRange((tempArray[0], tempArray[1]))

print("to :\n{}".format(paramRange.getRangeList()))
comfirm = raw_input("Continue with \"y\" or cancel with \"n\":")

if (comfirm == "n" or comfirm == "N"):
    print(Const.EXIT_WITH_CANCEL)
    exit()

# 拼凑配置字符串，回写配置
newObjJsonStr = paramRange.getNewObjJsonStr()

# 借助json进一步转义，以作为shell的字符串参数
temp = json.dumps([newObjJsonStr])
configCommandStr = Const.configCommandTemplate.format(temp[1:len(temp)])

print("config command is: {}".format(configCommandStr))

resultFile = None
try:
    resultFile = os.popen(configCommandStr)
    resultStrArray = resultFile.readlines()
    print("config command result:\n{}".format(resultStrArray))

    if len(resultStrArray) > 0:
        print(Const.EXIT_WITH_ERROR)
    else:
        print(Const.EXIT_WITH_SUCCESS)

finally:
    if resultFile:
        resultFile.close()
