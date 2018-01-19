#! /usr/bin/python3
# -*- coding: utf-8 -*-
# Python v3

""" - PROGRAMME PRINCIPAL - """

import sys
import numpy as np
import csv

from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QMainWindow, QFileDialog

from classificationActive import *
from choixClasse import *
from chargementFichiers import *

import strategy
import batiment



class File:

    """ --- ENREGISTREMENT CHEMIN ACCES ---

    ATTRIBUTS :
    ===========
        -path : chemin d'accès
    """

    def __init__(self,path):
        self.path = path


class ChargementFichiers (QDialog,Ui_ChargerFichier):

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

    def __init__ (self):

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
        classeChem, test = QFileDialog.getOpenFileName(self,"Sélection du fichier des classes", "","Fichier CSV (*.csv)", options=QFileDialog.Options())
        if classeChem:
            self.chemClasseLabel.setText(classeChem)    # Affiche le chemin du fichier de classes
            self.cheminClasse.path=classeChem           # Enregistre le chemin du fichier de classes

    def selectCheminResultat(self):
        resultChem, test = QFileDialog.getOpenFileName(self,"Sélection des résultats de la classification", "","Fichiers CSV (*.csv)", options=QFileDialog.Options())
        if resultChem:
            self.cheminResultLabel.setText(resultChem)  # Affiche le chemin du fichier de résutlats
            self.cheminResult.path=resultChem           # Enregistre le chemin du fichier de résultats

    def selectCheminOrtho(self):
        orthoChem, test = QFileDialog.getOpenFileName(self,"Sélection de l'orthoimage", "","Fichiers GEOTIFF (*.geotiff)", options=QFileDialog.Options())
        if orthoChem:
            self.cheminOrthoLabel.setText(orthoChem)    # Affiche le chemin de l'orthophoto
            self.cheminOrtho.path=orthoChem             # Enregistre le chemin de l'orthophoto

    def selectDossierEmprises(self):
        empriseChem = QFileDialog.getExistingDirectory(self,"Sélection du dossier contenant les emprises", "", options=QFileDialog.Options())
        if empriseChem:
            self.cheminEmpriseLabel.setText(empriseChem)    # Affiche le chemin du dossier emprise
            self.cheminEmprise.path=empriseChem             # Enregistre le chemin du dossier emprise


class ChoixClasse (QDialog,Ui_ChoixClasse):

    """--- INTERFACE DE SELECTION DES CLASSES ---

    HERITAGE : Boite de dialogue "ChoixClasse"
    ==========

    ATTRIBUTS :
    ===========

    METHODES :
    ==========
    """

    def __init__ (self):
        super().__init__()
        self.setupUi(self)


class ClassificationActive (QMainWindow,Ui_InterfacePrincipale):

    """--- INTERFACE PRINCIPALE ---

    HERITAGE : Boite de dialogue "InterfacePrincipale"
    ==========

    ATTRIBUTS :
    ===========
        - classe : dictionnaire contenant les id des classes (clef) et leur description (valeurs)
        - results : liste de tuples (id, classe, probabilié) contenant l'ensemble des résultats de classification
        - buildings : liste d'objets Batiment après processus de sélection des données

    METHODES :
    ==========
        - showChoix : affichage de la fenêtre de choix des classes
        - showChargt : permet de récupérer les chemins des fichiers à utiliser
    """

    def __init__ (self):
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


    def showChargt (self):

        # Affichage de l'interface de chargement des fichiers
        chargement = ChargementFichiers()
        chargement.show()
        chargement.exec_()

        # Test pour vérifier le bon chargement des fichiers
        if (chargement.cheminClasse.path != '') & (chargement.cheminOrtho.path != '') & (chargement.cheminEmprise.path != '') & (chargement.cheminResult.path != ''):
            # Affichage de l'état du traitement
            self.etatLabel.setText("Fichiers chargés - Le programme peut être lancé")

            # Lecture du fichier csv des classes et remplissage du dictionnaire
            with open(chargement.cheminClasse.path, newline='') as file:
                reader = csv.DictReader(file, fieldnames=['Nom','Description'])
                for row in reader :
                    self.classes[row['Nom']]= row['Description']
            #print(self.classes)

            # Lecture des résultats de la classification
            with open(chargement.cheminResult.path, newline='') as file:
                reader = csv.DictReader(file, fieldnames=['ID','Classe','Proba'])
                for row in reader :
                    self.results.append((row['ID'], row['Classe'], row['Proba']))
            #print(self.results)

            # Sélection des entités à transformer en objet batiment
            self.results = strategy.Random(3).filtre(self.results)
            #self.results = strategy.Naive.filtre(self.results)
            print(self.results)

            # Création de la liste de Batiments
            for k in range(len(self.results)):

                # Recherche de la géométrie dans le dossier des emprises
                try :
                    with open(chargement.cheminEmprise.path + "/" + self.results[k][0] + ".gml") as file:
                        # Récupérer les paramètres de géométries des fichiers ....

                        # Compléter la liste de batiments
                        self.buildings.append(batiment.Batiment(self.results[k][0],'geom',self.results[k][1],float(self.results[k][2])))
                # Si la géométrie n'existe pas, on affiche un message d'erreur
                except IOError:
                    print ("Erreur! Le fichier n'existe pas dans le dossier des emprises")

                print(self.buildings[k].identity, self.buildings[k].geometry, self.buildings[k].classe, self.buildings[k].probability)


def showMainWindow():
    """Affichage de l'interface principale."""

    app = QApplication(sys.argv)
    classification = ClassificationActive()
    classification.show()
    app.exec_()

""" Programme principal - Lancement de la fenêtre de classification"""
showMainWindow()
