#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import numpy as np
import csv

from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QMainWindow, QFileDialog, QGraphicsScene, QMessageBox
import PyQt5.QtCore

from lib.vue import CorrectionWindow, MainWindow
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
