# -*- coding: utf-8 -*-

import csv

import inspect

from PyQt5 import QtCore, QtGui, QtWidgets

import lib.model
import lib.strategy


class LoaderWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.setup_ui()

        self.strategy_parameters = []
        self.strategy = self.select_strategy()

        self.classes_button.clicked.connect(self.select_classes)
        self.entries_table_button.clicked.connect(self.select_entries_table)
        self.background_button.clicked.connect(self.select_background)
        self.instances_button.clicked.connect(self.select_instances)
        self.strategy_combo.activated.connect(self.select_strategy)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def setup_ui(self):
        self.setObjectName('LoadingWindow')
        self.setMaximumWidth(800)
        self.setMinimumWidth(600)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.loading_box = QtWidgets.QGroupBox()
        self.loading_grid = QtWidgets.QGridLayout(self.loading_box)
        self.classes_label = QtWidgets.QLabel()
        self.loading_grid.addWidget(self.classes_label, 0, 0, 1, 1)
        self.entries_table_label = QtWidgets.QLabel()
        self.loading_grid.addWidget(self.entries_table_label, 1, 0, 1, 1)
        self.instances_label = QtWidgets.QLabel()
        self.loading_grid.addWidget(self.instances_label, 2, 0, 1, 1)
        self.background_label = QtWidgets.QLabel()
        self.loading_grid.addWidget(self.background_label, 3, 0, 1, 1)
        self.classes_button = QtWidgets.QPushButton()
        self.loading_grid.addWidget(self.classes_button, 0, 5, 1, 1)
        self.entries_table_button = QtWidgets.QPushButton()
        self.loading_grid.addWidget(self.entries_table_button, 1, 5, 1, 1)
        self.instances_button = QtWidgets.QPushButton()
        self.loading_grid.addWidget(self.instances_button, 2, 5, 1, 1)
        self.background_button = QtWidgets.QPushButton()
        self.loading_grid.addWidget(self.background_button, 3, 5, 1, 1)
        self.classes_value = QtWidgets.QLineEdit()
        self.loading_grid.addWidget(self.classes_value, 0, 1, 1, 4)
        self.entries_table_value = QtWidgets.QLineEdit()
        self.loading_grid.addWidget(self.entries_table_value, 1, 1, 1, 4)
        self.instances_value = QtWidgets.QLineEdit()
        self.loading_grid.addWidget(self.instances_value, 2, 1, 1, 4)
        self.background_value = QtWidgets.QLineEdit()
        self.loading_grid.addWidget(self.background_value, 3, 1, 1, 4)
        self.main_layout.addWidget(self.loading_box, QtCore.Qt.AlignRight)

        self.strategy_box = QtWidgets.QGroupBox()
        self.strategy_grid = QtWidgets.QGridLayout(self.strategy_box)
        self.strategy_label = QtWidgets.QLabel()
        self.strategy_grid.addWidget(self.strategy_label, 0, 0, 1, 1)
        self.strategy_combo = QtWidgets.QComboBox()
        self.strategy_combo.addItems(
            [
                strat.__name__
                for strat in lib.strategy.Strategy.__subclasses__()
            ]
        )
        self.strategy_grid.addWidget(self.strategy_combo, 0, 1, 1, 4)
        self.main_layout.addWidget(self.strategy_box)

        self.margins_box = QtWidgets.QGroupBox()
        self.margins_grid = QtWidgets.QGridLayout(self.margins_box)
        self.xmarging_label = QtWidgets.QLabel()
        self.xmarging_value = QtWidgets.QLineEdit('50')
        self.xmarging_value.setMaximumWidth(100)
        self.ymarging_label = QtWidgets.QLabel()
        self.ymarging_value = QtWidgets.QLineEdit('50')
        self.ymarging_value.setMaximumWidth(100)
        self.margins_grid.addWidget(self.xmarging_label, 0, 0, 1, 1)
        self.margins_grid.addWidget(self.xmarging_value, 0, 1, 1, 1)
        self.margins_grid.addWidget(self.ymarging_label, 1, 0, 1, 1)
        self.margins_grid.addWidget(self.ymarging_value, 1, 1, 1, 1)
        self.margins_grid.addItem(
            QtWidgets.QSpacerItem(
                1,
                4,
                QtWidgets.QSizePolicy.Maximum,
                QtWidgets.QSizePolicy.Maximum
            ),
            0,
            2,
            1,
            4
        )
        self.margins_grid.addItem(
            QtWidgets.QSpacerItem(1, 4),
            1,
            2,
            1,
            4
        )
        self.main_layout.addWidget(self.margins_box)

        self.button_box = QtWidgets.QDialogButtonBox(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok
        )
        self.main_layout.addWidget(
            self.button_box,
            QtCore.Qt.AlignRight
        )

        self.setLayout(self.main_layout)
        self.retranslate_ui()

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.loading_box.setTitle(
            _translate('LoadingWindow', 'Loading files:')
        )
        self.classes_label.setText(
            _translate('LoadingWindow', 'Classes/Labels definition:')
        )
        self.entries_table_label.setText(
            _translate('LoadingWindow', 'Results:')
        )
        self.instances_label.setText(
            _translate('LoadingWindow', 'Instances:')
        )
        self.background_label.setText(
            _translate('LoadingWindow', 'Background:')
        )
        self.classes_button.setText(
            _translate('LoadingWindow', 'Browse...')
        )
        self.entries_table_button.setText(
            _translate('LoadingWindow', 'Browse...')
        )
        self.instances_button.setText(
            _translate('LoadingWindow', 'Browse...')
        )
        self.background_button.setText(
            _translate('LoadingWindow', 'Browse...')
        )

        self.strategy_box.setTitle(
            _translate('LoadingWindow', 'Selecting strategy:')
        )
        self.strategy_label.setText(
            _translate('LoadingWindow', 'Strategy:')
        )

        self.margins_box.setTitle(
            _translate('LoadingWindow', 'Margins:')
        )
        self.xmarging_label.setText(
            _translate('LoadingWindow', 'Horizontal margin:')
        )
        self.ymarging_label.setText(
            _translate('LoadingWindow', 'Vertical margin:')
        )

    def select_strategy(self):
        self.strategy = getattr(
            lib.strategy,
            str(
                self.strategy_combo.currentText()
            )
        )

        for parameter_label, parameter_value in self.strategy_parameters:
            self.strategy_grid.removeWidget(parameter_label)
            self.strategy_grid.removeWidget(parameter_value)
            parameter_label.deleteLater()
            parameter_value.deleteLater()
            parameter_label = None
            parameter_value = None
        self.strategy_parameters = [
            (
                QtWidgets.QLabel(arg),
                QtWidgets.QLineEdit('1')
            )
            for arg
            in inspect.getargspec(self.strategy.__init__).args
            if arg != 'self'
        ]
        for index, (parameter_label, parameter_value) in enumerate(
            self.strategy_parameters
        ):
            self.strategy_grid.addWidget(parameter_label, 1 + index, 1, 1, 2)
            self.strategy_grid.addWidget(parameter_value, 1 + index, 3, 1, 2)

    def select_classes(self):
        self.classes_path, test = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Classes file selecetion",
            self.classes_value.text(),
            "Fichier CSV(*.csv)",
            options=QtWidgets.QFileDialog.Options()
        )
        if self.classes_path:
            self.classes_value.setText(self.classes_path)

    def select_entries_table(self):
        self.entries_table_path, test = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Sélection des résultats de la classification",
            self.entries_table_value.text(),
            "Fichiers CSV(*.csv)",
            options=QtWidgets.QFileDialog.Options()
        )
        if self.entries_table_path:
            self.entries_table_value.setText(self.entries_table_path)

    def select_background(self):
        self.background_path, test = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Sélection de l'orthoimage",
            self.background_value.text(),
            "Fichiers GEOTIFF(*.geotiff)",
            options=QtWidgets.QFileDialog.Options()
        )
        if self.background_path:
            self.background_value.setText(self.background_path)

    def select_instances(self):
        self.instances_path = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "Sélection du dossier contenant les emprises",
            self.instances_value.text(),
            options=QtWidgets.QFileDialog.Options()
        )
        if self.instances_path:
            self.instances_value.setText(self.instances_path)

    def get_strategy(self):
        return self.strategy(
            *[
                int(parameter_value.text())
                for _, parameter_value in self.strategy_parameters
            ]
        ) if self.result() == QtWidgets.QDialog.Accepted else None

    def get_classes(self):
        with open(self.classes_value.text(), newline='') as cls_file:
            return {
                name.strip(): description
                for name, description in csv.reader(cls_file, delimiter=',')
            } if self.result() == QtWidgets.QDialog.Accepted else {}

    def get_entries(self):
        with open(self.entries_table_value.text(), newline='') as table_file:
            return [
                lib.model.Building.from_shapefile(
                    self.instances_value.text(),
                    building_id.strip(),
                    classe.strip(),
                    float(prob)
                )
                for building_id, classe, prob in csv.reader(
                    table_file, delimiter=','
                )
            ] if self.result() == QtWidgets.QDialog.Accepted else []

    def get_background(self):
        return lib.model.Background.from_geotiff(
            self.background_value.text()
        ) if self.result() == QtWidgets.QDialog.Accepted else None

    def get_margins(self):
        return(
            int(self.xmarging_value.text()),
            int(self.ymarging_value.text())
        ) if self.result() == QtWidgets.QDialog.Accepted else None


class CorrectionWindow(QtWidgets.QDialog):
    def __init__(self, classes):
        super().__init__()

        self.setup_ui(classes)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def setup_ui(self, choices):
        self.setObjectName('CorrectionWindow')
        self.main_layout = QtWidgets.QVBoxLayout(
            sizeConstraint=QtWidgets.QLayout.SetFixedSize
        )

        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        self.choice_box = QtWidgets.QGroupBox()
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

        self.button_box = QtWidgets.QDialogButtonBox()
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok
        )
        self.button_box.setObjectName("button_box")
        self.main_layout.addWidget(
            self.button_box,
            QtCore.Qt.AlignRight
        )

        self.setLayout(self.main_layout)
        self.retranslate_ui()

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(
            _translate('CorrectionWindow', "Instance class correction")
        )
        self.choice_box.setTitle(
            _translate('CorrectionWindow', 'Please choose the right class:')
        )

    def get_choice(self):
        return (
            self.choice_group.checkedId()
            if self.result() == QtWidgets.QDialog.Accepted
            else -1
        )


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.classes = {}
        self.entries = []
        self.output_instances = []

        self.new_label = None
        self.current = None

        self.setup_ui()

        self.actionLoader.triggered.connect(self.pop_load)
        self.actionSave.triggered.connect(self.save)
        self.actionQuit.triggered.connect(self.close)
        self.actionSubmitIssue.triggered.connect(self.submite_issue)
        self.actionAbout.triggered.connect(self.about)
        self.validate_button.clicked.connect(self.validate)
        self.correct_button.clicked.connect(self.correct)

    def setup_ui(self):
        self.setObjectName("sGrISner")
        self.setMinimumSize(QtCore.QSize(800, 600))

        self.setup_menu_bar()
        self.setup_central_widget()

        self.retranslate_ui()

    def setup_menu_bar(self):
        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar()
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.actionSubmitIssue = QtWidgets.QAction()
        self.actionSubmitIssue.setObjectName("actionSubmitIssue")
        self.actionAbout = QtWidgets.QAction()
        self.actionAbout.setObjectName("actionAbout")
        self.actionLoader = QtWidgets.QAction()
        self.actionLoader.setObjectName("actionLoader")
        self.actionQuit = QtWidgets.QAction()
        self.actionQuit.setObjectName("actionQuit")
        self.actionSave = QtWidgets.QAction()
        self.actionSave.setObjectName("actionSave")
        self.menuFile.addAction(self.actionLoader)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionSubmitIssue)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

    def setup_central_widget(self):
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)

        self.main_layout = QtWidgets.QGridLayout(self.centralwidget)
        self.main_layout.setObjectName("gridLayout")

        self.main_layout.setContentsMargins(10, 10, 10, 10)

        self.building_viewer = QtWidgets.QGraphicsView()
        self.building_viewer.setMinimumSize(QtCore.QSize(400, 400))
        policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Preferred
        )
        policy.setWidthForHeight(True)
        self.building_viewer.setSizePolicy(policy)
        self.building_viewer.setObjectName("buildingViewer")
        self.main_layout.addWidget(self.building_viewer, 0, 0, 10, 10)

        self.info_layout = QtWidgets.QVBoxLayout()
        self.info_box = QtWidgets.QGroupBox()
        self.info_grid = QtWidgets.QGridLayout(self.info_box)
        self.identity_label = QtWidgets.QLabel()
        self.info_grid.addWidget(self.identity_label, 0, 0)
        self.identity_value = QtWidgets.QLabel(
            None if self.current is None else self.current.identity
        )
        self.info_grid.addWidget(self.identity_value, 0, 1)
        self.class_label = QtWidgets.QLabel()
        self.info_grid.addWidget(self.class_label, 1, 0)
        self.class_value = QtWidgets.QLabel(
            None if self.current is None else self.current.classe
        )
        self.info_grid.addWidget(self.class_value, 1, 1)
        self.probability_label = QtWidgets.QLabel()
        self.info_grid.addWidget(self.probability_label, 2, 0)
        self.probability_value = QtWidgets.QLabel(
            None if self.current is None else self.current.probability
        )
        self.info_grid.addWidget(self.probability_value, 2, 1)
        self.info_box.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Preferred,
                QtWidgets.QSizePolicy.Fixed
            )
        )
        self.validationBox = QtWidgets.QVBoxLayout()
        self.validate_button = QtWidgets.QPushButton('Validate')
        self.validationBox.addWidget(self.validate_button)
        self.correct_button = QtWidgets.QPushButton('Correct')
        self.validationBox.addWidget(self.correct_button)

        self.info_layout.addWidget(self.info_box, QtCore.Qt.AlignVCenter)
        self.info_layout.addItem(
            QtWidgets.QSpacerItem(
                20,
                40,
                QtWidgets.QSizePolicy.Minimum,
                QtWidgets.QSizePolicy.Maximum
            )
        )
        self.info_layout.addLayout(
            self.validationBox,
            QtCore.Qt.AlignBottom
        )
        self.main_layout.addLayout(self.info_layout, 0, 10, 10, 1)

        self.bounds_layout = QtWidgets.QGridLayout()
        xs, ys = self.get_view_bounds()
        self.bounds_label = QtWidgets.QLabel()
        self.bounds_layout.addWidget(self.bounds_label, 0, 0)
        self.xbound_value = QtWidgets.QLabel(xs)
        self.bounds_layout.addWidget(self.xbound_value, 0, 1)
        self.ybound_value = QtWidgets.QLabel(ys)
        self.bounds_layout.addWidget(self.ybound_value, 1, 1)
        self.main_layout.addLayout(self.bounds_layout, 10, 0, 1, 1)

    def get_view_bounds(self):
        if self.current is None:
            return ('(x_min, xmax)', '(y_min, ymax)')
        else:
            (i_max, j_min), (i_min, j_max) = self.background.get_crop_points(
                self.current.get_bounding_box()
            )
            return (
                '{:0.2f}, {:0.2f}'.format(j_min, j_max),
                '{:0.2f}, {:0.2f}'.format(i_max, i_min)
            )

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("sGrISner", "sGrISner"))
        self.menuFile.setTitle(_translate("sGrISner", "File"))
        self.menuHelp.setTitle(_translate("sGrISner", "Help"))
        self.actionSubmitIssue.setText(
            _translate(
                "sGrISner",
                'Submit Issue...'
            )
        )
        self.actionAbout.setText(_translate("sGrISner", "About sGrISner"))
        self.actionLoader.setText(_translate("sGrISner", "Load Files..."))
        self.actionQuit.setText(_translate("sGrISner", "Quit"))
        self.actionSave.setText(_translate("sGrISner", "Save..."))
        self.info_box.setTitle(
            _translate(
                'sGrISner',
                'Instance informations:'
            )
        )
        self.identity_label.setText(_translate("sGrISner", 'Identifier:'))
        self.class_label.setText(_translate("sGrISner", 'Class:'))
        self.probability_label.setText(_translate("sGrISner", 'Probability:'))
        self.bounds_label.setText(_translate("sGrISner", 'Bounds:'))

    def pop_load(self):
        loader = LoaderWindow()
        loader.show()
        loader.exec_()

        self.margins = loader.get_margins()
        self.strategy = loader.get_strategy()

        try:
            self.classes = loader.get_classes()
            self.entries = loader.get_entries()
            self.background = loader.get_background()
        except FileNotFoundError:
            pass

        if self.classes and self.entries and self.strategy and self.background:
            self.input_instances = self.strategy.filter(self.entries)
            self.next()

    def pop_correction(self):
        possible_classes = [
            cls
            for cls in self.classes.keys()
            if cls != self.current.classe
        ]
        choice_window = CorrectionWindow(
            possible_classes
        )
        choice_window.show()
        choice_window.exec_()

        _id = choice_window.get_choice()
        self.new_label = (
            possible_classes[_id]
            if _id >= 0 else None
        )

    def show_building(self):
        self.identity_value.setText(self.current.identity)
        self.class_value.setText(self.current.classe)
        self.probability_value.setText(str(self.current.probability))
        xs, ys = self.get_view_bounds()
        self.xbound_value.setText(xs)
        self.ybound_value.setText(ys)

        scene = QtWidgets.QGraphicsScene(self)
        self.building_viewer.setScene(scene)

        item = scene.addPixmap(
            self.background.crop(
                self.current.get_bounding_box(),
                self.margins
            )
        )

        for polygon in self.current.get_qgeometry(
            self.background,
            self.margins
        ):
            scene.addPolygon(polygon)

        self.building_viewer.fitInView(item, QtCore.Qt.KeepAspectRatio)

    def validate(self):
        if self.current:
            self.current.probability = 1
            self.output_instances.append(self.current)
            self.next()

    def correct(self):
        if self.current:
            self.pop_correction()
            if self.new_label is None:
                self.show_building()
            else:
                self.current.classe = self.new_label
                self.current.probability = 1
                self.output_instances.append(self.current)
                self.next()

    def next(self):
        if self.input_instances:
            self.current = self.input_instances.pop()
            self.show_building()
        else:
            self.save()
            self.close()

    def save(self):
        self.save_path, test = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Création du fichier de sauvegarde",
            "output.csv",
            "Fichiers CSV(*.csv)",
            options=QtWidgets.QFileDialog.Options()
        )

        if self.save_path:
            with open(self.save_path, 'w', newline='') as save_file:
                output_writer = csv.writer(
                    save_file, delimiter=',', quoting=csv.QUOTE_MINIMAL
                )
                for build in self.output_instances:
                    output_writer.writerow(
                        [build.identity, build.classe, build.probability]
                    )

    def submite_issue(self):
        QtGui.QDesktopServices.openUrl(
            QtCore.QUrl('https://github.com/ethiy/sgrisner/issues')
        )

    def about(self):
        QtGui.QDesktopServices.openUrl(
            QtCore.QUrl('https://github.com/ethiy/sgrisner')
        )
