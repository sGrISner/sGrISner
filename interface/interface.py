#! /usr/bin/python3
# -*- coding: utf-8 -*-
# Python v3

from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QMainWindow, QFileDialog
import sys
import numpy as np
import csv
from classificationActive import *
from choixClasse import *
from chargementFichiers import *
from select import *

"""Classe permettant l'enregistrement d'un chemin d'accès"""
class File():

    def __init__(self,path):
        self.path=path          # attribut permettant d'accéder au chemin d'accès

"""Classe correpsondant à l'interface de chargement des fichiers"""
class ChargementFichiers (QDialog,Ui_ChargerFichier):

    def __init__ (self):
        """Définition des objets permettant de récupérer les adresses des fichiers"""
        super().__init__()
        self.setupUi(self)

        self.cheminClasse=File('')
        self.cheminResult=File('')
        self.cheminOrtho=File('')
        self.cheminEmprise=File('')

        """Définition des signaux et connexions"""

        # Chargement des fichiers
        self.chargerClasseButton.clicked.connect(self.selectCheminClasse)
        self.chargerResultButton.clicked.connect(self.selectCheminResultat)
        self.chargerOrthoButton.clicked.connect(self.selectCheminOrtho)
        self.chargerEmpriseButton.clicked.connect(self.selectDossierEmprises)

    def selectCheminClasse(self):
        """Demander et afficher le chemin de la classe"""
        option = QFileDialog.Options()
        classeChem, test = QFileDialog.getOpenFileName(self,"Sélection du fichier des classes", "","Fichier CSV (*.csv)", options=option)
        if classeChem:
            self.chemClasseLabel.setText(classeChem)    # Affiche le chemin du fichier de classes
            self.cheminClasse.path=classeChem           # Enregistre le chemin du fichier de classes

    def selectCheminResultat(self):
        """Demander et afficher le chemin des résultats de la classification"""
        option = QFileDialog.Options()
        resultChem, test = QFileDialog.getOpenFileName(self,"Sélection des résultats de la classification", "","Fichiers CSV (*.csv)", options=option)
        if resultChem:
            self.cheminResultLabel.setText(resultChem)  # Affiche le chemin du fichier de résutlats
            self.cheminResult.path=resultChem           # Enregistre le chemin du fichier de résultats

    def selectCheminOrtho(self):
        """Demander et afficher le chemin de l'orthoimage"""
        option = QFileDialog.Options()
        orthoChem, test = QFileDialog.getOpenFileName(self,"Sélection de l'orthoimage", "","Fichiers GEOTIFF (*.geotiff)", options=option)
        if orthoChem:
            self.cheminOrthoLabel.setText(orthoChem)    # Affiche le chemin de l'orthophoto
            self.cheminOrtho.path=orthoChem             # Enregistre le chemin de l'orthophoto

    def selectDossierEmprises(self):
        """Demander et afficher le chemin du dossier des emprises"""
        option = QFileDialog.Options()
        empriseChem = QFileDialog.getExistingDirectory(self,"Sélection du dossier contenant les emprises", "", options=option)
        if empriseChem:
            self.cheminEmpriseLabel.setText(empriseChem)    # Affiche le chemin du dossier emprise
            self.cheminEmprise.path=empriseChem             # Enregistre le chemin du dossier emprise

"""Classe correpsondant à l'interface de sélection de nouvelles classes"""
class ChoixClasse (QDialog,Ui_ChoixClasse):

    def __init__ (self):
        super().__init__()
        self.setupUi(self)

"""Classe correpsondant à l'interface principale """
class ClassificationActive (QMainWindow,Ui_InterfacePrincipale):

    def __init__ (self):
        super().__init__()
        self.setupUi(self)

        """Initialisation des variables"""
        self.classes = {}
        self.results = []

        """"Définition des signaux et connexions"""
        self.noButton.clicked.connect(self.showChoix)
        self.chargerAction.triggered.connect(self.showChargt)

    """Affichage de la fenêtre de choix des nouvelles classes."""
    def showChoix(self):
        choix = ChoixClasse()
        choix.show()
        choix.exec_()

    """Affichage de la fenêtre de chargement des fichiers & renseignement des variables"""
    def showChargt (self):
        chargement = ChargementFichiers()
        chargement.show()
        chargement.exec_()

        # Test pour vérifier le bon chargement des fichiers
        if (chargement.cheminClasse.path != '') & (chargement.cheminOrtho.path != '') & (chargement.cheminEmprise.path != '') & (chargement.cheminResult.path != ''):
            # Affichage de l'état du traitement
            self.etatLabel.setText("Fichiers chargés - Le programme peut être lancé")

            # Lecture du fichier csv des classes et remplissage du dictionnaire
            with open(chargement.cheminClasse.path, newline='') as file:
                reader=csv.DictReader(file, fieldnames=['Nom','Description'])
                for row in reader :
                    self.classes[row['Nom']]= row['Description']
            print(self.classes)

            # Lecture des résultats de la classification
            with open(chargement.cheminResult.path, newline='') as file:
                reader=csv.DictReader(file, fieldnames=['ID','Classe','Proba'])
                for row in reader :
                    self.results.append((row['ID'], row['Classe'], row['Proba']))
            print(self.results)


"""Affichage de l'interface principale."""
def showMainWindow():
    app = QApplication(sys.argv)
    classification = ClassificationActive()
    classification.show()
    app.exec_()

""" Programme principal - Lancement de la fenêtre de classification"""
showMainWindow()
