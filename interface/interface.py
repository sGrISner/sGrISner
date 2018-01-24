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


class File:

    """ --- ENREGISTREMENT CHEMIN ACCES ---

    ATTRIBUTS :
    ===========
        -path : chemin d'accès
    """

    def __init__(self, path):
        self.path = path


class ChargementFichiers(QDialog, Ui_ChargerFichier):

    """--- INTERFACE DE CHARGEMENT FICHIERS ---

    HERITAGE : Boite de dialogue "ChargerFichier"
    ==========

    ATTRIBUTS :
    ===========
        - cheminClasse : chemin d'accès au fichier .CSV contenant les classes
        - cheminResult : chemin d'accès au fichier .CSV contenant les résultats
        - cheminOrtho : chemin d'accès au fichiet .GEOTIFF contenant l'orthoimage
        - cheminEmprise : chemin d'accès au dossier contenant les géométries des emprises

    METHODES :
    ==========
        - selectCheminClasse : demande et affiche le chemin de la classe
        - selectCheminResultat : demande et affiche le chemin du fichier de résultats
        - selectCheminOrtho : demande et affiche le chemin de l'orthoimage
        - selectDossierEmprises : demande et affiche le chemin du dossier des emprises
    """

    def __init__(self):

        super().__init__()
        self.setupUi(self)

        """Définition des objets permettant de récupérer les adresses des fichiers"""
        self.cheminClasse = File('')
        self.cheminResult = File('')
        self.cheminOrtho = File('')
        self.cheminEmprise = File('')

        """Définition des connexions pour charger les fichiers"""
        self.chargerClasseButton.clicked.connect(self.selectCheminClasse)
        self.chargerResultButton.clicked.connect(self.selectCheminResultat)
        self.chargerOrthoButton.clicked.connect(self.selectCheminOrtho)
        self.chargerEmpriseButton.clicked.connect(self.selectDossierEmprises)

    def selectCheminClasse(self):
        classeChem, test = QFileDialog.getOpenFileName(self,"Sélection du fichier des classes", "","Fichier CSV(*.csv)", options=QFileDialog.Options())
        if classeChem:
            self.chemClasseLabel.setText(classeChem)    # Affiche le chemin du fichier de classes
            self.cheminClasse.path=classeChem           # Enregistre le chemin du fichier de classes

    def selectCheminResultat(self):
        resultChem, test = QFileDialog.getOpenFileName(self,"Sélection des résultats de la classification", "","Fichiers CSV(*.csv)", options=QFileDialog.Options())
        if resultChem:
            self.cheminResultLabel.setText(resultChem)  # Affiche le chemin du fichier de résutlats
            self.cheminResult.path=resultChem           # Enregistre le chemin du fichier de résultats

    def selectCheminOrtho(self):
        orthoChem, test = QFileDialog.getOpenFileName(self,"Sélection de l'orthoimage", "","Fichiers GEOTIFF(*.geotiff)", options=QFileDialog.Options())
        if orthoChem:
            self.cheminOrthoLabel.setText(orthoChem)    # Affiche le chemin de l'orthophoto
            self.cheminOrtho.path=orthoChem             # Enregistre le chemin de l'orthophoto

    def selectDossierEmprises(self):
        empriseChem = QFileDialog.getExistingDirectory(self,"Sélection du dossier contenant les emprises", "", options=QFileDialog.Options())
        if empriseChem:
            self.cheminEmpriseLabel.setText(empriseChem)    # Affiche le chemin du dossier emprise
            self.cheminEmprise.path=empriseChem             # Enregistre le chemin du dossier emprise


class ChoixClasse(QDialog, Ui_ChoixClasse):

    """--- INTERFACE DE SELECTION DES CLASSES ---

    HERITAGE : Boite de dialogue "ChoixClasse"
    ==========

    ATTRIBUTS :
    ===========

    METHODES :
    ==========
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)


class ClassificationActive(QMainWindow, Ui_InterfacePrincipale):

    """--- INTERFACE PRINCIPALE ---

    HERITAGE : Boite de dialogue "InterfacePrincipale"
    ==========

    ATTRIBUTS :
    ===========
        - classe : dictionnaire contenant les id des classes(clef) et leur description(valeurs)
        - results : liste de tuples(id, classe, probabilié) contenant l'ensemble des résultats de classification
        - buildings : liste d'objets Building après processus de sélection des données

    METHODES :
    ==========
        - showChoix : affichage de la fenêtre de choix des classes
        - showChargt : permet de récupérer les chemins des fichiers à utiliser
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        """Initialisation des variables"""
        self.classes = {}
        self.results = []
        self.buildings = []

        """"Définition des signaux et connexions"""
        self.noButton.clicked.connect(self.showChoix)
        self.chargerAction.triggered.connect(self.showChargt)

    def showChoix(self):
        choix = ChoixClasse()
        choix.show()
        choix.exec_()

    def showData(self,building,background):

        """Fonction permettant l'affichage graphique des emprises et du fond de plan"""

        # Affichage de l'othoimage rognées
        im = background.crop(building.get_bounding_box(),(500, 500))
        scene = QGraphicsScene(self)
        scene.addPixmap(QPixmap.fromImage(qimage2ndarray.array2qimage(im)))
        self.entiteView.setScene(scene)

        # Affichage de la géométrie
        for polygon in building.geometry :
            poly = QPolygonF()
            for sommet in polygon :
                poly.append(QPointF((sommet[0] - background.reference_point[0]) / background.pixel_sizes[0],
                                    (sommet[1] - background.reference_point[1]) / -background.pixel_sizes[1]))
            scene.addPolygon(poly)

        # Affichage du texte
        self.idLabel.setText("Identitifiant : " + building.identity)
        self.classeLabel.setText("Classe : " + building.classe)
        self.probaLabel.setText("Probabilité : " + building.probability)

        # Bornes d'affichage



    def validate(self, event, building):
        # Valide ou change label
            # If self.noButton cliqué
                # Affichage fenêtre ChoixClasse
                # Enregistrement de la nouvelle classe + prob = 1

            # If self.yeSButton cliqué
                # Enregistrement classe actuelle + prob = 1
        # stock label dans building
        self.output_buildings.append(building)

    def showChargt(self):
        # Affichage de l'interface de chargement des fichiers
        chargement = ChargementFichiers()
        chargement.show()
        chargement.exec_()

        # Test pour vérifier le bon chargement des fichiers
        if(
            chargement.cheminClasse.path != ''
            and
            chargement.cheminOrtho.path != ''
            and
            chargement.cheminEmprise.path != ''
            and
            chargement.cheminResult.path != ''
        ):

            # Lecture du fichier csv des classes et remplissage du dictionnaire
            with open(chargement.cheminClasse.path, newline='') as cls_file:
                reader = csv.DictReader(
                    cls_file, fieldnames=['Nom', 'Description']
                )
                for row in reader:
                    self.classes[row['Nom']] = row['Description']

            # Lecture des résultats de la classification
            with open(chargement.cheminResult.path, newline='') as resuts_file:
                reader = csv.DictReader(
                    resuts_file,
                    fieldnames=['ID', 'Classe', 'Proba']
                )
                for row in reader:
                    self.results.append(
                        (row['ID'], row['Classe'], row['Proba'])
                    )

            # Sélection des entités à transformer en objet batiment
            self.selected_results = strategy.Random(3).filtre(self.results)
            print(self.selected_results)

            # showData(Liste des Batiments + ortho)
            self.input_buildings = [
                building.read_building(
                    chargement.cheminEmprise.path,
                    building_id,
                    classe,
                    prob
                )
                for building_id, classe, prob in self.selected_results
            ]
            self.background = background.read_background(chargement.cheminOrtho.path)

            #while self.input_buildings:
            build = self.input_buildings.pop()
            self.showData(build, self.background)
                #self.validate(eventiqucui, building)


def showMainWindow():
    """Affichage de l'interface principale."""

    app = QApplication(sys.argv)
    classification = ClassificationActive()
    classification.show()
    app.exec_()


""" Programme principal - Lancement de la fenêtre de classification"""
showMainWindow()
