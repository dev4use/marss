# -*- coding: utf-8 -*-
import pytest  # pour fixture
from pytest_bdd import scenario
import os
from pathlib import Path
import itertools
"""
jointure avec le scenario de la feature
appel pytest standard
suit l'ordre des tests exposés ici et non l'ordre de la feature
"""


here = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
herePath = file_path = Path(here)

@pytest.fixture(scope="function")
def echanges():
   """ echanges de données entre steps """
   yield {}

@pytest.fixture(scope="function")
def nettoyer():
   """ nettoyer les repertoires de site statique """
   yield {}
   print("nettoyer :")
   files = Path(f'{here}/Dataset/WebSite-reference').rglob('*.*')
   files2 = Path(f'{here}/Dataset/WebSite-accueil').rglob('*.*')
   # chainer/merger generator
   def chained_generator():
        yield from files
        yield from files2
   # generator object Path.rglob
   for file in chained_generator():
    if file.name.startswith("."):
        print("ne pas supprimer :", file.name)        
    else:
        print("supprimer :", file)
        file.unlink()

@scenario("generation.feature", "récupérer la configuration interne")
def test_conf_parDefaut():  # test pytest obligatoire
    pass

@scenario("generation.feature", "récupérer la configuration externe")
def test_conf_personnalisee():
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

@scenario("generation.feature", "logger les événements")
def test_log_AlaDemande():
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

@scenario("generation.feature", "récupérer des fichiers markdown en doublon")
def test_contenu_doublon_recupere():
    """
    prérequis : conf, dataset de contenu avec doublon
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

@scenario("generation.feature", "transformer les liens md")
def test_transformer_les_liens_md():
    pass

@scenario("generation.feature", "transformer le chemin image")
def test_changer_chemin_image_md():
    pass

@scenario("generation.feature", "récupérer le contenu md de la page d'accueil")
def test_contenu_initial_accueil():
    pass

@scenario("generation.feature", "récupérer le contenu html de la page d'accueil")
def test_contenu_html_accueil():
    pass

@scenario("generation.feature", "créer le fichier html de l'accueil")
def test_creer_page_index():
    pass

@scenario("generation.feature", "récupérer le html d'une page avec menu page actif")
def test_menu_page_actif():
    pass

@scenario("generation.feature", "récupérer les liens de toutes les pages")
def test_liens_toutes_pages_html():
    pass

@scenario("generation.feature", "afficher le menu du site")
def test_menu_site():
    pass

@scenario("generation.feature", "identifier les liens des posts précédent et suivant")
def test_liens_precedent_suivant():
    pass

@scenario("generation.feature", "récupérer les infos du markdown")
def test_infos_markdown():
    pass

@scenario("generation.feature", "afficher les liens des posts précédent et suivant")
def test_afficher_liens_precedent_suivant():
    pass

@scenario("generation.feature", "afficher les posts d'une catégorie")
def test_afficher_posts_categorie():
    pass

@scenario("generation.feature", "afficher les liens du footer")
# pas de parser pour un scenario, dommage pour lisibilité du rapport
# @scenario("generation.feature", parsers.parse("afficher les liens du footer pour {cas}"))
def test_liens_footer():
    pass

@scenario("generation.feature", "preparer le dossier de destination")
def test_nettoyer_dossier():
    pass

@scenario("generation.feature", "disposer de tous les fichiers du site statique")
def test_depot_fichiers_statiques():
    # ne trouve pas de fichier à supprimer à cause de la fixture de nettoyage
    # python -m pytest Tests/Tests/test_generation.py::test_depot_fichiers_statiques
    # test_lancer_tout_le_programme
    pass

@scenario("generation.feature", "visualiser le site statique")
def test_lancer_tout_le_programme():
    """
    appeller la page main
    et voir le serveur de debug
    """
    pass
