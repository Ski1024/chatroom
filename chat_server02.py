"""
chatroom
"""
from socket import *
import os,sys
#服务器地址
ADDR = ("176.140.10.2",7777)

#存储用户信息
user = {}

#登录聊天室
def do_login(target,name,addr):
    global user
    if name in user or "管理员" in name:
        return target.sendto("该用户名已存在".encode(),addr)
    target.sendto(b"ok",addr)

    #通知其他人
    msg = "欢迎%s进入聊天室"%name
    for i in user:
        target.sendto(msg.encode(),user[i])
    #将用户信息插入字典
    user[name] = addr

def do_chat(target,name,text):
    msg = "%s : %s"%(name,text)
    for i in user:
        if i != name:
            target.sendto(msg.encode(),user[i])

def do_quit(target,name):
    global user
    msg = "%s 退出了聊天室"%name
    for i in user:
        if i != name:
            target.sendto(msg.encode(),user[i])
        else:
            target.sendto(b"exit",user[i])
    #从字典移除客户信息
    del user[name]


#处理请求
def do_request(target):
    while True:
        data,addr = target.recvfrom(1024)
        tmp = data.decode().split(" ")
        #根据请求类型执行不同内容
        if tmp[0] == "L":
            do_login(target,tmp[1],addr) #完成具体的登录工作
        elif tmp[0] =="C":
            text = " ".join(tmp[2:])#拼接消息内容
            do_chat(target,tmp[1],text)
        elif tmp[0] == "Q":
            if tmp[1] not in user:
                target.sendto(b"exit",addr)
                continue
            do_quit(target,tmp[1])
#搭建udp网络
def main():
    sockfd  = socket(AF_INET,SOCK_DGRAM)
    sockfd.bind(ADDR)

    pid = os.fork()
    if pid < 0 :
        return
    elif pid == 0:
       while True:
           msg = input("管理员消息:")
           msg = "C 管理员消息 " + msg
           sockfd.sendto(msg.encode(),ADDR)
    else:
        #请求处理函数
        do_request(sockfd)

if __name__ == "__main__":
        main()

