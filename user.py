from socket import*
from tkinter import*
import threading
import operator as op
import time


# 发送按钮，使用套接字向服务器发送消息
def send(data, tcpCliSock):
    if not data:
        return
    data = data.encode('utf-8')
    tcpCliSock.send(data)


# 使用套接字从服务器接收消息
def recv(tcpCliSock):
    # 当套接字未释放时
    while tcpCliSock.fileno() != -1:
        data = tcpCliSock.recv(BUFSIZ)
        data = data.decode('utf-8')
        if op.eq(data,''):
            continue
        
        # 打印消息
        print(data)

        # 收到断开信息
        if op.eq(data,'close'):
            break


# 关闭按钮
def close(root,tcpCliSock):
    data = 'close'
    data = data.encode('utf-8')
    tcpCliSock.send(data)
    root.destroy()


# 界面
def win():
     root = Tk()
     root.title('输入框')
     root.geometry('240x160')
     inp = Entry(root)
     inp.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.3)
     btsend = Button(root,text='发送', command = lambda: send(inp.get(),tcpCliSock))
     btsend.place(relx = 0.2, rely = 0.6)
     btclose = Button(root,text='关闭', command = lambda: close(root,tcpCliSock))
     btclose.place(relx = 0.7, rely = 0.6)
     root.mainloop()


HOST = '127.0.0.1' # 服务器的IP
PORT = 8880        # 服务器的端口号
BUFSIZ = 1024
ADDR = (HOST, PORT)

# 面向网络的，TCP
tcpCliSock = socket(AF_INET,SOCK_STREAM)
# 连接
tcpCliSock.connect(ADDR)
# 启动线程用于接收消息
myThread = threading.Thread(target=recv, args=(tcpCliSock,))
myThread.setDaemon(True) # 主线程结束则终止子线程
myThread.start()
win()

time.sleep(2)
tcpCliSock.close()
