#!/usr/bin/env python
#coding:utf-8
'''
本程序初始化数据库，注意会删除joke、jokekey所有的数据，请务必谨慎执行！！！
在执行前请确实表已经存在数据库中，配置见设置文件
'''
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wx.settings")

'''
Django 版本大于等于1.7的时候，需要加上下面两句
import django
django.setup()
否则会抛出错误 django.core.exceptions.AppRegistryNotReady: Models aren't loaded yet.
'''

import django
if django.VERSION >= (1, 7):#自动判断版本
    django.setup()




from poem.models import poem


def main_code():

    
    poem.objects.all().delete()
 
    fname = "poem.txt"
    try:
        file = open(fname,'r')
    except:
        print("not find poem.txt file")
    while True:
        title=file.readline() 
        if len(title)==0: # Zero length indicates EOF 
            break 
        writer=file.readline() 
        content=file.readline() 
        obj_poem = poem()
        obj_poem.title = title
        obj_poem.writer= writer
        obj_poem.content = content
        try:
            obj_poem.save()

        except Exception as e:
            print(e)
            print('save error in line %d'% i)
            break
    file.close()

if __name__ == "__main__":
    print(u'本程序将会删除数据库所有数据并创建元数据，如果继续请输入YES，如果中断执行请输入其它')
    #print(u'请先在admin先手工新建TEACHER组,目前没有什么功能')
    print('program will delete all data in db,if want continue press YES,or press aother key')
    #answer = input()
    answer = 'YES'
    if answer != 'YES':
        print(u'程序退出，没有修改数据库')
        print('program exit and not modify any data')   
    else:
        main_code()
        print(u'完成数据库初始化！')