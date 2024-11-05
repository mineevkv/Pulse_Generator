import sys
from socket import *
import qdarkstyle

from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRunnable, Qt

"""
Module for defining external functions to use in Qt-interface
"""

def set_text(label, text, color = 'red'):
    """Set label text: (obj, str, str)"""
    label.setText(text)
    label.setStyleSheet(f'color: {color}')


class ExampleApp(QtWidgets.QMainWindow):
    """" Ethernet communication (UDP protocol)"""
    ip = '192.168.127.111'
    port = 5000
    address = (ip, port)

    client_socket = None
    web_status = True  # show web interface
    status = True  # device is correct
    flag_pulse = False

    pulse_time = 0

    def __init__(self):
        super().__init__()
        uic.loadUi('window.ui', self)
        self.socket_init()

        self.btn_check.clicked.connect(self.btn_check_click)
        self.btn_set.clicked.connect(self.btn_set_click)
        self.btn_pulse.clicked.connect(self.btn_pulse_click)
        self.btn_web.clicked.connect(self.web_chagne)

        set_text(self.label_web_status, 'ON', 'green')
        set_text(self.btn_pulse, 'READY', 'yellow')
        self.label_ready_info.setText('')

        self.btn_check_click()


    def socket_init(self):
        self.client_socket = socket(AF_INET, SOCK_DGRAM)  # socket UDP setup
        self.client_socket.settimeout(2)  # only wait 2 second for a response

    def get_pulse_time(self):
        answer = self.send('t')
        if answer and answer[0:1] == 't':
            pulse_time = int(answer[2:])
            return pulse_time
        else:
            print('WARNING: device error')
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
                set_text(self.label_web_status, 'OFF', 'red')
            else:
                self.send('wf1')
                self.web_status = True
                set_text(self.label_web_status, 'ON', 'green')


    def send(self, message):
        self.client_socket.sendto(message.encode('utf-8'), self.address)
        try:
            rec_data, addr = self.client_socket.recvfrom(2048)
            return rec_data.decode()
        except timeout:
            return 0
        
    def btn_check_click(self):
        answer = self.send('c')
        if answer and answer[0:2] == 'ok':
            self.status = True
            set_text(self.label_connection, f'Connection to {self.ip}', 'green')
            self.pulse_time = self.get_pulse_time()
            self.edit_pulse_width.setText(f'{self.pulse_time}')
        else:
            self.status = False
            # print('WARNING: connection error')
            set_text(self.label_connection, 'Connection error', 'red')

    def btn_set_click(self):
        self.pulse_time = int(self.edit_pulse_width.text())
        answer = self.send(f's={self.pulse_time}')
        if answer and answer[0:2] == 'ok':
            self.status = True
            set_text(self.label_connection, f'Connection to {self.ip}', 'green')
            self.pulse_time = self.get_pulse_time()
            self.edit_pulse_width.setText(f'{self.pulse_time}')         
            set_text(self.btn_pulse, 'READY', 'yellow')
            self.label_ready_info.setText('Ok')
        else:
            self.status = False
            # print('WARNING: connection error')
            set_text(self.label_connection, 'Connection error', 'red')
    
    def btn_pulse_click(self):
        if self.flag_pulse:
            self.flag_pulse = False
            answer = self.send('p')
            if answer and answer[0:2] == 'ok':
                self.status = True
                set_text(self.label_connection, f'Connection to {self.ip}', 'green')
                self.pulse_time = self.get_pulse_time()
                self.edit_pulse_width.setText(f'{self.pulse_time}')
                
                set_text(self.btn_pulse, 'READY', 'yellow')
                self.label_ready_info.setText('Ok')
            else:
                self.status = False
                # print('WARNING: connection error')
                set_text(self.label_connection, 'Connection error', 'red')
        else:
            self.flag_pulse = True
            set_text(self.btn_pulse, 'PULSE', 'magenta')
            self.label_ready_info.setText('Gen is ready')


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp

    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))  # dark style

    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()