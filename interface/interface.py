#! /usr/bin/python3
# -*- coding: utf-8 -*-
# Python v3

from PyQt5.QtWidgets import QApplication, QWidget, QDialog
import sys
from classificationActive import *
from choixClasse import *
from chargementFichiers import *

class ClassificationActive (QDialog,Ui_InterfacePrincipale):

    def __init__ (self):
        super().__init__()
        self.setupUi(self)

class ChargementFichiers (QDialog,Ui_ChargerFichier):

    def __init__ (self):
        super().__init__()
        self.setupUi(self)

class ChoixClasse (QDialog,Ui_ChoixClasse):

    def __init__ (self):
        super().__init__()
        self.setupUi(self)

app = QApplication(sys.argv)
classification = ClassificationActive()
classification.show()
app.exec_()

app2 = QApplication(sys.argv)
chargement = ChargementFichiers()
chargement.show()
app2.exec_()

app3 = QApplication(sys.argv)
choix = ChoixClasse()
choix.show()
app3.exec_()
