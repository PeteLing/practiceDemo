import socket
from threading import Thread
import struct

sockServer = socket.socket()
sockServer.bind(('', 5050))
sockServer.listen(50)


def agent(conn):
    # 接收客户端发来的指令，并进行过滤
    sql = conn.recv(1024)
    if not sql.decode('gbk').startswith(('select', 'delete', 'insert', 'update')):
        message = b'not a sql statement'
        conn.send(struct.pack('i', len(message)))
        conn.send(message)
        return
    else:
        sockClient = socket.socket()
        # 尝试连接服务器
        try:
            sockClient.connect(('192.168.253.1', 3030))
        except:
            message = b'Server not alive'
            conn.send(struct.pack('i', len(message)))
            conn.send(message)
            return
        # 向服务器转发SQL语句
        sockClient.send(sql)
        # 数据量大小，使用struct序列化一个整数需要4个字节
        size = sockClient.recv(4)
        conn.send(size)
        size = struct.unpack('i', size)[0]
        while True:
            if size == 0:
                break
            elif size > 4096:
                data = sockClient.recv(4096)
                conn.send(data)
                size -= len(data)
            else:
                data = sockClient.recv(size)
                conn.send(data)
                size -= len(data)
            sockClient.close()
        conn.close()


while True:
    conn, _ = sockServer.accept()
    Thread(target=agent, args=(conn,)).start()
