# -*- coding: UTF-8 -*- 

# Author:LC
#使用xlrd库解析xls文件，得到每个格子的数据。

import xlrd
import os
import os.path
import time
import multiprocessing
# 让py可以读取文件中的中文
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


#遍历文件夹下面所有的xls文件
def dirlist(path, allfile):  
    filelist =  os.listdir(path)  
    for filename in filelist:  
        filepath = os.path.join(path, filename)
        if os.path.isdir(filepath):  
            dirlist(filepath, allfile)  
        else:
            if -1 != filepath.find(".xls"):
                allfile.append(filepath)
    return allfile  


#创建一个保存的文件夹，不存在则重新创建
outputDir = 'xmlConfig'
if not os.path.exists(os.path.join(os.getcwd(), outputDir)):
    os.makedirs(os.path.join(os.getcwd().decode('GBK'), outputDir))
    
  
def print_lua(xlsname): 
    workbook = xlrd.open_workbook(xlsname)
    #获取每一个sheet中的行列数据
    for booksheet in workbook.sheets(): 
        # 可以在这里写一些固定的注释代码之类的
        writeData = '<?xml version="1.0" encoding="UTF-8"?>\n'
        
        for cols in xrange(booksheet.ncols):
            writeData = writeData + '<!-- ' + booksheet.cell(0, cols).value + ' = ' + booksheet.cell(1, cols).value
            writeData = writeData + '-->\n'
            
        outputName = booksheet.name +'_config' 
        # print os.path.join(os.getcwd().decode('GBK'), outputDir) + '\\' + outputName
        fileOutput = open(os.path.join(os.getcwd().decode('GBK'), outputDir) + '\\' + outputName + '.xml','w')
        fileOutput.write(writeData)
        #生成配置名
        writeData ='<'+ outputName + '>\n'
        fileOutput.write(writeData)
        writeData = ''
        onlyOne = (booksheet.nrows == 4)
        for row in xrange(booksheet.nrows):
            #print 'booksheet.nrows ================='+booksheet.nrows
            if row > 2: #第三行开始写入数据
                writeData = '    <'+booksheet.name+' ' #写到lua里面每一行都是一个table
                #写入每一列的数据
                for col in xrange(booksheet.ncols):
                    writeData = writeData + booksheet.cell(1, col).value + ' = ' #写入key,key是固定的位置，每一行都会有
                    value = booksheet.cell(row, col).value
                    if booksheet.cell(row, col).ctype == 0:
                        writeData = writeData + '""'
                    elif booksheet.cell(row, col).ctype == 1:
                        writeData = writeData + '"' + value + '"'
                    elif booksheet.cell(row, col).ctype == 2:
                        #判断单元格的内容是不是float类型（int(value) != value 代表是有小数的）
                        if type(value) == float and int(value) != value:
                            writeData = writeData + '"' + str(float(value)) + '"' #写入float value
                        else:
                            writeData = writeData + '"' + str(int(value)) + '"' #写入int value
                    #最后一行不加逗号
                    if col < booksheet.ncols - 1:
                        if onlyOne :
                            writeData = writeData + '\n            '
                        else :
                            writeData = writeData + ' '
                    else:
                        writeData = writeData + '/>\n'

                fileOutput.write(writeData)        
            else:
                #writeData = '}\n\n'
                fileOutput.write(writeData)

        writeData = '</' + outputName + '>\n'
        fileOutput.write(writeData)
        fileOutput.close()


#遍历所有的xls文件
if __name__ == "__main__":
    print 'main'
    #开始时间
    startTime = time.clock()
    
    #记录所有.xls文件路径
    allXlsfile = []
    #遍历当前工作目录
    dirlist(os.getcwd(), allXlsfile)
    pool = multiprocessing.Pool(processes=10)

    for xlsname in allXlsfile:
        pool.apply_async(print_lua, (xlsname,))
    pool.close() # 关闭进程池，表示不能在往进程池中添加进程
    pool.join() # 等待进程池中的所有进程执行完毕，必须在close()之后调用
    

    #结束时间
    endTime = time.clock()   
    print('Running time: %s Seconds'%(endTime-startTime))

    

    