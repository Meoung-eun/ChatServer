# TCP_sendfile.py
# 파일전송 프로그램

import socket
import sys

port = 2500
s_sock = socket.socket()
host = ""
s_sock.bind((host, port))
s_sock.listen(1)

print('Waiting for connection....')

c_sock, addr = s_sock.accept() # 클라이언트와 연결
print('Connected from', addr)
msg = c_sock.recv(1024) #클라이언트로부터 준비완료 수신
print(msg.decode())
filename = input('File name to send(c:/test/sample.bin): ') # '\'대신 '/'사용하여 경로구분
print(f"Sending '{filename}'")
fn = filename.split('/') # 파일경로 중 파일이름만 추출

c_sock.sendall(fn[-1].encode()) #파일이름 전송

with open(filename, 'rb') as f:
    c_sock.sendfile(f, 0) #파일내용 전송

    #data = f.read()
    #while data:
    #   c_sock.sendall(data)
    #   data = f.read()

print('Sending complete')
c_sock.close()