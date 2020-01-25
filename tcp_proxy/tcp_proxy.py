# -*- coding: utf-8 -*-

import sys
import socket
import threading

def server_loop(local_host,local_port,remote_host,remote_port,receive_first):
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    try:
        server.bind((local_host,local_port))
    except:
        print("filed to bind")
        sys.exit(0)
        
    server.listen(5)
    
    while True:
        client_socket,addr = server.accept()
        printf("addr[0]=%s,addr[1]=%d"%(addr[0],addr[1]))
        proxy_thread = threading.Thread(target=proxy_handler,args=(client_socket,remote_host,remote_port,receive_first))
        proxy_thread.start()
        
def main():
    if len(sys.argv[1:]) != 5:
        printf("Example:./tcp_proxy.py 127.0.0.1 9000 192.168.1.100 9000 True")
        
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    
    receive_first = sys.argv[5]
    if receive_first==True:
        receive_first = True
    else:
        receive_first = False
    
    server_loop(local_host,local_port,remote_host,remote_port,receive_first)
    
main()

def proxy_handler(client_socket,remote_host,remote_port,receive_first):
    remote_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    remote_socket = socket.connect((remote_host,remote_port))
    
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)
        
        remote_buffer = response_handler(remote_buffer)
        if len(remote_buffer):
            print("remote_buffer1 len=%d"%len(remote_buffer))
            client_socket.send(remote_buffer)
            
    while True:
        local_buffer = receive_from(client_socket)
        
        if len(local_buffer):
            print("local_buffer len=%d"%local_buffer)
            hexdump(local_buffer)
            
            request_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("send to remote")
            
        remote_buffer = receive_from(remote_socket)
        
        if len(remote_buffer):
            print("remote_buffer2 len=%d"%len(remote_buffer))
            hexdump(remote_buffer)
            
            remote_buffer = response_handler(remote_buffer)
            
            client_socket.send(remote_buffer)
            print("send to localhost")
            
        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("no more data")
            break
        
def hexdump(src,length=16):
    result = []
    digits = 4 if isinstance(src,unicode) else 2
    
    for i in xrang(0,len(src),length):
        s = src[i:i+length]
        hexa = b' '.join(["%0*X" % (digits,ord(x)) for x in s])
        text = b' '.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append(b"%04X %-*s %s" % (i,length*(digits+1),hexa,text))
        
    print b'\n'.join(result)
    
def receive_from(connection):
    buffer = ""
    connection.settimeout(2)
    
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except:
        pass
    
    return buffer

def request_handler(buffer):
    return buffer

def response_handler(buffer):
    return buffer            