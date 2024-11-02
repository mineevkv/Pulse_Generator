import sys
from socket import *

from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRunnable, Qt


class ExampleApp(QtWidgets.QMainWindow):
    """" Ethernet communication (UDP protocol)"""
    ip = '192.168.127.111'
    port = 5000
    address = (ip, port)

    client_socket = None
    web_status = True  # show web interface
    status = True  # device is correct

    def __init__(self):
        super().__init__()
        uic.loadUi('window.ui', self)


    def socket_init(self):
        self.client_socket = socket(AF_INET, SOCK_DGRAM)  # socket UDP setup
        self.client_socket.settimeout(2)  # only wait 2 second for a response

    def get_pulse_time(self):
        answer = self.send('t')
        if answer and answer[0:1] == 't':
            pulse_time = int(answer[2:])
            return pulse_time
        else:
            print('WARNING: check device')
            return 0
        

    def check_device(self):
        self.client_socket.close()
        self.socket_init()
    # get_status()
        if not self.status:
            self.client_socket.close()


    def web_chagne(self):
        if self.status:
            if self.web_status:
                self.send('wf0')
                self.web_status = False
            else:
                self.send('wf1')
                self.web_status = True


    def send(self, message):
        self.client_socket.sendto(message.encode('utf-8'), self.address)
        try:
            rec_data, addr = self.client_socket.recvfrom(2048)
            return rec_data.decode()
        except timeout:
            return 0

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp

    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())   # dark style
    # app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))  # dark style

    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()