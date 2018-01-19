import hashlib
from .reply import *
from .receive import *
from django.utils.encoding import smart_bytes
import random,re
from poem.models import poem
from django.db.models import Q

#作为匹配用，初始化可以使用正则表达式，然后用match匹配，会自动执行事先定义好的函数，匹配的字符串
#当作参数（但不能有“或者‘，否则会有语法问题）

class Handle(object):
    def __init__(self):
        self.r1 = re.compile('[ ,]') #可以用空格或者，分隔输入的参数
        #动作的字典，索引是关键字，内容是调用的函数
        
    def POST(self,request):
        try:
            #粉丝的信息用POST方式发送给自己服务器
            if request.method == 'POST':
                webData = smart_bytes(request.body) #此处是关键，获得http头信息，并转换为字符串（去unicode），参考自强学堂
                print("Handle Post webdata is %s"% webData)   #后台打日志
                recMsg = parse_xml(webData)
                #以下代码将收到的用户消息经过格式化处理之后，根据第一个关键字调用相应的处理程序（TOKEN字典）
                if isinstance(recMsg, RecMsg) and recMsg.MsgType == 'text':
                    toUser = recMsg.FromUserName
                    #print('toUser %s'%toUser)
                    fromUser = recMsg.ToUserName
                    content = recMsg.Content
                    content =content.decode('utf-8', 'ignore') #byte转unicode
                    content1 = self.r1.split(content)
                    content=[]
                    #将用户输入字符串转换为列表
                    for i in range(0,len(content1)):
                        if content1[i]!="":
                            content.append(content1[i])
                    if content[0] == "帮助":
                        rep_content='''使用规则: 
1.精确查询 输入题目或者题目加作者，中间用空格分开。例如:"登金陵凤凰台"，"游子吟 孟郊"
2.模糊查询，输入"题目"或"诗句"，然后输入题目或诗歌的一部分(连续的部分)，并用空格分开。例如:"题目 春"，"诗句 慈母"'''
                    else:
                        rep_content = self.Search_poem(content) #查询结果
                    replyMsg = TextMsg(toUser, fromUser, rep_content)
                    return replyMsg.send()
                else:
                    print("暂且不处理")
                    return "success"
        except Exception as e:
            print(e)
            return e                       

    def Search_poem(self,content):
        if content[0] == "题目": #模糊查询 根据题目
            obj_poem = poem.objects.filter(Q(title__icontains=content[1]))
            rep_content = "题目中含有\'"+str(content[1])+"\'的诗歌共有"+str(len(obj_poem))+"首"
        elif content[0]=="诗句":  #模糊查询 根据诗句    
            obj_poem = poem.objects.filter(Q(writer__icontains=content[1]))
            rep_content = "诗句中含有\'"+str(content[1])+"\'的诗歌共有"+str(len(obj_poem))+"首"
        elif len(content) == 1: #精确查询，只输入了一个参数
            obj_poem = poem.objects.filter(title=content[0])
            rep_content="题目为《"+str(content[0])+"》的诗歌共有"+str(len(obj_poem))+"首"
        else: #输入了标题和作者，后面的只考虑一个参数
            obj_poem = poem.objects.filter(Q(title=content[0])&Q(content=content[1]))
            rep_content="题目为《"+str(content[0])+"》，作者为\'"+str(content[1])+"\'的诗歌共有"+str(len(obj_poem))+"首"
        if len(obj_poem) != 0: #没找到诗句
            for  i in range(0,len(obj_poem)):
                rep_content = rep_content +"\n"  +obj_poem[i].title+ "\n" + obj_poem[i].content+ "\n" +obj_poem[i].writer+ "\n"
                if len(rep_content)>600: #超过微信最长限制，停止循环
                    rep_content = rep_content[0:600]+"..."
                    rep_content = rep_content +"\n\n" + "由于微信回复长度限制，无法显示全部内容，请缩小查找范围。输入\"帮助\"获取使用规则。"            
                    break;
        else:
            rep_content = "未能找到符合条件的古诗。输入\"帮助\"获取使用规则。"
        return rep_content






