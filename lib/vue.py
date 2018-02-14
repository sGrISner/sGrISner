# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

import lib.model


class CorrectionWindow(QtWidgets.QDialog):
    def __init__(self, classes):
        super().__init__()
        self.setupUi(classes)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def setupUi(self, choices):
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
        self.output_buildings = []

        self.new_label = None
        self.current = None

        self.setup_ui()

        self.actionLoader.triggered.connect(self.load)
        self.actionSave.triggered.connect(self.save)
        self.actionQuit.triggered.connect(self.close)
        self.actionSubmitIssue.triggered.connect(self.submite_issue)
        self.actionAbout.triggered.connect(self.about)
        # self.validateButton.clicked.connect(self.validate)
        # self.correctButton.clicked.connect(self.correct)

    def setup_ui(self):
        self.setObjectName("sGrISner")
        self.resize(800, 600)
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
        self.building_viewer.setObjectName("instanceView")
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
        self.validationBox = QtWidgets.QDialogButtonBox(QtCore.Qt.Vertical)
        self.validationBox.setCenterButtons(True)
        self.validationBox.addButton(
            'Validate', QtWidgets.QDialogButtonBox.AcceptRole
        )
        self.validationBox.addButton(
            'Correct', QtWidgets.QDialogButtonBox.RejectRole
        )
        self.info_box.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Preferred,
                QtWidgets.QSizePolicy.Fixed
            )
        )
        self.info_layout.addWidget(self.info_box, QtCore.Qt.AlignVCenter)
        self.info_layout.addItem(
            QtWidgets.QSpacerItem(
                20,
                40,
                QtWidgets.QSizePolicy.Minimum,
                QtWidgets.QSizePolicy.Maximum
            )
        )
        self.info_layout.addWidget(
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

    def load(self):
        pass
        # loader = LoaderWindow()
        # loader.show()
        # loader.exec_()
        #
        # self.margins = loader.get_margins()
        #
        # if(
        #     loader.classes_path != ''
        #     and
        #     loader.orthoimage_path != ''
        #     and
        #     loader.footprint_path != ''
        #     and
        #     loader.entries_path != ''
        # ):
        #     # Lecture du fichier csv des classes et remplissage du dictionnaire
        #     with open(loader.classes_path, newline='') as cls_file:
        #         reader = csv.DictReader(
        #             cls_file, fieldnames=['Nom', 'Description']
        #         )
        #         for row in reader:
        #             self.classes[row['Nom']] = row['Description']
        #
        #     # Lecture des résultats de la classification
        #     with open(loader.entries_path, newline='') as resuts_file:
        #         reader = csv.DictReader(
        #             resuts_file,
        #             fieldnames=['ID', 'Classe', 'Proba']
        #         )
        #         for row in reader:
        #             self.entries.append(
        #                 (row['ID'], row['Classe'], row['Proba'])
        #             )
        #
        #     # Selection des entités à présenter
        #     self.selected_entries = loader.current_strategy(self.entries)
        #
        #     # Création d'une liste d'objets Building
        #     self.input_buildings = [
        #         lib.model.Building.from_shapefile(
        #             loader.footprint_path,
        #             building_id,
        #             classe,
        #             prob
        #         )
        #         for building_id, classe, prob in self.selected_entries
        #     ]
        #     # Chargement de l'orthoimage
        #     self.background = lib.model.Background.from_geotiff(
        #         loader.orthoimage_path
        #     )
        #
        #     # Affichage et interaction
        #     self.next()

    def correction_window(self):
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
        scene = QGraphicsScene(self)
        self.building_viewer.setScene(scene)

        # Affichage de l'othoimage rognées
        item = scene.addPixmap(
            self.background.crop(
                self.current.get_bounding_box(),
                self.margins
            )
        )

        # Affichage de la géométrie
        for polygon in self.current.get_qgeometry(
            self.background,
            self.margins
        ):
            scene.addPolygon(polygon)

        self.instanceView.fitInView(item, PyQt5.QtCore.Qt.KeepAspectRatio)

    def validate(self):
        if self.current:
            self.current.probability = 1
            self.output_buildings.append(self.current)
            self.next()

    def correct(self):
        if self.current:
            self.correction_window()
            if self.new_label is None:
                self.show_building()
            else:
                self.current.classe = self.new_label
                self.current.probability = 1
                self.output_buildings.append(self.current)
                self.next()

    def next(self):
        if self.input_buildings:
            self.current = self.input_buildings.pop()
            self.show_building()
        else:
            self.save()
            self.close()

    def save(self):
        self.save_entries_path, test = QFileDialog.getSaveFileName(
            self,
            "Création du fichier de sauvegarde",
            "output_entries.csv",
            "Fichiers CSV(*.csv)",
            options=QFileDialog.Options()
        )

        if self.save_entries_path:
            with open(self.save_entries_path, 'w', newline='') as save_file:
                output_writer = csv.writer(
                    save_file, delimiter=',', quoting=csv.QUOTE_MINIMAL
                )
                for build in self.output_buildings:
                    output_writer.writerow(
                        [build.identity, build.classe, build.probability]
                    )
        else:
            QMessageBox.about(
                self,
                'Error',
                'Chemin d\'enregistrement non défini'
            )
            self.save()

    def submite_issue(self):
        QtGui.QDesktopServices.openUrl(
            QtCore.QUrl('https://github.com/ethiy/sgrisner/issues')
        )

    def about(self):
        QtGui.QDesktopServices.openUrl(
            QtCore.QUrl('https://github.com/ethiy/sgrisner')
        )
