#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QAction, qApp
from PyQt5.QtGui import QIcon


from slippymap.map import Map

TITLE = 'QT - CFPS Weather Map'
TILE_URL = "https://www.cfps.halc/static/tiles/base/{}/{}/{}.png"


class CFPS(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.map = Map(TILE_URL, 45.42, -75.69, 4, self)
        self._init_menu()
        self._init_window_icon()
        self._init_window_geom_and_title()
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

        nightAction = QAction('&Use Night Tiles', self)
        nightAction.triggered.connect(self._night_action_event)
        nightAction.triggered.connect(self.map.repaint)
        nightAction.setCheckable(True)
        nightAction.setChecked(False)

        siteAction = QAction('&Site Layer', self)
        siteAction.triggered.connect(self._site_action_event)
        siteAction.triggered.connect(self.map.repaint)
        siteAction.setCheckable(True)
        siteAction.setChecked(True)

        metarAction = QAction('&METAR Layer', self)
        metarAction.triggered.connect(self._metar_action_event)
        metarAction.triggered.connect(self.map.repaint)
        metarAction.setCheckable(True)
        metarAction.setChecked(True)

        refreshAction = QAction('&Refresh Layers', self)
        refreshAction.triggered.connect(self._refresh_action_event)
        refreshAction.triggered.connect(self.map.repaint)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        mapMenu = menubar.addMenu('&Map')
        mapMenu.addAction(nightAction)
        mapMenu.addAction(siteAction)
        mapMenu.addAction(metarAction)
        mapMenu.addAction(refreshAction)

    def _night_action_event(self, is_night):
        self.map.model.is_night = is_night

    def _site_action_event(self, is_enabled):
        self.map.get_layer('site').enabled = is_enabled

    def _metar_action_event(self, is_enabled):
        self.map.get_layer('metar').enabled = is_enabled

    def _refresh_action_event(self):
        self.map.fetch_layers()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CFPS()
    sys.exit(app.exec_())
