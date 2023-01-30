# TCP_receivefile.py
# 파일 수신 프로그램

import socket

s_sock = socket.socket()
host = "localhost"
port = 2500

s_sock.connect((host, port)) # 서버와연결
s_sock.send("I am ready".encode()) # 준비완료 메시지 송신
fn = s_sock.recv(1024).decode()

with open('e:/'+fn, 'wb') as f: #저장파일 열기
    print('file opened')
    print('receiving file...')
    while True:
        data = s_sock.recv(8192) #파일내용 수신
        if not data: # 내용이 없으면 종료
            break
        f.write(data) # 내용을 파일에쓰기

print('Download complete')
s_sock.close()
print('Connection closed')