#!/usr/bin/python
# -*- coding: UTF-8 -*-

from Tkinter import *           # 导入 Tkinter 库
import os
import os.path
import time

root = Tk()
root.resizable(width=False, height=False)

def nameTran(oldName):
    oldName=oldName.lower()
    oldName=oldName.replace(".xlsx", "_config.xml")
    return oldName

print (nameTran("Arenareward.xlsx"))

path = "./xmlConfig/"

allXmlFile = {}
needFile1 = []
needFile2 = []

filelist = os.listdir(".")
for filename in filelist:
    if filename.endswith(".xlsx"):
        # update_time = os.path.getctime(filename)#获取创建时间，返回值是标准时间，需要转换
        update_time = os.path.getmtime(filename)#获取最后修改时间，返回值是标准时间，需要转换
        # update_time = os.path.getatime(filename)#获取访问时间，返回值是标准时间，需要转换
        allXmlFile[nameTran(str(filename))] = update_time

allXmlFileSort = sorted(allXmlFile.iteritems(),
                        key=lambda f: f[1], reverse=True)

nowTime = 0
allDone = False
append = True

for key in allXmlFileSort:

    keyName = ""

    for b in key:
        keyName = b
        break

    time = allXmlFile[keyName]

    if time < 1635321600.0 :
        continue

    if nowTime == 0:
        nowTime = time
    elif (nowTime - time) > 3600.0:
        if append:
            nowTime = time
            append = False
        else:
            allDone = True
    else:
        nowTime = time

    if allDone:
        break
    else:
        if append:
            needFile1.append(keyName)
        else:
            needFile2.append(keyName)
length = 0

if len(needFile1) < 10:
    length+=len(needFile1)

if len(needFile2) < 10:
    length+=len(needFile2)

root.geometry("250x"+str(165+30*length)+"+600+400")

dic1 = {}
dicName = {}
index = 0

if len(needFile1) < 10:
    for file in needFile1:
        checkVar = StringVar(value="0")
        check = Checkbutton(root, text=str(file), variable=checkVar)
        check.select()
        check.grid()

        dic1[index] = checkVar
        dicName[index] = file
        index+=1

if len(needFile2) < 10:
    for file in needFile2:
        checkVar = StringVar(value="0")
        check = Checkbutton(root, text=str(file), variable=checkVar)
        check.grid()

        dic1[index] = checkVar
        index+=1

def uploadFile():
    for dicIndex in range(len(dic1)):
        if dic1[dicIndex].get() == "1" :
            uName = dicName[dicIndex]
            try :
                # os.system("scp xmlConfig/"+uName+" root@47.114.90.162:/data/main/configserver/test/")
                os.system("scp xmlConfig/"+uName+" root@47.114.90.162:/data/main/configserver/resources/data/")
            except :
                text.insert("end",">>> "+uName+'上传异常\n')
                continue 
            text.insert("end",">>> "+uName+'上传成功\n')

text=Text(root,width=100,height=10)
text.insert("end",'·出现并被选中的文件：最近一批次修改过的文件\n')
text.insert("end",'·出现未被选中的文件：是上一批次修改过的文件\n')
text.insert("end",'·两个文件修改时间没有超过1小时代表为一批次的修改\n')
text.insert("end",'·有问题找小阳\n')

if length ==0 :
    text.insert("end",'>>> 没有文件被修改\n')

text.grid()

upload = Button(root, width=10, height=1, text='上传', borderwidth=3,
                relief='ridge', compound='bottom', command=uploadFile)
upload.grid()

root.grid_columnconfigure(0, weight=1)

root.mainloop()
