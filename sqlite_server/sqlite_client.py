import sqlite3
import socket
import struct

while True:
    sql = input('输入一个要执行的SQL语句: \n')
    # 没有输入，进入下一次循环
    if sql.strip() == '':
        continue

    if sql in ('exit', 'quit'):
        break

    # 建立socket，尝试连接
    sockClient = socket.socket()
    try:
        sockClient.connect(('192.168.253.1', 5050))
    except:
        print('服务器异常，请检查')
    else:
        # 发送远程SQL语句
        sockClient.send(sql.encode('gbk'))
        size = sockClient.recv(4)
        size = struct.unpack('i', size)[0]

        data = b''
        while True:
            if size == 0:
                break
            elif size > 4096:
                # 注意断包和粘包
                # 虽然设置了4096，但是不一定能够接收4096字节
                # 即使缓冲区的数据远比4096
                t = sockClient.recv(4096)
                data += t
                size -= len(t)
            else:
                t = sockClient.recv(size)
                data += t
                size -= len(t)
            data = data.decode('gbk')
            try:
                data = eval(data)
            except:
                pass
            sockClient.close()
            print(data)
