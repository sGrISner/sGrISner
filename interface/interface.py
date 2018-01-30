#! /usr/bin/python3
# -*- coding: utf-8 -*-
# Python v3

""" - PROGRAMME PRINCIPAL - """

import sys
import numpy as np
import csv

from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QMainWindow, QFileDialog, QGraphicsScene
from PyQt5.QtGui import QPixmap, QPolygonF
from PyQt5.QtCore import QPointF

from classificationActive import *
from choixClasse import *
from chargementFichiers import *

import strategy
import building
import background

import qimage2ndarray


class LoaderWindow(QDialog, Ui_ChargerFichier):
    """
    INTERFACE DE CHARGEMENT FICHIERS

    HERITAGE: Boite de dialogue "ChargerFichier"
    ==========

    ATTRIBUTS:
    ===========
        - classe: chemin du fichier .CSV contenant les classes.
        - cheminResult: chemin du fichier .CSV contenant les résultats.
        - orthoimage_path: chemin de l'orthoimage.
        - footprint_path: chemin du dossier contenant les géométries.

    METHODES:
    ==========
        - select_classes: demande le chemin de la classe
        - select_results: demande le chemin du fichier de résultats
        - select_background: demande le chemin de l'orthoimage
        - select_buildings_dir: demande le chemin du dossier des emprises
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


class CorrectionWindow(QDialog, Ui_ChoixClasse):
    """
    INTERFACE DE SELECTION DES CLASSES

    HERITAGE: Boite de dialogue "CorrectionWindow"
    ==========

    ATTRIBUTS:
    ===========

    METHODES:
    ==========
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def check(self, building, classes):
        values = [cle for cle in classes.keys() if cle != building.classe]

        self.newClass1.setText(values[0])
        self.newClass2.setText(values[1])
        self.newClass3.setText(values[2])

    def new_choice(self):
        if self.newClass1.isChecked():
            return self.newClass1.text()
        elif self.newClass2.isChecked():
            return self.newClass2.text()
        elif self.newClass3.isChecked():
            return self.newClass3.text()
        else:
            return ''


class ClassificationActive(QMainWindow, Ui_InterfacePrincipale):
    """
    INTERFACE PRINCIPALE

    HERITAGE: Boite de dialogue "InterfacePrincipale"
    ==========

    ATTRIBUTS:
    ===========
        - classe: dictionnary of classes and the corresponding descriptions.
        - results: liste of 4-tuples representing classification results.
        - buildings: Building list after selection.

    METHODES:
    ==========
        - show_correction_window: show correction window.
        - show_loading_window: show loader window.
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.classes = {}
        self.results = []
        self.buildings = []
        self.output_buildings = []

        self.new_label = None

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
        """
        Affichage graphique des emprises et du fond de plan.
        """
        scene = QGraphicsScene(self)
        self.entiteView.setScene(scene)

        # Affichage de l'othoimage rognées
        margins = (50, 50)
        item = scene.addPixmap(
            QPixmap.fromImage(
                qimage2ndarray.array2qimage(
                    self.background.crop(
                        self.current.get_bounding_box(),
                        margins
                    )
                )
            )
        )
        # to translate in case: i_min<0 or i_max>5000
        item.setPos(0, 0)

        # Affichage de la géométrie
        for polygon in self.current.geometry:
            poly = QPolygonF()
            for sommet in polygon:
                poly.append(
                    QPointF(
                        (self.current.get_bounding_box()[0][0] - sommet[0]) / self.background.pixel_sizes[1] + margins[0],
                        (self.current.get_bounding_box()[1][1] - sommet[1]) / self.background.pixel_sizes[0] + margins[1]
                    )
                )
            scene.addPolygon(poly)

        # Affichage du texte
        self.idLabel.setText("Identitifiant: " + self.current.identity)
        self.classeLabel.setText("Classe: " + self.current.classe)
        self.probaLabel.setText(
            "Probabilité: " + str(self.current.probability)
        )

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
        self.current.probability = 1
        self.output_buildings.append(self.current)
        self.next()

    def correct(self):
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
            "",
            "Fichiers CSV(*.csv)",
            options=QFileDialog.Options()
        )

        # Lecture du fichier csv et remplissage avec output_buildings
        with open(self.save_results_path, 'w', newline='') as save_file:
            output_writer = csv.writer(
                save_file, delimiter=',', quoting=csv.QUOTE_MINIMAL
            )
            for build in self.output_buildings:
                output_writer.writerow(
                    [build.identity, build.classe, build.probability]
                )

    def show_loading_window(self):
        loader = LoaderWindow()
        loader.show()
        loader.exec_()

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

            self.selected_results = strategy.Random(3).filtre(self.results)

            self.input_buildings = [
                building.read_building(
                    loader.footprint_path,
                    building_id,
                    classe,
                    prob
                )
                for building_id, classe, prob in self.selected_results
            ]
            self.background = background.read_background(
                loader.orthoimage_path
            )

            self.next()


def show_main_window():
    """Affichage de l'interface principale."""

    app = QApplication(sys.argv)
    classification = ClassificationActive()
    classification.show()
    app.exec_()


if __name__ == '__main__':
    show_main_window()
