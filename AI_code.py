import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QTextBrowser, QTextEdit, QAction, QVBoxLayout, \
    QHBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QKeySequence


class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.listwidget = QListWidget(self)
        self.listwidget.insertItem(0, "Room 1")
        self.listwidget.insertItem(1, "Room 2")
        self.listwidget.insertItem(2, "Room 3")
        self.listwidget.itemClicked.connect(self.setCurrentRoom)

        self.textbrowser = QTextBrowser(self)

        self.textedit = QTextEdit(self)
        send_message_action = QAction("Send", self)
        send_message_action.setShortcut(QKeySequence.InsertParagraphSeparator)
        send_message_action.triggered.connect(self.sendMessage)
        self.addAction(send_message_action)

        hbox = QHBoxLayout()
        hbox.addWidget(self.listwidget)
        hbox.addWidget(self.textbrowser)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.textedit)

        central_widget = QWidget(self)
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)

        self.setWindowTitle('Chat')
        self.setGeometry(500, 300, 600, 400)
        self.show()

    def setCurrentRoom(self, item):
        self.current_room = item.text()
        self.textbrowser.clear()

    def sendMessage(self):
        message = self.textedit.toPlainText()
        self.textbrowser.append("[{}]: {}".format(self.current_room, message))
        self.textedit.clear()


app = QApplication(sys.argv)
chat_window = ChatWindow()
sys.exit(app.exec_())
