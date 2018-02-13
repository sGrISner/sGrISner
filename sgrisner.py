#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import numpy as np
import csv

from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QMainWindow, QFileDialog, QGraphicsScene, QMessageBox
from PyQt5.QtGui import QPixmap, QPolygonF
import PyQt5.QtCore

from lib.classificationActive import *
from lib.choixClasse import *
from lib.chargementFichiers import *


import lib.strategy
import lib.building
import lib.background


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
        - select_results: demande le chemin du fichier de résultats
        - select_background: demande le chemin de l'orthoimage
        - select_buildings_dir: demande le chemin du dossier des emprises
        - param_stratregy: activation/désactivation des Label des stratégies
        - get_margins: retourne les valeurs des marges
        - current_strategy(results=list):
                sélectionne les entités à présenter selon la stratégie
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        """Adresses des fichiers"""
        self.classes_path = ''
        self.results_path = ''
        self.orthoimage_path = ''
        self.footprint_path = ''

        """Connexions pour charger les fichiers"""
        self.chargerClasseButton.clicked.connect(self.select_classes)
        self.chargerResultButton.clicked.connect(self.select_results)
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

    def select_results(self):
        self.results_path, test = QFileDialog.getOpenFileName(
            self,
            "Sélection des résultats de la classification",
            "",
            "Fichiers CSV(*.csv)",
            options=QFileDialog.Options()
        )
        if self.results_path:
            self.cheminResultLabel.setText(self.results_path)

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

    def current_strategy(self, results):
        strat = [
            cle for cle in lib.strategy.STRATEGIES.keys()
            if cle == self.modeComboBox.currentText()
        ]

        if strat[0] == 'Naive':
            return(lib.strategy.Naive().filter(results))
        if strat[0] == 'Random':
            return(lib.strategy.Random(int(self.nbrEdit.text())).filter(results))


class CorrectionWindow(QDialog, Ui_ChoixClasse):
    """
    INTERFACE DE SELECTION DES CLASSES

    HERITAGE: Boite de dialogue "CorrectionWindow"
    ==========

    METHODES:
    ==========
        - check(building=Building, classes=dictionnary):
                affiche les classes possibles
        - new_choice: retourne la classe sélectionnée
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def check(self, building, classes):
        values = [cle for cle in classes.keys() if cle != lib.building.classe.strip()]

        self.newClass1.setText(values[0])
        self.helpLabel1.setToolTip(classes[values[0]])
        self.newClass2.setText(values[1])
        self.helpLabel2.setToolTip(classes[values[1]])
        self.newClass3.setText(values[2])
        self.helpLabel3.setToolTip(classes[values[2]])

    def new_choice(self):
        if self.newClass1.isChecked():
            return self.newClass1.text()
        elif self.newClass2.isChecked():
            return self.newClass2.text()
        elif self.newClass3.isChecked():
            return self.newClass3.text()
        else:
            return ''


class MainWindow(QMainWindow, Ui_InterfacePrincipale):
    """
    INTERFACE PRINCIPALE

    HERITAGE: Boite de dialogue "InterfacePrincipale"
    ==========

    ATTRIBUTS PRINCIPAUX :
    ======================
        - classes: dictionnaire des classes et de leur description.
        - results: liste de 4-tuples avec les résultats de classification.
        - output_buildings: liste d'objets Building après validation.
        - new_label: classe sélectionnée par l'utilisateur.
        - current: objet Building en cours de visualisation.

    METHODES:
    ==========
        - show_correction_window: affiche la fenêtre de correction.
        - show_loading_window: affiche la fenêtre de chargement et lis les données.
        - show_building: affiche des emprises et de l'orthoimage dans l'espace graphique.
        - validate: enregistre le Building validé par l'utilisateur.
        - correct: enregistre le Building corrgié par l'utilisateur.
        - save: sélectionne le chemin d'enregistrement et créer le fichier de sortie.
        - next: parcourt les entités.
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.classes = {}
        self.results = []
        self.output_buildings = []

        self.new_label = None
        self.current = None

        self.chargerAction.triggered.connect(self.show_loading_window)
        self.yesButton.clicked.connect(self.validate)
        self.noButton.clicked.connect(self.correct)

    def show_correction_window(self):
        choix = CorrectionWindow()
        choix.check(self.current, self.classes)
        choix.show()
        choix.exec_()

        # Stock la novuelle classe sélectionnée par l'utilisateur
        self.new_label = choix.new_choice()

    def show_building(self):
        scene = QGraphicsScene(self)
        self.entiteView.setScene(scene)

        # Affichage de l'othoimage rognées
        item = scene.addPixmap(
            self.background.crop(
                self.current.get_bounding_box(),
                self.margins
            )
        )
        # to translate in case: i_min<0 or i_max>5000
        item.setPos(0, 0)

        # Affichage de la géométrie
        for polygon in self.current.geometry:
            poly = QPolygonF()
            for sommet in polygon:
                poly.append(
                    PyQt5.QtCore.QPointF(
                        (self.current.get_bounding_box()[0][0] - sommet[0]) / self.background.pixel_sizes[1] + self.margins[0],
                        (self.current.get_bounding_box()[1][1] - sommet[1]) / self.background.pixel_sizes[0] + self.margins[1]
                    )
                )
            scene.addPolygon(poly)

        self.entiteView.fitInView(item, PyQt5.QtCore.Qt.KeepAspectRatio)

        # Affichage du texte
        self.idLabel.setText("Identitifiant: " + self.current.identity)
        self.classeLabel.setText("Classe: " + self.current.classe)
        self.probaLabel.setText(
            "Probabilité: " + str(self.current.probability)
        )
        self.helpLogo.setToolTip(self.classes[self.current.classe.strip()])

        # Bornes d'affichage
        bornes = self.background.get_crop_points(
            self.current.get_bounding_box()
        )
        self.bornexValueLabel.setText(
            '{:0.2f}, {:0.2f}'.format(bornes[0][0], bornes[0][1])
        )
        self.borneyValueLabel.setText(
            '{:0.2f}, {:0.2f}'.format(bornes[1][0], bornes[1][1])
        )

    def validate(self):
        if self.current :
            self.current.probability = 1
            self.output_buildings.append(self.current)
            self.next()

    def correct(self):
        if self.current :
            self.show_correction_window()
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
        self.save_results_path, test = QFileDialog.getSaveFileName(
            self,
            "Création du fichier de sauvegarde",
            "output_results.csv",
            "Fichiers CSV(*.csv)",
            options=QFileDialog.Options()
        )

        # Lecture du fichier csv et remplissage avec output_buildings
        if self.save_results_path:
            with open(self.save_results_path, 'w', newline='') as save_file:
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
            loader.results_path != ''
        ):
            # Lecture du fichier csv des classes et remplissage du dictionnaire
            with open(loader.classes_path, newline='') as cls_file:
                reader = csv.DictReader(
                    cls_file, fieldnames=['Nom', 'Description']
                )
                for row in reader:
                    self.classes[row['Nom']] = row['Description']

            # Lecture des résultats de la classification
            with open(loader.results_path, newline='') as resuts_file:
                reader = csv.DictReader(
                    resuts_file,
                    fieldnames=['ID', 'Classe', 'Proba']
                )
                for row in reader:
                    self.results.append(
                        (row['ID'], row['Classe'], row['Proba'])
                    )

            # Selection des entités à présenter
            self.selected_results = loader.current_strategy(self.results)

            # Création d'une liste d'objets Building
            self.input_buildings = [
                lib.building.read_building(
                    loader.footprint_path,
                    building_id,
                    classe,
                    prob
                )
                for building_id, classe, prob in self.selected_results
            ]
            # Chargement de l'orthoimage
            self.background = lib.background.Background.from_geotiff(
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
