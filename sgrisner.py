#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import numpy as np
import csv

from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QMainWindow, QFileDialog, QGraphicsScene, QMessageBox
import PyQt5.QtCore

from lib.mainWindow import Ui_mainWindow
from lib.classChoice import CorrectionWindow
from lib.chargementFichiers import *


import lib.strategy
import lib.model


class LoaderWindow(QDialog, Ui_ChargerFichier):
    """
    INTERFACE DE CHARGEMENT FICHIERS

    HERITAGE: Boite de dialogue "ChargerFichier"
    ==========

    ATTRIBUTS PRINCIPAUX :
    ======================
        - classe_path: chemin du fichier .CSV contenant les classes
        - result_path: chemin du fichier .CSV contenant les résultats
        - orthoimage_path: chemin de l'orthoimage
        - footprint_path: chemin du dossier contenant les géométries

    METHODES:
    ==========
        - select_classes: demande le chemin de la classe
        - select_entries: demande le chemin du fichier de résultats
        - select_background: demande le chemin de l'orthoimage
        - select_buildings_dir: demande le chemin du dossier des emprises
        - param_stratregy: activation/désactivation des Label des stratégies
        - get_margins: retourne les valeurs des marges
        - current_strategy(entries=list):
                sélectionne les entités à présenter selon la stratégie
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        """Adresses des fichiers"""
        self.classes_path = ''
        self.entries_path = ''
        self.orthoimage_path = ''
        self.footprint_path = ''

        """Connexions pour charger les fichiers"""
        self.chargerClasseButton.clicked.connect(self.select_classes)
        self.chargerResultButton.clicked.connect(self.select_entries)
        self.chargerOrthoButton.clicked.connect(self.select_background)
        self.chargerEmpriseButton.clicked.connect(self.select_buildings_dir)

        """Connexion pour la comboBox"""
        self.modeComboBox.activated.connect(self.param_stratregy)

    def param_stratregy(self):
        type_strategy = self.modeComboBox.currentText()

        if type_strategy == 'Naive':
            self.nbrLabel.setEnabled(False)
            self.nbrEdit.setEnabled(False)

        if type_strategy == 'Random':
            self.nbrLabel.setEnabled(True)
            self.nbrEdit.setEnabled(True)

    def select_classes(self):
        self.classes_path, test = QFileDialog.getOpenFileName(
            self,
            "Sélection du fichier des classes",
            "",
            "Fichier CSV(*.csv)",
            options=QFileDialog.Options()
        )
        if self.classes_path:
            self.chemClasseLabel.setText(self.classes_path)

    def select_entries(self):
        self.entries_path, test = QFileDialog.getOpenFileName(
            self,
            "Sélection des résultats de la classification",
            "",
            "Fichiers CSV(*.csv)",
            options=QFileDialog.Options()
        )
        if self.entries_path:
            self.cheminResultLabel.setText(self.entries_path)

    def select_background(self):
        self.orthoimage_path, test = QFileDialog.getOpenFileName(
            self,
            "Sélection de l'orthoimage",
            "",
            "Fichiers GEOTIFF(*.geotiff)",
            options=QFileDialog.Options()
        )
        if self.orthoimage_path:
            self.cheminOrthoLabel.setText(self.orthoimage_path)

    def select_buildings_dir(self):
        self.footprint_path = QFileDialog.getExistingDirectory(
            self,
            "Sélection du dossier contenant les emprises",
            "",
            options=QFileDialog.Options()
        )
        if self.footprint_path:
            self.cheminEmpriseLabel.setText(self.footprint_path)

    def get_margins(self):
        return(
            (
                int(self.margeXEdit.text()),
                int(self.margeYEdit.text())
            )
        )

    def current_strategy(self, entries):
        strat = [
            cle for cle in lib.strategy.STRATEGIES.keys()
            if cle == self.modeComboBox.currentText()
        ]

        if strat[0] == 'Naive':
            return(lib.strategy.Naive().filter(entries))
        if strat[0] == 'Random':
            return(lib.strategy.Random(int(self.nbrEdit.text())).filter(entries))


class MainWindow(QMainWindow, Ui_mainWindow):
    """
        Main Window

        Extends both `QMainWindow` and `Ui_mainWindow`.

        Attribute `classes` represents the classes that can have an instance.
        Attribute `entries` is the list containing all instances.
        Attribute `output_buildings` lists the program output.
        Attribute `new_label` is the new label entered by the user.
        Attribute `current` holds the currently processed building.
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.classes = {}
        self.entries = []
        self.output_buildings = []

        self.new_label = None
        self.current = None

        self.loaderAction.triggered.connect(self.show_loading_window)
        self.actionExit.triggered.connect(self.close)
        self.validateButton.clicked.connect(self.validate)
        self.correctButton.clicked.connect(self.correct)

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
            if _id >= 0 else self.correction_window()
        )

    def show_building(self):
        scene = QGraphicsScene(self)
        self.instanceView.setScene(scene)

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

        self.idLabel.setText("Identitifiant: " + self.current.identity)
        self.classLabel.setText("Classe: " + self.current.classe)
        self.probaLabel.setText(
            "Probabilité: " + str(self.current.probability)
        )
        self.helpLogo.setToolTip(self.classes[self.current.classe.strip()])

        (i_max, j_min), (i_min, j_max) = self.background.get_crop_points(
            self.current.get_bounding_box()
        )
        self.boundxValueLabel.setText(
            '{:0.2f}, {:0.2f}'.format(j_min, j_max)
        )
        self.boundyValueLabel.setText(
            '{:0.2f}, {:0.2f}'.format(i_max, i_min)
        )

    def validate(self):
        if self.current:
            self.current.probability = 1
            self.output_buildings.append(self.current)
            self.next()

    def correct(self):
        if self.current:
            self.correction_window()
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

        # Sélection du chemin d'enregistrement
        self.save_entries_path, test = QFileDialog.getSaveFileName(
            self,
            "Création du fichier de sauvegarde",
            "output_entries.csv",
            "Fichiers CSV(*.csv)",
            options=QFileDialog.Options()
        )

        # Lecture du fichier csv et remplissage avec output_buildings
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

    def show_loading_window(self):
        loader = LoaderWindow()
        loader.show()
        loader.exec_()

        self.margins = loader.get_margins()

        if(
            loader.classes_path != ''
            and
            loader.orthoimage_path != ''
            and
            loader.footprint_path != ''
            and
            loader.entries_path != ''
        ):
            # Lecture du fichier csv des classes et remplissage du dictionnaire
            with open(loader.classes_path, newline='') as cls_file:
                reader = csv.DictReader(
                    cls_file, fieldnames=['Nom', 'Description']
                )
                for row in reader:
                    self.classes[row['Nom']] = row['Description']

            # Lecture des résultats de la classification
            with open(loader.entries_path, newline='') as resuts_file:
                reader = csv.DictReader(
                    resuts_file,
                    fieldnames=['ID', 'Classe', 'Proba']
                )
                for row in reader:
                    self.entries.append(
                        (row['ID'], row['Classe'], row['Proba'])
                    )

            # Selection des entités à présenter
            self.selected_entries = loader.current_strategy(self.entries)

            # Création d'une liste d'objets Building
            self.input_buildings = [
                lib.model.Building.from_shapefile(
                    loader.footprint_path,
                    building_id,
                    classe,
                    prob
                )
                for building_id, classe, prob in self.selected_entries
            ]
            # Chargement de l'orthoimage
            self.background = lib.model.Background.from_geotiff(
                loader.orthoimage_path
            )

            # Affichage et interaction
            self.next()


def show_main_window():
    """Affichage de l'interface principale."""

    app = QApplication(sys.argv)
    viewer = MainWindow()
    viewer.show()
    app.exec_()


if __name__ == '__main__':
    show_main_window()
