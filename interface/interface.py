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

import matplotlib.pyplot as plt


class File:

    """ --- ENREGISTREMENT CHEMIN ACCES ---

    ATTRIBUTS:
    ===========
        -path: chemin d'accès
    """

    def __init__(self, path):
        self.path = path


class ChargementFichiers(QDialog, Ui_ChargerFichier):

    """--- INTERFACE DE CHARGEMENT FICHIERS ---

    HERITAGE: Boite de dialogue "ChargerFichier"
    ==========

    ATTRIBUTS:
    ===========
        - cheminClasse: chemin d'accès au fichier .CSV contenant les classes
        - cheminResult: chemin d'accès au fichier .CSV contenant les résultats
        - cheminOrtho: chemin d'accès au fichiet .GEOTIFF contenant l'orthoimage
        - cheminEmprise: chemin d'accès au dossier contenant les géométries des emprises

    METHODES:
    ==========
        - selectCheminClasse: demande et affiche le chemin de la classe
        - selectCheminResultat: demande et affiche le chemin du fichier de résultats
        - selectCheminOrtho: demande et affiche le chemin de l'orthoimage
        - selectDossierEmprises: demande et affiche le chemin du dossier des emprises
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

    HERITAGE: Boite de dialogue "ChoixClasse"
    ==========

    ATTRIBUTS:
    ===========

    METHODES:
    ==========
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def checkComplete(self, building, classes):
        values = [cle for cle in classes.keys() if cle != building.classe]

        self.newClass1.setText(values[0])
        self.newClass2.setText(values[1])
        self.newClass3.setText(values[2])

    def btnCheck(self):

        if self.newClass1.isChecked() == True :
            return(self.newClass1.text())
        elif self.newClass2.isChecked() == True :
            return(self.newClass2.text())
        elif self.newClass3.isChecked() == True :
            return(self.newClass3.text())
        else :
            return('')

class ClassificationActive(QMainWindow, Ui_InterfacePrincipale):

    """--- INTERFACE PRINCIPALE ---

    HERITAGE: Boite de dialogue "InterfacePrincipale"
    ==========

    ATTRIBUTS:
    ===========
        - classe: dictionnaire contenant les id des classes(clef) et leur description(valeurs)
        - results: liste de tuples(id, classe, probabilié) contenant l'ensemble des résultats de classification
        - buildings: liste d'objets Building après processus de sélection des données

    METHODES:
    ==========
        - showChoix: affichage de la fenêtre de choix des classes
        - showChargt: permet de récupérer les chemins des fichiers à utiliser
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        """Initialisation des variables"""
        self.classes = {}
        self.results = []
        self.buildings = []
        self.output_buildings = []

        """"Définition des signaux et connexions"""
        self.chargerAction.triggered.connect(self.showChargt)

    def showChoix(self, building, classes):

        # Affiche la fenêtre de sélection de la nouvelle classe
        choix = ChoixClasse()
        # Sélectionne les noms de classes à afficher
        choix.checkComplete(building, classes)
        choix.show()
        choix.exec_()

        # Stock la novuelle classe sélectionnée par l'utilisateur
        self.newClasse = choix.btnCheck()

    def showData(self, building, background):

        """Fonction permettant l'affichage graphique des emprises et du fond de plan"""
        scene = QGraphicsScene(self)
        self.entiteView.setScene(scene)

        # Affichage de l'othoimage rognées
        margins = (50, 50)
        item = scene.addPixmap(
            QPixmap.fromImage(
                qimage2ndarray.array2qimage(
                    background.crop(building.get_bounding_box(), margins)
                )
            )
        )
        # to translate in case: i_min<0 or i_max>5000
        item.setPos(0, 0)

        # Affichage de la géométrie
        for polygon in building.geometry:
            poly = QPolygonF()
            for sommet in polygon:
                poly.append(
                    QPointF(
                        (building.get_bounding_box()[0][0] - sommet[0]) / background.pixel_sizes[1] + margins[0] ,
                        (building.get_bounding_box()[1][1] - sommet[1]) / background.pixel_sizes[0] + margins[1]
                    )
                )
            scene.addPolygon(poly)

        # Affichage du texte
        self.idLabel.setText("Identitifiant: " + building.identity)
        self.classeLabel.setText("Classe: " + building.classe)
        self.probaLabel.setText("Probabilité: " + building.probability)

        # Bornes d'affichage
        bornes = background.get_crop_points(building.get_bounding_box())
        self.bornexValueLabel.setText(str(round(bornes[0][0],2)) + ' , ' + str(round(bornes[0][1],2)))
        self.borneyValueLabel.setText(str(round(bornes[1][0],2)) + ' , ' + str(round(bornes[1][1],2)))

    def validate(self,building,classes):

        sender = self.sender()
        # Si le bouton cliqué est "no"
        if sender.text() == self.noButton.text() :
            # Afficher la fenêtre de choix de la classe
            self.showChoix(building=building, classes=classes)
            # Enregistrement de la nouvelle classe + prob = 1
            building.classe = self.newClasse
            building.probability = 1
            # Test d'affichage
            print(building.classe + str(building.probability) + " NO")

        # Si le bouton cliqué est "yes"
        elif sender.text() == self.yesButton.text():
            # Enregistrement classe actuelle + prob = 1
            building.probability = 1
            # Test d'affichage
            print(building.classe + str(building.probability) + " YES")

        # On stocke le résultats dans la liste output_buildings
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

            # On parcourt la liste des buildings sélectionnés
            ### PROBLEME : la boucle tourne mais ne sérrête pas pour exécuter l'affichage et la validation
            while self.input_buildings:
                # On enlève de la liste des buildings sélectionnés le dernier élément => stocké dans build
                build = self.input_buildings.pop()
                print(build)
                # On affiche l'élément build dans la fenêtre avec l'orthoimage correspondante
                self.showData(build, self.background)

                if self.noButton.clicked or self.yesButton.clicked :
                    # On lance la fonction de validation de l'entité (varie selon l'évènement considéré)
                    self.noButton.clicked.connect(lambda: self.validate(building=build, classes=self.classes))
                    self.yesButton.clicked.connect(lambda: self.validate(building=build, classes=self.classes))

                print(self.output_buildings)


def showMainWindow():
    """Affichage de l'interface principale."""

    app = QApplication(sys.argv)
    classification = ClassificationActive()
    classification.show()
    app.exec_()


""" Programme principal - Lancement de la fenêtre de classification"""
showMainWindow()
