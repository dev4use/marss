# -*- coding: utf-8 -*-
import pytest  # pour fixture
from pytest_bdd import scenario, given, when, then, parsers

from Code.marss import *  # recupererCmdLine, recupererTouteLaConf
import os
from pathlib import Path

@pytest.fixture(scope="function")
def echanges():
   """ echanges de données entre steps """
   yield {}

@scenario("generation.feature", "récupérer la configuration interne")
def test_conf_parDefaut():  # test pytest obligatoire
    pass

@scenario("generation.feature", "récupérer la configuration externe")
def test_conf_personnalisee():  # test pytest obligatoire
    pass

@scenario("generation.feature", "récupérer la configuration avec erreur de chemin")
def test_conf_avec_erreur_chemin():
    """
    Exemple : dossier content avec mauvais chemin
    """
    pass

@scenario("generation.feature", "récupérer la configuration avec erreur de format")
def test_conf_avec_erreur_format():
    """
    Exemple : champ avec =
    """
    pass

@scenario("generation.feature", "récupérer le contenu")
def test_contenu_propre_recupere():
    """
    prérequis : conf, dataset de contenu
    """
    pass

@scenario("generation.feature", "récupérer les fichiers markdown présents en contenu")
def test_contenu_mixte_recupere():
    """
    prérequis : conf, dataset de contenu
    """
    pass

@scenario("generation.feature", "récupérer les fichiers html, labels et catégories")
def test_html_correct():
    """
    prérequis : conf, dataset de contenu
    """
    pass

@scenario("generation.feature", "récupérer des fichiers html, parfois incomplets")
def test_html_avec_categorie_par_defaut():
    """
    pré requis : ressource sans préfixe
    pré requis : catégorie par défaut en configuration
    """
    pass

@scenario("generation.feature", "récupérer les liens de toutes les pages")
def test_liens_toutes_pages_html():
    pass

@scenario("generation.feature", "afficher le menu du site")
def test_menu_site():
    pass

@scenario("generation.feature", "afficher les liens du footer")
# pas de parser pour un scenario, dommage pour lisibilité du rapport
# @scenario("generation.feature", parsers.parse("afficher les liens du footer pour {cas}"))
def test_liens_footer():
    pass

@scenario("generation.feature", "disposer de tous les fichiers du site statique")
def test_depot_fichiers_statiques():
    pass

