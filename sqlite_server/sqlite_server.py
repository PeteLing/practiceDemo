import sqlite3
import socket
import struct


def getData(sql):
    '''通过给定的SQL SELECT语句返回结果'''
    with sqlite3.connect(r'test.db') as conn:
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
    return result


def doSql(sql):
    '''适用于DELETE/UPDATE/INSERT INTO'''
    with sqlite3.connect(r'test.db') as conn:
        cur = conn.cursor()
        result = cur.execute(sql)
    return result.rowcount


sockServer = socket.socket()
sockServer.bind(('', 3030))
sockServer.listen(1)

while True:
    # 接受客户端连接
    try:
        conn, addr = sockServer.accept()
    except:
        continue
    sql = conn.recv(1024).decode('gbk').lower()

    if sql.startswith(('update', 'delete', 'insert', 'create')):
        try:
            # 首先发送要发送的字节总数量
            # 然后再发送真实数据
            result = str(doSql(sql)).encode('gbk')
            conn.send(struct.pack('i', len(result)))
            conn.send(result)
        except:
            message = b'error'
            conn.send(struct.pack('i', len(message)))
            conn.send(message)

    elif sql.startswith('select'):
        try:
            result = str(getData(sql)).encode('gbk')
            conn.send(struct.pack('i', len(result)))
            conn.send(result)
        except:
            message = b'error'
            conn.send(struct.pack('i', len(message)))
            conn.send(message)
