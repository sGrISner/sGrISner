# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_classChoice(object):
    def setupUi(self, classChoice, choices):
        classChoice.setObjectName("classChoice")
        self.main_layout = QtWidgets.QVBoxLayout(classChoice)

        self.main_layout.addWidget(
            QtWidgets.QLabel('Class correction')
        )

        self.choice_box = QtWidgets.QGroupBox('Please enter the right class')
        self.choice_group = QtWidgets.QButtonGroup()
        self.choice_layout = QtWidgets.QVBoxLayout()
        for _id, choice in enumerate(choices):
            choice_button = QtWidgets.QRadioButton(choice)
            self.choice_layout.addWidget(choice_button)
            self.choice_group.addButton(choice_button)
            self.choice_group.setId(choice_button, _id)
        self.choice_box.setLayout(self.choice_layout)
        self.main_layout.addWidget(self.choice_box)

        self.okButton = QtWidgets.QPushButton("OK")
        self.main_layout.addWidget(
            self.okButton
        )

        self.setLayout(self.main_layout)

    def retranslateUi(self, classChoice):
        _translate = QtCore.QCoreApplication.translate
        classChoice.setWindowTitle(
            _translate("classChoice", "Instance class correction")
        )
