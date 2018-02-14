#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QMainWindow, QFileDialog, QGraphicsScene, QMessageBox

from lib.vue import CorrectionWindow, MainWindow, LoaderWindow

import lib.strategy
import lib.model


# class _MainWindow(QMainWindow, Ui_mainWindow):
#     """
#         Main Window
#
#         Extends both `QMainWindow` and `Ui_mainWindow`.
#
#         Attribute `classes` represents the classes that can have an instance.
#         Attribute `entries` is the list containing all instances.
#         Attribute `output_buildings` lists the program output.
#         Attribute `new_label` is the new label entered by the user.
#         Attribute `current` holds the currently processed building.
#     """
#
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)
#
#         self.classes = {}
#         self.entries = []
#         self.output_buildings = []
#
#         self.new_label = None
#         self.current = None
#
#         self.loaderAction.triggered.connect(self.show_loading_window)
#         self.actionExit.triggered.connect(self.close)
#         self.validateButton.clicked.connect(self.validate)
#         self.correctButton.clicked.connect(self.correct)



def show_main_window():
    """Affichage de l'interface principale."""

    app = QApplication(sys.argv)
    viewer = MainWindow()
    viewer.show()
    app.exec_()


if __name__ == '__main__':
    show_main_window()
