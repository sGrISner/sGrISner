# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Clémence\Documents\0-ENSG\1_TRONC_COMMUN\PROJET_INFO\1_ANALYSE\active-labelling\interface\choixClasse.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ChoixClasse(object):
    def setupUi(self, ChoixClasse):
        ChoixClasse.setObjectName("ChoixClasse")
        ChoixClasse.resize(370, 350)
        self.gridLayout = QtWidgets.QGridLayout(ChoixClasse)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 4, 1, 1)
        self.helpLabel1 = QtWidgets.QLabel(ChoixClasse)
        self.helpLabel1.setMaximumSize(QtCore.QSize(20, 20))
        self.helpLabel1.setText("")
        self.helpLabel1.setPixmap(QtGui.QPixmap("question.png"))
        self.helpLabel1.setScaledContents(True)
        self.helpLabel1.setObjectName("helpLabel1")
        self.gridLayout.addWidget(self.helpLabel1, 1, 4, 1, 1)
        self.helpLabel2 = QtWidgets.QLabel(ChoixClasse)
        self.helpLabel2.setMaximumSize(QtCore.QSize(20, 20))
        self.helpLabel2.setText("")
        self.helpLabel2.setPixmap(QtGui.QPixmap("question.png"))
        self.helpLabel2.setScaledContents(True)
        self.helpLabel2.setObjectName("helpLabel2")
        self.gridLayout.addWidget(self.helpLabel2, 3, 4, 1, 1)
        self.helpLabel3 = QtWidgets.QLabel(ChoixClasse)
        self.helpLabel3.setMaximumSize(QtCore.QSize(20, 20))
        self.helpLabel3.setText("")
        self.helpLabel3.setPixmap(QtGui.QPixmap("question.png"))
        self.helpLabel3.setScaledContents(True)
        self.helpLabel3.setObjectName("helpLabel3")
        self.gridLayout.addWidget(self.helpLabel3, 5, 4, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 3, 6, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 7, 0, 1, 7)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 2, 4, 1, 1)
        self.newClass1 = QtWidgets.QRadioButton(ChoixClasse)
        self.newClass1.setObjectName("newClass1")
        self.gridLayout.addWidget(self.newClass1, 1, 2, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 1, 0, 6, 1)
        self.newClass3 = QtWidgets.QRadioButton(ChoixClasse)
        self.newClass3.setObjectName("newClass3")
        self.gridLayout.addWidget(self.newClass3, 5, 2, 1, 1)
        self.newClass2 = QtWidgets.QRadioButton(ChoixClasse)
        self.newClass2.setObjectName("newClass2")
        self.gridLayout.addWidget(self.newClass2, 3, 2, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem5, 1, 5, 6, 1)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem6, 0, 0, 1, 8)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem7, 4, 2, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem8, 2, 2, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(ChoixClasse)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 8, 0, 1, 8)

        self.retranslateUi(ChoixClasse)
        self.buttonBox.accepted.connect(ChoixClasse.accept)
        self.buttonBox.rejected.connect(ChoixClasse.reject)
        QtCore.QMetaObject.connectSlotsByName(ChoixClasse)

    def retranslateUi(self, ChoixClasse):
        _translate = QtCore.QCoreApplication.translate
        ChoixClasse.setWindowTitle(_translate("ChoixClasse", "Choix de la nouvelle classe"))
        self.newClass1.setText(_translate("ChoixClasse", "Nouvelle classe 1"))
        self.newClass3.setText(_translate("ChoixClasse", "Nouvelle classe 3"))
        self.newClass2.setText(_translate("ChoixClasse", "Nouvelle classe 2"))

#import images_rc
