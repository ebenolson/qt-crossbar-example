import os
import sys
import asyncio

from qtpy.QtWidgets import QMainWindow, QDialog, QApplication, QPushButton, QWidget, QLineEdit, QGridLayout, QLabel, QFileDialog
from qtpy.QtGui import QImage, QPixmap
from qtpy.QtCore import Qt, QObject, QSettings
import qdarkstyle

from autobahn.asyncio.wamp import ApplicationRunner, ApplicationSession
from autobahn.wamp.types import PublishOptions
from autobahn.wamp.exception import TransportLost
from autobahn import wamp

from quamash import QEventLoop

from design import window as ui

class ControlWindow(ApplicationSession, QMainWindow, ui.Ui_MainWindow):
    def __init__(self, cfg=None):
        ApplicationSession.__init__(self, cfg)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowFlags(Qt.Window)
        self.progressBar.setProperty("value", 0)
        self.pushButton.clicked.connect(lambda: self.publish('com.prepbot.window.start'))

    async def onJoin(self, details):
        try:
            res = await self.subscribe(self)
            print("Subscribed to {0} procedure(s)".format(len(res)))
        except Exception as e:
            print("could not subscribe to procedure: {0}".format(e))
        self.show()

    @wamp.subscribe('com.prepbot.window.progress')
    def update_progress(self, n):
        self.progressBar.setProperty('value', n)
        self.repaint()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_from_environment())

    asyncio_loop = QEventLoop(app)
    asyncio.set_event_loop(asyncio_loop)

    runner = ApplicationRunner(url="ws://127.0.0.1:8080/ws", realm="realm1")
    runner.run(ControlWindow)
