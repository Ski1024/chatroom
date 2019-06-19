"""
chatroom 客户端
"""
from socket import *
import os,sys
#服务端地址
ADDR = ("176.140.10.2",7777)

#发消息
def send_msg(s,name):
    while True:
        try:
            text = input("发言:")
        except KeyboardInterrupt:
            text = "quit"
        if text.strip() == "quit":
            msg = "Q" + name
            s.sendto(msg.encode(),ADDR)
            sys.exit("退出聊天室")
        msg = "C %s %s"%(name,text)
        s.sendto(msg.encode(),ADDR)

#接收消息
def recv_msg(s):
    while True:
        try:
            data,addr = s.recvfrom(4096)
        except KeyboardInterrupt:
            sys.exit()
        #服务器发送"exit"退出
        if data.decode() == "exit":
            sys.exit()
        print(data.decode())

#启动客户端
def main():
    s = socket(AF_INET,SOCK_DGRAM)
    # sockfd.sendto("我要登录".encode(),ADDR)
    while True:
        name = input("请输入姓名:")
        msg = "L " + name
        s.sendto(msg.encode(),ADDR)
        #等待反馈
        data,addr = s.recvfrom(1024)
        if data.decode() == "ok":
            print("您已进入聊天室")
            break
        else:
            print(data.decode())

        #创建新进程
    #创建新进程
    pid = os.fork()
    if pid < 0:
        sys.exit("error!")
    elif pid == 0:
        send_msg(s,name)
    else:
        recv_msg(s)
if __name__ == "__main__":
        main()