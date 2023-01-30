# 예외처리를 한 TCP 클라이언트 프로그램
# 실행할 때 서버주소와 포트를 지정한다.
# 지정하지 않으면 '127.0.0.1'과 2500 사용

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버주소 입력
svrIP = input(("Server IP(default: 127.0.0.1): "))
if svrIP == '':
    svrIP = '127.0.0.1' #기본주소

# 포트번호 입력
port = input('port(default: 2500): ')
if port == '':
    port = 2500 # 기본포트
else:
    port = int(port)

sock.connect((svrIP, port))
print('Connected to' + svrIP)

while True:
    msg = input("Sending message: ")

    # 송신데이터가 없으면 다시진행
    if not msg:
        continue

    try: # 데이터전송
        sock.send(msg.encode()) # 메시지전송

    except: # 연결종료
        print("연결이 종료되었습니다.")
        break

    try: # 데이터읽기
        msg = sock.recv(1024)
        if not msg:
            print("연결이 종료되었습니다.")
            break
        print(f'Received message: {msg.decode()}')

    except: # 연결종료
        print("연결이 종료되었습니다.")
        break

sock.close()