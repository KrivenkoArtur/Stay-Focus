import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore

from design import Ui_Dialog

class Timer(QMainWindow):
    def __init__(self):
        super(Timer, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.thread_timer = QtCore.QThread()
        self.stop_watch = StopWatch()
        self.stop_watch.moveToThread(self.thread_timer)
        self.stop_watch.sec_commit.connect(self.change_sec)
        self.thread_timer.started.connect(self.stop_watch.run)

        self.ui.btn_pause.hide()
        self.ui.btn_reset.hide()

        self.ui.btn_play.clicked.connect(self.start_timer)
        self.ui.btn_pause.clicked.connect(self.pause_timer)
        self.ui.btn_reset.clicked.connect(self.reset_timer)

    def start_timer(self):
        self.stop_watch.running = True
        self.stop_watch.pause = False
        self.thread_timer.start()
        self.ui.btn_play.hide()
        self.ui.btn_pause.show()
        self.ui.btn_reset.hide()

    def pause_timer(self):
        self.ui.btn_pause.hide()
        self.ui.btn_play.show()
        self.ui.btn_reset.show()
        self.stop_watch.pause = True

    def reset_timer(self):
        self.stop_watch.running = False
        self.ui.label.setText('00:00:00')
        self.ui.btn_pause.hide()
        self.ui.btn_play.show()

    @QtCore.pyqtSlot(str)
    def change_sec(self, seconds):
        hours, minutes, seconds = self.calculate_time(seconds)
        self.ui.label.setText(f'{hours}:{minutes}:{seconds}')

    def calculate_time(self, seconds):
        hours = '00'
        minutes = '00'

        if int(seconds) > 3600:
            hours = int(seconds) - int(hours) * 3600
            if hours < 10:
                hours = f'0{hours}'

        if int(seconds) > 60:
            minutes = int(seconds) // 60
            seconds = int(seconds) - minutes * 60
            if minutes < 10:
                minutes = f'0{minutes}'

        if int(seconds) < 10:
            seconds = f'0{seconds}'

        return hours, minutes, seconds


class StopWatch(QtCore.QObject):
    running = True
    sec_commit = QtCore.pyqtSignal(str)
    pause = False

    def run(self):
        sec = 0
        while True:
            if not self.running:
                sec = 0
                continue
            if self.pause:
                continue
            QtCore.QThread.msleep(1000)
            sec += 1
            self.sec_commit.emit(str(sec))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Timer()
    window.show()
    sys.exit(app.exec())