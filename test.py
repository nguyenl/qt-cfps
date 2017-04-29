#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QToolTip, QPushButton, QMessageBox, QDesktopWidget, QAction, qApp
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QCoreApplication


TITLE = 'QT - CFPS Weather Map'


class CFPS(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
        
    def initUI(self):
        self._init_menu()
        self._init_toolbar()
        QToolTip.setFont(QFont('SansSerif', 10))
        
        self.setToolTip('This is a <b>QWidget</b> widget')
        
        btn = QPushButton('Quit', self)
        btn.clicked.connect(QCoreApplication.instance().quit)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(100, 150)       

        self.statusBar().showMessage('Ready')
        
        self.resize(500, 500)
        self.center()
        self.setWindowTitle(TITLE)
        self.setWindowIcon(QIcon('icon.png'))        
        self.show()

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

        
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):
        
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CFPS()
    sys.exit(app.exec_())  
