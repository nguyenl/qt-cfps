#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QToolTip, QPushButton, QMessageBox, QDesktopWidget, QAction, qApp, QVBoxLayout
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QCoreApplication

from slippymap.map import Map

TITLE = 'QT - CFPS Weather Map'
TILE_URL = "https://www.cfps.halc/static/tiles/base/{}/{}/{}.png"


class CFPS(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self._init_menu()
        self._init_window_icon()
        self._init_window_geom_and_title()
        self.map = Map(TILE_URL, 45.42, -75.69, 4, self)
        self.setCentralWidget(self.map)
        self.show()

    def _init_window_geom_and_title(self):
        self.resize(1000, 1000)
        self.center()
        self.setWindowTitle(TITLE)

    def _init_window_icon(self):
        self.setWindowIcon(QIcon('icon.png'))

    def _init_toolbar(self):
        exitAction = QAction(QIcon('application_exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(qApp.quit)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)

    def _init_menu(self):
        exitAction = QAction(QIcon('application_exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CFPS()
    sys.exit(app.exec_())
