# GUI 채팅 클라이언트

import pymysql
from socket import *
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import threading

form_class = uic.loadUiType("chat1.ui")[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.move(100,100) # 창의 위치를 띄워주는
        self.initialize_socket()
        self.send_btn.clicked.connect(self.send_chat) #ui메시지전송버튼
        self.stackedWidget.setCurrentIndex(0) #스택위젯 0p 고정
        self.chat_open_btn.clicked.connect(self.chat_open)

    def DB(self):
        self.checkboxList = []  # 체크박스 넣을 빈 리스트 만들기
        ## sql파일 커넥트
        conn = pymysql.connect(host='10.10.21.110', user='root', password='xlavmfhwprxm8', db='room',
                               charset='utf8')
        cur = conn.cursor()
        ## conn로부터  결과를 얻어올 때 사용할 Cursor 생성
        cur = conn.cursor()
        ## SQL문 실행
        sql = "select COLUMN_NAME from INFORMATION_SCHEMA COLUMNS WHERE TABLEt8_db.chat"
        cur.execute(sql)
        print(cur.execute(sql))  # 실행(excute) 했더니 10884줄이 나온다.
        rows = cur.fetchall()


    def chat_open(self): # 1p 들어가기 버튼 클릭했을때
        print('button click')
        self.user_name_label_2p.setText(self.user_name_line_edit_1p.text())
        self.stackedWidget.setCurrentIndex(1)

    def initialize_socket(self):
        ip = '10.10.21.122'
        port = 3000
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect((ip, port))

    def send_chat(self):
        senders_name = self.user_name_line_edit_1p.text() #ui사용자이름
        print(1)
        data = self.signal_textEdit.toPlainText() #
        print(2)
        self.receive_listWidget.addItem(f'{senders_name} : {data}') #ui
        print(3)
        message = (f'{senders_name} : {data}').encode('utf-8')
        print(4)
        self.client_socket.send(message)
        print(5)
        self.signal_textEdit.clear()
        print(6)

    def receive_message(self, so):
        while True:
            buf = so.recv(256)
            if not buf: # 연결종료
                break
            recv_data=buf.decode()
            print(recv_data)
            self.receive_listWidget.addItem(f'{recv_data}')
        so.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    cThread = threading.Thread(target=myWindow.receive_message, args=(myWindow.client_socket,))
    cThread.start()
    app.exec_()
