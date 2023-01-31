# GUI 채팅 클라이언트

from socket import *
import sys

import pymysql
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtGui
import threading

form_class = uic.loadUiType("chat1.ui")[0]

class WindowClass(QMainWindow, form_class):
    HOST = '10.10.21.110'
    PORT = 3306
    USER = 'Team8'
    PASSWORD = 'xlavmfhwprxm8'
    DB = 't8_db'

    user = None # (이름, 번호, 비밀번호) 튜플

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.move(100,300)
        self.initialize_socket()

        self.send_btn.clicked.connect(self.send_chat) #ui메시지전송버튼
        self.stackedWidget.setCurrentIndex(0) #스택위젯 0p 고정
        self.acount_tabWidget.setCurrentIndex(0) # 로그인/가입 탭위젯 0

        self.chat_open_btn.clicked.connect(self.chat_open) # 로그인
        # self.join_btn.clicked.connect(self.create_acount) # 회원가입

        self.chat_add_btn.clicked.connect(self.create_chatroom) #채팅방 생성 버튼

        # lineEdit 입력 제한
        phone_re = QtCore.QRegExp("[0-9]{10,11}") # 휴대폰 번호
        self.phone_lineEdit.setValidator(QtGui.QRegExpValidator(phone_re))
        self.user_phone_lineEdit.setValidator(QtGui.QRegExpValidator(phone_re))

        pw_re = QtCore.QRegExp("[a-zA-Z0-9]{5,24}") # 비밀번호
        self.user_pass_lineEdit.setValidator(QtGui.QRegExpValidator(pw_re))
        self.pass_lineEdit.setValidator(QtGui.QRegExpValidator(pw_re))


    def chat_open(self): # 1p 들어가기 버튼 클릭했을때 : 로그인
        print('button click')
        phone = self.user_phone_lineEdit.text()
        password = self.user_pass_lineEdit.text()

        if phone == '' or password == '':
            self.login_label.setText('휴대폰 번호와 비밀번호를 입력해주세요.')
            return # 왜 return을 하였을까? 궁금하다

        with self.conn_fetch() as cur:
            sql = f"SELECT user_name, user_phone, user_pass FROM users WHERE user_phone = '{phone}';"
            cur.execute(sql)
            acount = cur.fetchone()

            if acount: # 핸드폰 번호 조회 결과가 존재한다면
                name, id, pw = acount

                if password == pw: # 비밀번호가 일치할 때
                    print('phone / pass 일치, 로그인 확인')
                    # self.user_name_label_2p.setText(self.user_name_line_edit_1p.text())
                    self.user = acount
                    self.stackedWidget.setCurrentIndex(1) # 페이지 이동
                    print('페이지이동')
                    self.user_name_label_2p.setText(name)
                    print('이름출력')
                    self.list_up_room()  # 채팅방 목록 조회
                    print('채팅방 목록 조회')

                    # 로그인 경고, 비밀번호 입력란 초기화
                    self.login_label.setText('')
                    self.user_pass_lineEdit.setText('')
                else:
                    print('phone / pass 불일치')
                    self.login_label.setText('비밀번호를 확인해주세요.')
            else:
                print('조회된 계정 없음')
                self.login_label.setText('존재하지 않는 계정입니다.')
                return

    def create_acount(self):
        print('회원가입')
        new_user = (self.name_lineEdit.text(), self.phone_lineEdit.text(), self.pass_lineEdit.text())
        if '' not in new_user:
            print('가입 시도: ', new_user[0])
            with self.conn_fetch() as cur:
                sql = f"SELECT user_phone FROM users WHERE user_phone = '{new_user[1]}'"
                cur.execute(sql)
                acount = cur.fetchone()

            if acount: # 휴대폰 번호가 이미 존재한다면
                print('이미 존재하는 계정')
                self.join_label.setText('이미 사용중인 휴대폰 번호입니다.')
            else: # 휴대폰 번호가 존재하지 않는다면
                msg = f'이름: {new_user[0]}\n휴대폰 번호: {new_user[1]}\n비밀번호: {new_user[2]}\n가입하시겠습니까?'
                reply = QMessageBox.question(self, '회원가입', msg,
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

                if reply == QMessageBox.Yes:
                    print('가입 완료')
                    with self.conn_commit() as con:
                        with con.cursor() as cur:
                            sql = 'INSERT INTO users(user_name, user_phone, user_pass)' \
                                  'VALUES (%s, %s, %s)'
                            cur.execute(sql, new_user)
                            con.commit()

                    QMessageBox.information(self, '완료', '가입이 완료되었습니다.')
                    print('가입 완료')

                    # 회원가입 입력칸 초기화
                    self.name_lineEdit.setText('')
                    self.phone_lineEdit.setText('')
                    self.pass_lineEdit.setText('')
                    self.join_label.setText('')
                    self.acount_tabWidget.setCurrentIndex(0)

        else:
            print('빈 칸 존재')
            self.join_label.setText('모든 항목을 입력해주세요.')
            return

    def initialize_socket(self):
        ip = '10.10.21.122'
        port = 10000
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect((ip, port))

    def send_chat(self):
        # senders_name = self.user_name_line_edit_1p.text() #ui사용자이름
        senders_name = self.user[0] # 윗줄의 코드를 수정
        data = self.signal_textEdit.toPlainText() #
        self.receive_listWidget.addItem(f'{senders_name} : {data}') #ui
        message = (f'{senders_name} : {data}').encode('utf-8')
        self.client_socket.send(message)
        self.signal_textEdit.clear()

    def receive_message(self, so):
        while True:
            buf = so.recv(256)
            if not buf: # 연결종료
                break
            recv_data=buf.decode()
            print(recv_data)
            #raw_data = ['★']
            #if raw_data == '★':
                #raw_data = self.client_socket.recv(buf.decoding())
                #self.data = eval(raw_data)
                # data = 보내기의 raw_data의 자료와 자료형
            self.receive_listWidget.addItem(f'{recv_data}')
        so.close()

    def create_chatroom(self):
        text = self.chat_name_line_edit.text()
        print(f'방제목: {text}')
        if text == '':
            return QMessageBox.information(self, '채팅 생성', '방 제목을 입력해주세요.')

        reply = QMessageBox.question(self, '채팅 생성', f"방장:'{self.user[0]}'\n'{text}' 채팅방을 생성하시겠습니까?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            print(f'채팅방 [{text}] -- 생성 시도')
            with self.conn_commit() as con:
                with con.cursor() as cur:
                    sql = 'INSERT INTO t8_db.room (room_name, room_master) VALUES (%s, %s)' # 채팅방 생성 쿼리
                    cur.execute(sql, (text, self.user[1]))
                    con.commit()
            a = [text] # 서버 eval()을 위한 변수
            total_info = str(a).encode('utf-8') # 서버 eval()을 위한 변수
            self.client_socket.send(total_info) # 서버 eval()을 위한 함수
            QMessageBox.information(self, '완료', '채팅방이 생성되었습니다.')
            print('채팅방 생성')
            self.list_up_room()  # 채팅 목록 조회

    def list_up_room(self): # 채팅 목록 조회
        with self.conn_fetch() as cur:  # with가 뜻하는게 뭘까?
                sql = 'SELECT * FROM t8_db.room;'  # 채팅방 조회 쿼리
                cur.execute(sql)
                rows = cur.fetchall() # 방 목록

        # 테이블 행 / 열 설정
        self.chat_list_tableWidget.setColumnCount(2)
        self.chat_list_tableWidget.setRowCount(len(rows))

        col = 0
        for row in rows:
            self.chat_list_tableWidget.setItem(col, 0, QTableWidgetItem(str(row[0])))
            self.chat_list_tableWidget.setItem(col, 1, QTableWidgetItem(str(row[1])))
            col += 1

        # 테이블 헤더 조정
        self.chat_list_tableWidget.setColumnWidth(0, 20)
        self.chat_list_tableWidget.horizontalHeader().setStretchLastSection(True)

        # 테이블 셀 클릭 이벤트
        self.chat_list_tableWidget.cellClicked.connect(self.select_chatroom)
        # 이제 더블클릭 했을 때 채팅방 새 창으로 열기 만들면 됨


    def select_chatroom(self, row):
        r_num = self.chat_list_tableWidget.item(row, 0) # 방 번호
        r_name = self.chat_list_tableWidget.item(row, 1) # 방 이름

        room = (int(r_num.text()), r_name.text())
        print(f'@{room[0]}번 : {room[1]}')

    def conn_fetch(self):
        con = pymysql.connect(host=self.HOST, user=self.USER, password=self.PASSWORD, db=self.DB, charset='utf8')
        cur = con.cursor()
        return cur

    def conn_commit(self):
        con = pymysql.connect(host=self.HOST, user=self.USER, password=self.PASSWORD, db=self.DB, charset='utf8')
        return con

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    cThread = threading.Thread(target=myWindow.receive_message, args=(myWindow.client_socket,), daemon=True)
    cThread.start()
    app.exec_()