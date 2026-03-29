import pytest  # pour fixture
from pytest_bdd import scenario, given, when, then, parsers
from Code.marss import *  # recupererCmdLine, recupererTouteLaConf
import os
from pathlib import Path
import pprint
from bs4 import BeautifulSoup

here = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

# ---------------------- CONFIGURATION

# CONFIGURATION given

@given("Je Ne Précise Pas La Configuration")
def indiquer_configuration_defaut(echanges):
    """ nominal, conf par défaut """
    dirname = os.path.dirname(__file__)
    myConf = os.path.join(dirname, "../../Conf/conf.yaml")
    echanges['confFile'] = myConf

@given("Je Précise La Configuration")
def indiquer_configuration_precise(echanges):
    dirname = os.path.dirname(__file__)
    myConf = os.path.join(dirname, "../../Tests/Dataset/conf.yaml")
    echanges['confFile'] = myConf

@given("j'indique une configuration inexistante")
def indiquer_configuration_erreur(echanges):
    #dirname = os.path.dirname(__file__)
    #myConf = os.path.join(dirname, "../../Tests/Dataset/Autre/conf-erreur.yaml")
    #echanges['confFile'] = myConf
    # fixture echoue meme : raise ValueError(f"{request.fixturename} did not yield a value") from None
    echanges["cheminInexistant"] = "../../Tests/Dataset/aute/conf-erreur.yaml"
    pass

@given("J'ai une configuration mal formatée")
def indiquer_configuration_format(echanges):
    dirname = os.path.dirname(__file__)
    myConf = os.path.join(dirname, "../../Tests/Dataset/conf-format.yaml")
    echanges['confFile'] = myConf

# CONFIGURATION when

@when("je récupère la configuration")
def recuperer_configuration(echanges):
    """ recupéartion simple de la conf
    """
    conf = recupererTouteLaConf(echanges['confFile'])
    echanges['confData'] = conf
    # print(conf)

@when("Je récupère la configuration inexistante")
def recuperer_configuration(echanges):
    dirname = os.path.dirname(__file__)
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        myConf = os.path.join(dirname, echanges["cheminInexistant"])
        conf = recupererTouteLaConf(myConf)
    # a déporter dans autre step
    # assert pytest_wrapped_e.type == SystemExit
    # assert pytest_wrapped_e.value.code == 1
    echanges['erreur'] = pytest_wrapped_e

@when("Je récupère la configuration mal formatée")
def recuperer_conf_mauvais_format(echanges):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        conf = recupererTouteLaConf(echanges['confFile'])
    echanges['erreur'] = pytest_wrapped_e

# CONFIGURATION then

@then("Je Recois La Configuration par défaut")
def lire_configuration_defaut(echanges):

    assert echanges['confData']['version'] == "ST-0.2.0"
    # print("retour:", echanges['confData']['version'])

@then("Je Recois La Configuration Personnalisée")
def lire_configuration_personnalisee(echanges):

    assert echanges['confData']['version'] == "TEST-0.2.0"
    # print("retour:", echanges['confData']['version'])

@then("Je reçois une erreur de format")
def recevoir_erreur(echanges):
    assert echanges['erreur'].type == SystemExit
    assert echanges['erreur'].value.code == 2
    # même erreur pour deux cas ?

@then("Je reçois une erreur de chemin")
def recevoir_erreur(echanges):
    assert echanges['erreur'].type == SystemExit
    assert echanges['erreur'].value.code == 1
    # même erreur pour deux cas ?

# ----------------------------- CONTENU

# CONTENU given

@given("le contenu n'a que du markdown")
def dataset_mixte_indiquer(echanges):
    dirname = os.path.dirname(__file__)
    myConf = os.path.join(dirname, "../../Tests/Dataset/conf-propre.yaml")
    echanges['confFile'] = myConf
    
@given("Le Contenu A Des Fichiers Markdown Parmi D'autres Extensions")
def dataset_mixte_indiquer(echanges):
    dirname = os.path.dirname(__file__)
    myConf = os.path.join(dirname, "../../Tests/Dataset/conf-mixte.yaml")
    echanges['confFile'] = myConf

# CONTENU when

@when("Je Récupère Les Fichiers")
def dataset_mixte_recuperer(echanges):
    conf = recupererTouteLaConf(echanges['confFile'])
    echanges['contenuMd']= listerFichiersExtensionRepertoire()
    # print('liste md:', echanges['contenuMd'])

 # CONTENU then

@then("Je Recois La Liste Des Fichiers Markdown Exclusivement")
def liste_markdown(echanges):
    """
    dépendance forte au jeu de donnée sélectionné en given
    peu indépendant tel quel
    """ 
    expected_Size = 2
    print("here:", here)  # accessible depuis ce fichier
    # désormais PosiXPath en liste avec virgule ou non en fin
    expected_Liste = [
        Path(f'{here}/Dataset/Content-propre/01.md'), 
        Path(f'{here}/Dataset/Content-propre/02.md')
    ]

    assert expected_Size == len(echanges['contenuMd'])  # redondant ou info fine
    assert expected_Liste == echanges['contenuMd']

@then("Je Recois La Liste Des Fichiers Markdown")
def liste_markdown(echanges):
    """
    dépendance forte au jeu de donnée sélectionné en given
    peu indépendant tel quel
    """ 

    expected_Size = 2
    # désormais PosiXPath en liste avec virgule ou non en fin
    expected_Liste = [
        Path(f'{here}/Dataset/Content-mixte/01.md'), 
        Path(f'{here}/Dataset/Content-mixte/02.md')
    ]

    assert expected_Size == len(echanges['contenuMd'])  # redondant ou info fine
    assert expected_Liste == echanges['contenuMd']

@then("Les Fichiers D'autres Extensions Sont Absents")
def dataset_mixte_exclusion(echanges):

    unexpected_File = Path('/home/user/Documents/marss/Tests/Dataset/Content-mixte/autre.txt')
    
    assert unexpected_File  not in  echanges['contenuMd']

#------------------------------ HTML 

# HTML given

@given("la liste des markdowns propre est prête")
def md_avec_categorie(echanges):
    echanges['listeMd'] = [
        Path(f'{here}/Dataset/Content-categorie/DEV-01.md'), 
        Path(f'{here}/Dataset/Content-categorie/TEST-02.md'),
        Path(f'{here}/Dataset/Content-categorie/DEV-33.md'),
    ]
    # toujours recuperer la conf
    dirname = os.path.dirname(__file__)
    myConf = os.path.join(dirname, "../../Tests/Dataset/conf-propre.yaml")
    conf = recupererTouteLaConf(myConf)  # acessible en global à l'application

@given("la liste des markdowns parfois sans préfixe est prête")
def md_avec_categorie(echanges):
    echanges['listeMd'] = [
        Path(f'{here}/Dataset/Content-categorie/DEV-01.md'), 
        Path(f'{here}/Dataset/Content-categorie/02.md'),
        Path(f'{here}/Dataset/Content-categorie/DEV-33.md'),
    ]

@given("le référentiel complet des pages est disponible")
def referentiel_md_html(echanges):
    echanges['referentiel'] = [
        ('DEV',
         '01',
         'DEV-01.html',
          Path('/home/user/Documents/marss/Tests/Dataset/Content-categorie/DEV-01.md')
        ),
        ('DEV',
        '33',
        'DEV-33.html',
         Path('/home/user/Documents/marss/Tests/Dataset/Content-categorie/DEV-33.md')
        ),
        ('TEST',
         '02',
         'TEST-02.html',
          Path('/home/user/Documents/marss/Tests/Dataset/Content-categorie/TEST-02.md')
        )
    ]


@given("la liste de libellé url")
def liens_html(echanges):
    echanges['liens'] = {
        'DEV': [
                {'label': '01', 'url': 'DEV-01.html'},
                {'label': '33', 'url': 'DEV-33.html'}
               ],
        'TEST': [
            {'label': '02', 'url': 'TEST-02.html'}
            ]
            }

@given(parsers.parse("le préfixe footer est {presence_configuration} en configuration"))
def presence_footer(echanges, presence_configuration ):
    # conf = dict()
    if presence_configuration == "present":        
        echanges['footerLiens'] = "FOOTER"
    else:
        echanges['footerLiens'] = ""
    print(echanges)

@given(parsers.parse("les pages correspondant au préfixe footer sont {presence_page}"))
def presence_pages_prefixe_footer(echanges, presence_page):
    if presence_page == "presentes":
        echanges['referentiel'] = {'FOOTER': [
             {'label': 'ligne editoriale',
             'url': 'FOOTER-ligne-editoriale.html'},
            {'label': 'mentions legales',
             'url': 'FOOTER-mentions-legales.html'}
             ], # type: ignore
        'PROJET': [
            {'label': 'doser effort', 'url': 'PROJET-doser-effort.html'},
            {'label': 'etude opportunite',
             'url': 'PROJET-etude-opportunite.html'},
            {'label': 'fonctionnalites', 'url': 'PROJET-fonctionnalites.html'}
        ] }# type: ignore
    else:
        echanges['referentiel'] = {'PROJET': [
            {'label': 'doser effort', 'url': 'PROJET-doser-effort.html'},
            {'label': 'etude opportunite',
             'url': 'PROJET-etude-opportunite.html'},
            {'label': 'fonctionnalites', 'url': 'PROJET-fonctionnalites.html'}
        ] # type: ignore
        }

# WIP
@given(parsers.parse("est finalisé {args}"))
def demander_menu_footer(echanges, args):
    pass

# HTML when

@when("je demande cette liste en lien html avec catégorie")
def html_avec_categorie(echanges):
    echanges['listeHtml'] = creerReferentielPagesLiens(echanges['listeMd'])
    # je pensais que j'avais groupé par catégorie et non laissé à plat

@when("je demande la liste finale des liens")
def donner_liens_html(echanges):
    echanges['liensPages'] = creerLiensMenu(echanges['referentiel'])
    pprint.pprint(echanges['liensPages'] )
    pass

@when("je demande le menu des pages")
def demander_liste_html_pages(echanges):
    # TODO: retirer duplication de code
    dirname = os.path.dirname(__file__)
    myConf = os.path.join(dirname, "../../Tests/Dataset/conf.yaml")  
    conf = recupererTouteLaConf(myConf)
    vousEtesIci = ""
    echanges["menu_pages"] = afficherMenu(echanges['liens'], vousEtesIci)

@when("je demande le menu footer")
def demander_menu_footer(echanges):
    vousEtesIci = ""
    dirname = os.path.dirname(__file__)
    myConf = os.path.join(dirname, "../../Tests/Dataset/conf-mixte.yaml")
    recupererTouteLaConf(myConf)
    pprint.pprint(echanges['referentiel'])
    echanges["menuFooter"] = afficherLiensFooter(echanges['referentiel'], vousEtesIci)

# WIP
@when("on nettoie le dossier destination")
def demander_menu_footer(echanges):
    pass

# WIP
@when(parsers.parse("on dépose {args} dans le dossier"))
def demander_menu_footer(echanges, args):
    pass


# HTML then

@then("je reçois une liste ordonnée par catégorie")
def liste_reordonnee(echanges):
    pprint.pprint(echanges)
    assert  echanges['listeHtml'][0][0] == echanges['listeHtml'][1][0]  
    # "initialement TEST suivait DEV"
    pass

@then("j'ai un label pour chaque lien")
def lien_label(echanges):
    """
    test trivial qui a permis de découvrir le BUG-050
    """
    assert  echanges['listeHtml'][0][1] == '01' 

@then("chaque lien est vers un fichier html")
def lien_fichier(echanges):
   assert  echanges['listeHtml'][0][2] == 'DEV-01.html' 

@then("le fichier source md est consigné")
def lien_fichier(echanges):
   assert  echanges['listeHtml'][0][3] == Path(f'{here}/Dataset/Content-categorie/DEV-01.md')

@then("j'ai une catégorie par défaut pour une page sans préfixe")
def liste_reordonnee(echanges):
    pprint.pprint(echanges)
    assert  echanges['listeHtml'][2][0] == "HOME"
    pass

@then("j'ai une liste de libellé url")
def liste_labels_path_html(echanges):
    # TODO: retirer duplication de code de variable jeu de données aussi
    # duplicate content en liens_html
    expected = {
        'DEV': [
                {'label': '01', 'url': 'DEV-01.html'},
                {'label': '33', 'url': 'DEV-33.html'}
               ],
        'TEST': [
            {'label': '02', 'url': 'TEST-02.html'}
            ]
            }
    assert echanges['liensPages']  == expected

@then("j'ai une liste par catégorie")
def menu_par_categorie(echanges):
    expected_categories_nombre = 2
    expected_categories_liste_nom = ["DEV", "TEST"]

    # pprint.pprint(echanges["menu_pages"])
    soup = BeautifulSoup(echanges["menu_pages"], features='html.parser')
    echanges['soup'] = soup
    content = soup.prettify()
    # print(content)
    categories = soup.find_all("span")
    # print(categories)
    assert len(categories) == expected_categories_nombre 
    categories_liste_nom = list()
    for nom in categories:
        # print(nom.contents[0])
        categories_liste_nom.append(nom.contents[0])
    assert categories_liste_nom == expected_categories_liste_nom

@then("j'ai toutes les pages dans les bonnes catégories")
def pages_dans_menu_par_categorie(echanges):
   
    expected = [
                {'label': '01', 'url': 'DEV-01.html'},
                {'label': '33', 'url': 'DEV-33.html'}
               ]
    res = echanges['soup'].select("ul#DEV li a")
    # print(res)
    actual = list()    
    for el in res:
        data = dict()       
        data['label'] = el.contents[0]
        data['url'] = el['href']
        actual.append(data)
    assert actual == expected

    expected = [
                {'label': '02', 'url': 'TEST-02.html'}
               ]
    res = echanges['soup'].select("ul#TEST li a")
    # print(res)
    actual = list()    
    for el in res:
        data = dict()       
        data['label'] = el.contents[0]
        data['url'] = el['href']
        actual.append(data)
    assert actual == expected
    # TODO: retirer duplication de code


@then(parsers.parse("j'ai le menu footer {presence_menu} en pied de page"))
def presence_menu_footer(echanges, presence_menu): 
    # pprint.pprint(echanges["menuFooter"])
    if presence_menu == "present":
        assert  echanges["menuFooter"] != ""
    else:
        assert  echanges["menuFooter"] == ""

# WIP
@then(parsers.parse("on a {args} présent dans le dossier"))
def presence_fichier_dossier(echanges, args):
      pass
