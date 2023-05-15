from socket import*
from time import ctime
from operator import eq
import threading


def recv(tcpCliSock, addr, i):
    while True:
        # 从客户端接收消息
        data = tcpCliSock.recv(BUFSIZ)
        data = data.decode('utf-8')
        # 收到断开信息
        if eq(data,'close'):
            tcpCliSock.send(data.encode('utf-8'))
            tcpCliSock.close() # 释放套接字
            print('...connect break:',addr)
            break
        if eq(data,''):
            continue
        # 打印收到的消息
        data = '[%s][%s] %s' % (ctime(), addr, data)
        message.append(data)
        print(data)


def send(tcpCliSock):
    n = len(message)
    # 当套接字未释放时
    while tcpCliSock.fileno() != -1:
        n1 = len(message)
        i = n
        # 将消息队列中更新的消息发到客户端，实现多个客户端相互聊天
        while i < n1:
            data = message[i]
            i += 1
            tcpCliSock.send(data.encode('utf-8'))
        n = n1


HOST = ''      # 默认本机
PORT = 8880    # 端口号
BUFSIZ = 1024
ADDR = (HOST, PORT)

# 线程池
thread1 = []
thread2 = []

# 消息队列
message = []
i = 0

# 面向网络的，TCP
tcpSerSock = socket(AF_INET, SOCK_STREAM)
# 服务端用于将把用于通信的地址和端口绑定到 socket 上
tcpSerSock.bind(ADDR)
# 开启监听
tcpSerSock.listen(5)

while True:
    print('waiting for connection...')
    # 等待连接，主线程阻塞
    tcpCliSock, addr = tcpSerSock.accept()  # 用户套接字和IP
    print('...connected from:', addr)

    # 向连接成功的用户发送成功讯号 
    data = 'sucess'
    tcpCliSock.send(data.encode('utf-8'))  

    # 子线程实现服务器和客户端的通信
    thread1.append(threading.Thread(target=recv, args=(tcpCliSock, addr, i)))
    thread2.append(threading.Thread(target=send, args=(tcpCliSock,)))
    thread1[i].start()
    thread2[i].start()
    i+=1

tcpSerSock.close()


    
