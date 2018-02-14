# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class CorrectionWindow(QtWidgets.QDialog):
    def __init__(self, classes):
        super().__init__()
        self.setupUi(classes)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def setupUi(self, choices):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(
            _translate('CorrectionWindow', "Instance class correction")
        )

        self.setObjectName('CorrectionWindow')
        self.main_layout = QtWidgets.QVBoxLayout(
            sizeConstraint=QtWidgets.QLayout.SetFixedSize
        )

        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        self.main_layout.addWidget(
            QtWidgets.QLabel(
                _translate('CorrectionWindow', 'Class correction:')
            ),
            QtCore.Qt.AlignLeft
        )

        self.choice_box = QtWidgets.QGroupBox(
            _translate('CorrectionWindow', 'Please choose the right class:')
        )
        self.choice_group = QtWidgets.QButtonGroup()
        self.choice_layout = QtWidgets.QVBoxLayout()
        for _id, choice in enumerate(choices):
            choice_button = QtWidgets.QRadioButton(choice)
            self.choice_layout.addWidget(choice_button)
            self.choice_group.addButton(choice_button)
            self.choice_group.setId(choice_button, _id)
        self.choice_box.setLayout(self.choice_layout)
        self.main_layout.addWidget(
            self.choice_box,
            QtCore.Qt.AlignVCenter
        )

        self.buttonBox = QtWidgets.QDialogButtonBox()
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok
        )
        self.buttonBox.setObjectName("buttonBox")
        self.main_layout.addWidget(
            self.buttonBox,
            QtCore.Qt.AlignRight
        )

        self.setLayout(self.main_layout)

    def get_choice(self):
        return (
            self.choice_group.checkedId()
            if self.result() == QtWidgets.QDialog.Accepted
            else -1
        )
