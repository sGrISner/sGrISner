#! /usr/bin/python3
# -*- coding: utf-8 -*-
# Python v3

from PyQt5.QtWidgets import QApplication, QWidget, QDialog
import sys
from activeLabelling import *

class ActiveLabelling (QDialog,Ui_activeLabelling):

    def __init__ (self):
        super().__init__()
        self.setupUi(self)

app = QApplication(sys.argv)
classification = ActiveLabelling()
classification.show()
app.exec_()
