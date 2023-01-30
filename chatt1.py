# GUI 채팅 클라이언트

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
        self.move(600,100)
        self.initialize_socket()
        self.send_btn.clicked.connect(self.send_chat) #ui메시지전송버튼
        self.stackedWidget.setCurrentIndex(0) #스택위젯 0p 고정
        self.chat_open_btn.clicked.connect(self.chat_open)

    def chat_open(self): # 1p 들어가기 버튼 클릭했을때
        print('button click')
        self.user_name_label_2p.setText(self.user_name_line_edit_1p.text())
        self.stackedWidget.setCurrentIndex(1)

    def initialize_socket(self):
        ip = '10.10.21.122'
        port = 2700
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
