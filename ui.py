# GUI 채팅 클라이언트

from socket import *
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import threading

form_class = uic.loadUiType("chat.ui")[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.initialize_socket()
        self.send_btn.clicked.connect(self.send_chat) #ui메시지전송버튼

    def initialize_socket(self):
        ip = input('server IP addr: ')
        if ip == '':
            ip = '10.10.21.122'
        port = 19110
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect((ip, port))

    def send_chat(self):
        senders_name = self.user_name_line_edit.text() #ui사용자이름
        print(1)
        data = self.signal_textEdit.toPlainText() #
        print(2)
        self.receive_textBrowser.append(f'{senders_name} : {data}') #ui
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
            self.receive_textBrowser.append(f'{recv_data}')
        so.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    cThread = threading.Thread(target=myWindow.receive_message, args=(myWindow.client_socket,))
    cThread.start()
    app.exec_()
