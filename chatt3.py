# GUI 채팅 클라이언트

from socket import *
import sys

import pymysql
from PyQt5.QtWidgets import *
from PyQt5 import uic
import threading

form_class = uic.loadUiType("chat11.ui")[0]

class WindowClass(QMainWindow, form_class):
    HOST = '10.10.21.110'
    PORT = 3306
    USER = 'Team8'
    PASSWORD = 'xlavmfhwprxm8'
    DB = 't8_db'

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.move(600, 100)
        self.initialize_socket()

        self.send_btn.clicked.connect(self.send_chat) #ui메시지전송버튼
        self.stackedWidget.setCurrentIndex(1) #스택위젯 0p 고정  ####################
        self.chat_open_btn.clicked.connect(self.reply)

        self.chat_add_btn.clicked.connect(self.reply) #채팅방 생성버튼

    # def create_chatroom(self):
    #     QMessageBox.information(self, '채팅 생성', '방 제목을 입력해주세요.')

    def reply(self):
        reply = QMessageBox.question(self, '채팅 생성', f"'{self.chat_name_line_edit.text()}' 채팅방을 생성하시겠습니까?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            print(5)
            print(f'채팅방 [{self.chat_name_line_edit.text()}] -- 생성시도')
            with self.conn_commit() as con:
                with con.cursor() as cur:
                    sql = 'INSERT INTO t8_db.room (room_name) VALUES(%s)' # 채팅방 생성쿼리
                    cur.execute(sql,(self.chat_name_line_edit.text()))
                    con.commit()
                    QMessageBox.information(self, '완료', '채팅방이 생성되었습니다.')
                    print('채팅방 생성')
            self.list_up_room() #채팅목록 조회


    def list_up_room(self): #채팅목록 조회
        with self.conn.fetch() as cur:
            sql = 'SELECT * FROM t8_db.room' #채팅방 조회 쿼리
            cur.execute(sql)
            rows = cur.fetchall() # 방목록

        # 테이블 행 / 열 설정
        self.chat_list_tableWidget.setColumnCount(2) #이거궁금
        self.chat_list_tableWidget.setRowCount(len(rows)) #?

        col = 0
        for row in rows:
            self.chat_list_tableWidget.setItem(col, 0, QTableWidgetItem(str(row[0])))  #QTableWidgetItem 쳐보기
            self.chat_list_tableWidget.setItem(col, 1, QTableWidgetItem(str(row[1])))
            col += 1

        # 테이블 헤더 조정
        self.chat_list_tableWidget.setColumnWidth(0, 20)
        self.chat_list_tableWidget.horizontalHeader().setStretchl_astSection(True)

    def conn_fetch(self):
        con = pymysql.connect(host=self.HOST, user=self.USER, password=self.PASSWORD, db=self.DB, charset='utf-8')
        cur = con.cursor()
        return cur

    def conn_commit(self):
        con = pymysql.connect(host=self.HOST, user=self.USER, password=self.PASSWORD, db=self.DB, charset='utf-8')
        return con

    def chat_open(self): # 1p 들어가기 버튼 클릭했을때
        print('button click')
        self.user_name_label_2p.setText(self.user_name_line_edit_1p.text())
        self.stackedWidget.setCurrentIndex(1)

    def initialize_socket(self):
        ip = '10.10.21.122'
        port = 9000
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
            self.receive_listWidget.append(f'{recv_data}')
        so.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    cThread = threading.Thread(target=myWindow.receive_message, args=(myWindow.client_socket,))
    cThread.start()
    app.exec_()
