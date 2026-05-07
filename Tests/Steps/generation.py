import pytest  # pour fixture
from pytest_bdd import given, when, then, parsers
from Code.marss import * # mauvaise pratique
import os
from pathlib import Path
import pprint
from bs4 import BeautifulSoup
import requests
import time
import Tests.Dataset.data as data
import glob
"""
ensemble des éléments GWT appelés
"""

here = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
herePath = file_path = Path(here)

#----------------------- MAINTENANCE

@given("j'ai un fichier de log configuré")
def configurer_log(echanges):
    # conf = dict()
    # conf['logs'] = f'{here}/Dataset/flux.txt'
    # echanges['conf'] = conf   # impossible à passer comme cela
    dirname = os.path.dirname(__file__)
    myConf = os.path.join(dirname, "../Dataset/conf.yaml")
    echanges['conf'] = recupererTouteLaConf(myConf)  # initialise la conf dans marss

@given("le répertoire destination est connu")
@given("la page d'accueil est en configuration")
@given("le menu de page est en configuration")
def configurer_log(echanges):
    dirname = os.path.dirname(__file__)
    myConf = os.path.join(dirname, "../Dataset/conf-page.yaml")
    echanges['conf'] = recupererTouteLaConf(myConf) 

@when("je veux logger un événement")
def creer_log(echanges):
    aideLoggerFichier("evenement", "info")

@then("je vois apparaître l'événement en log")
def lire_log(echanges):
    print("here:", here)
    with open(f"{here}/Dataset/flux.txt", "r") as f:
        contenu = f.readlines()
        assert "---------------- evenement ----------------\n" in contenu
        assert "'info'" in contenu  # '...' effet du pformat

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
    print("\nchemin des steps de test:", dirname)
    myConf = os.path.join(dirname, "../Dataset/conf.yaml")
    print("chemin de fichier conf demande en test:", myConf)
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
    myConf = os.path.join(dirname, "../Dataset/conf-format.yaml")
    echanges['confFile'] = myConf

# CONFIGURATION when

@when("je récupère la configuration")
def recuperer_configuration(echanges):
    """ recupération simple de la conf
    """
    conf = recupererTouteLaConf(echanges['confFile'])
    echanges['confData'] = conf
    # print(conf)

@when("Je récupère la configuration inexistante")
def recuperer_configuration(echanges):
    dirname = os.path.dirname(__file__)
    with pytest.raises(SystemExit) as pytest_wrapped_e:  # ASTUCE: intercepter exit
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

    assert echanges['confData']['version'] == data.version_actuelle 
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

@given("le contenu a des fichiers au nom identique")  # peu importe la conf
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

@given("j'ai des contenus md avec lien md")
def liens_md_en_contenu(echanges):
    echanges["contenu"] = data.contenuMd_avecLiensMd

@when("je souhaite récupérer le contenu de la page d'accueil")
def recuperer_accueil(echanges):
    echanges["contenu"] = lireLeMarkdown('home')

# CONTENU when

@when("je veux transformer ces liens md")
def transformer_liens_md(echanges):
    dirname = os.path.dirname(__file__)
    myConf = os.path.join(dirname, "../../Tests/Dataset/conf-mixte.yaml")
    recupererTouteLaConf(myConf)
    pattern = r'(?<=\]\().*?(?=\s|\))'
    changer = dict()
    changer['old'] = ".md"
    changer['new'] = ".html"
    echanges["contenuMd_avecLiensHtml"] = remplacerExtensionDansContenu(echanges["contenu"], pattern, changer)

@when("Je Récupère Les Fichiers")
def dataset_mixte_recuperer(echanges):
    recupererTouteLaConf(echanges['confFile'])
    echanges['contenuMd']= listerFichiersExtensionRepertoire()
    # print('liste md:', echanges['contenuMd'])

@when("Je Récupère Les Fichiers avec doublon")
def dataset_doublons_recuperer(echanges):
    """cas impossible si dossier unique : pas 2 fois le même fichier
    """
    recupererTouteLaConf(echanges['confFile'])
    echanges['listeMd'] = [
        Path(f'{here}/Dataset/Content-mixte/doublon.md'), 
        Path(f'{here}/Dataset/Content-mixte/doublon.md')
    ]

@then("le contenu correspond à celui du fichier indiqué en accueil")
def controler_contenu_accueil(echanges):
    assert "Page d'accueil du site" in echanges["contenu"]

 # CONTENU then

@then("je me retrouve avec des liens html")
def visualiser_liens_transformes_en_html(echanges):
    # print(echanges["contenuMd_avecLiensHtml"])
    assert echanges["contenuMd_avecLiensHtml"] == data.expected_contenuMd_avecLiensHtml

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

@then("j'ai une alerte concernant les doublons")
def alerte_doublon(echanges, capsys):
    creerReferentielPagesLiens(echanges["listeMd"])
    captured = capsys.readouterr()  # ASTUCE: capturer la sortie console
    expected_message = "avec doublon de nom"
    assert expected_message in captured.out

@then("Je Recois La Liste Des doublons avec un nom incrémenté")
def doublons_incrementes(echanges):
    listeComplete = creerReferentielPagesLiens(echanges["listeMd"])
    pprint.pprint(listeComplete)
    expected_doublon =  ('HOME',
                        'doublon 2',
                        'doublon_2.html',
                         Path('/home/user/Documents/marss/Tests/Dataset/Content-mixte/doublon.md')
    )
    assert listeComplete[1] == expected_doublon

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
    recupererTouteLaConf(myConf)  # acessible en global à l'application

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
             ],  # type: ignore
        'PROJET': [
            {'label': 'doser effort', 'url': 'PROJET-doser-effort.html'},
            {'label': 'etude opportunite',
             'url': 'PROJET-etude-opportunite.html'},
            {'label': 'fonctionnalites', 'url': 'PROJET-fonctionnalites.html'}
        ] }  # type: ignore
    else:
        echanges['referentiel'] = {'PROJET': [
            {'label': 'doser effort', 'url': 'PROJET-doser-effort.html'},
            {'label': 'etude opportunite',
             'url': 'PROJET-etude-opportunite.html'},
            {'label': 'fonctionnalites', 'url': 'PROJET-fonctionnalites.html'}
        ]  # type: ignore
        }

@given(parsers.parse("est finalisé {args}"))
def demander_menu_footer(echanges, args):
    print(args)
    if args == "le referentiel des pages":
        print("FIND")
        dirname = os.path.dirname(__file__)
        myConf = os.path.join(dirname, "../Dataset/conf-reference.yaml")
        conf = recupererTouteLaConf(myConf)
        echanges['conf'] = conf
        pprint.pprint(echanges)
        pprint.pprint(data.propre_pagesMarkdown)
        pprint.pprint(data.propre_listeAvecHtml)
        pprint.pprint(data.propre_listeLiens)
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
    recupererTouteLaConf(myConf)
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

@when("je souhaite récupérer le contenu html de la page d'accueil")
def recuperer_accueil_html(echanges):
    md_text = lireLeMarkdown('home')
    menu = "tout menu"  # peu importe, non lié à l'objectif de test
    footer = "pied de page"  # peu importe, non lié à l'objectif de test
    infos = ""  # evolution, mal interceptee, mal debuggee en erreur de test
    echanges["html_text"] = ajouterEtTransformerEnHtml(infos, md_text, "titre", "famille", menu, footer, "home", True)

@when("je souhaite récupérer le contenu html d'une page forçant le plan de page")
def recuperer_page_avec_menu(echanges):
    md_text = lireLeMarkdown('home')
    menu = "tout menu"  # peu importe, non lié à l'objectif de test
    footer = "pied de page"  # peu importe, non lié à l'objectif de test
    echanges["html_text"] = ajouterEtTransformerEnHtml(md_text, "titre", "famille", menu, footer, "home", False)
    # EVOL-lien-categorie

@when("on nettoie le dossier destination")
def demander_menu_footer(echanges):
    """nettoyer avec la conf : conf['outputPath']

    - prérequis : récupérer la conf en step avant
    """
    # n'est pas effectué ? est déjà propre sans rien
    # conf = echanges['conf']
    print(echanges['conf'])
    print("--------- nettoyage en cours -----")
    supprimerFichiersDuRepertoireHtml()
    pass

@when(parsers.parse("on dépose {args} dans le dossier"))
def demander_menu_footer(echanges, args):

    if args == "le dossier media":

        recreerDossierMediaDeplacerStyle()

    elif args == "le fichier html de chaque contenu":

        # pour changer extension hyperlien markdown
        pattern = r'(?<=\]\().*?(?=\s|\))'
        changer = dict()
        changer['old'] = ".md"
        changer['new'] = ".html"

        # entrants importants
        menuListe = data.propre_listeLiens
        referentiel = data.propre_listeAvecHtml

        for element in referentiel:
            famille = element[0]  # EVOL-lien-categorie
            fileName = element[2]
            title = element[1]
            filePath = element[3]
            md_text = lireLeMarkdown(filePath)
            md_text = remplacerExtensionDansContenu(md_text, pattern, changer)
            menuHtml = afficherMenu(menuListe, fileName)
            footer = afficherLiensFooter(menuListe, fileName)
            infos = ""  # evolution
            html = ajouterEtTransformerEnHtml(infos, md_text, title, famille, menuHtml, footer, "post")
            creerFichierHtml(fileName, html)
    else:
        pass

@when("je souhaite créer le fichier html de la page d'accueil")
def creer_accueil_html(echanges):
    """
    forcer le nom de la page
    """
    html = """
    <html>
    <head><title>accueil'</title></head>
    <body>accueil</body>
    </html>
    """
    fichier = echanges['conf']['outputPath'] + 'index.html'
    if os.path.isfile(fichier):
        os.remove(fichier)
    creerFichierHtml("index.html", html, False)

# HTML then

@then("je reçois une liste ordonnée par catégorie")
def liste_reordonnee(echanges):
    pprint.pprint(echanges)
    assert  echanges['listeHtml'][0][0] == echanges['listeHtml'][1][0]  
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
    # TODO: retirer duplication de code liens_html de variable jeu de données aussi
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

    pprint.pprint(echanges["menu_pages"])
    soup = BeautifulSoup(echanges["menu_pages"], features='html.parser')
    echanges['soup'] = soup
    content = soup.prettify()
    print("DEBUG:", content)
    categories = soup.find_all('a', attrs={"class": "diff"})  # span (avant)
    print("CAT:", categories)
    # le texte seul devient lien et nombre de post : impact du dev "compter posts par rubrique"
    assert len(categories) == expected_categories_nombre 
    categories_liste_nom = list()
    for nom in categories:
        categories_liste_nom.append(nom.contents[0])
        # equivalent de .get_text()
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

@then(parsers.parse("on a {args} présent dans le dossier"))
def presence_fichier_dossier(echanges, args, nettoyer):
    if args == "le style css du site":          
        file = os.path.exists(f'{here}/Dataset/WebSite-reference/media/style.css')
        assert file == True
        # nettoyer  # (f'{here}/Dataset/WebSite-reference')
    elif args == "chaque fichier html du contenu":
        expected_list = data.propre_pagesHtml
        inPath = echanges['conf']['inputPath']
        inExt = echanges['conf']['inputExtension']
        actual_list = sorted(Path(inPath).glob('**/*' + inExt))
        assert  actual_list == expected_list
        # nettoyer   # (f'{here}/Dataset/WebSite-reference')
    else:
        pass          
    # fixture executée qu'une fois

@then("j'ai le lien accueil actif")
def lien_accueil_actif(echanges):  
    assert '<a href="./" class="active">accueil</a>' in echanges["html_text"]

@then("j'ai le menu page actif")
def plan_page_actif(echanges):  
    assert '<input type="radio" id="tdm" name="menu" value="page" class="cache" checked>' in echanges["html_text"]

@then("le fichier créé s'appelle index.html")
def visualiser_fichier_accueil_html(echanges):
    fichier = echanges['conf']['outputPath'] + 'index.html'
    assert os.path.isfile(fichier)
    if os.path.isfile(fichier):
        os.remove(fichier)    

#--------------- PROGRAMME -----------

@given("le site est configuré et le contenu markdown est présent")
def prerequis():
    """
    Utiliser votre propre site ?
    totalement inutile à présent
    """
    pass

@when("je lance la génération du site")
def generer():
    os.system(f"python Code/ >/dev/null 2>&1 &")
    time.sleep(1)  # obligatoire 

@then("le site est accessible en serveur de debug")
def lancer():
    expected_status = 200

    try:       
        r = requests.get('http://127.0.0.1:8001/', timeout=10)
        actual_status = r.status_code
    except requests.exceptions.ReadTimeout as e:
        print("error:", e)

    assert actual_status == expected_status

    time.sleep(1) 
    os.system("kill -15 $(ps aux | grep '[p]ython Code' | awk -F \" \" '{printf $2}')")

@given(parsers.parse("ma liste comporte {nombre:d} posts"))
def liste_de_liens(echanges, nombre):
    print(nombre)
    if nombre == 3:
        data =  [{'label': 'premier', 'url': 'premier.html'}, 
            {'label': 'milieu', 'url': 'milieu.html'}, 
            {'label': 'dernier', 'url': 'dernier.html'}
            ]
    elif nombre == 2:
        data =  [{'label': 'premier', 'url': 'premier.html'}, 
            {'label': 'milieu', 'url': 'milieu.html'} 
            ]
    elif nombre == 1:
        data =  [{'label': 'premier', 'url': 'premier.html'}
            ]
    echanges["data"] = data
    pass

@when(parsers.parse("je suis au post {index}"))
def liste_de_liens(echanges, index):
    res_precedent, res_suivant = liensPrecedentSuivant(courant=index + ".html", liste=echanges["data"])
    echanges["precedent"] = res_precedent
    echanges["suivant"] = res_suivant

@then(parsers.parse("j'ai en post precedent {precedent}"))
def lien_precedent(echanges, precedent):
    if precedent == "aucun":
        assert  echanges["precedent"] ==  {}
    else:
        assert  echanges["precedent"]["label"] == precedent

@then(parsers.parse("j'ai en post suivant {suivant}"))
def lien_suivant(echanges, suivant):
    if suivant == "aucun":
        assert  echanges["suivant"] ==  {}
    else:
        assert  echanges["suivant"]["label"] == suivant

@when(parsers.parse("j'affiche le post {index}"))
def liste_de_liens(echanges, index):
    res_precedent, res_suivant = liensPrecedentSuivant(courant=index + ".html", liste=echanges["data"])
    echanges["html"] = afficherInfosPost(res_precedent, res_suivant)
    print("HTML infosPost:", echanges["html"])

@then(parsers.parse("j'ai ce résultat {affichage}"))
def affichage_liens_suivant_precedent(echanges, affichage):
    if affichage != "aucun":
        assert  echanges["html"] ==  affichage
    else:
        assert  echanges["html"] == ""

@when("j'affiche les posts de la catégorie")
def affichage_posts_categorie(echanges):
    res = afficherPostsDeCategorie(echanges["data"])
    print(res)
    echanges["res"] = res
    pass

@then("j'ai mes liens pour chaque post")
def liens_posts_categorie(echanges):
    # etre fin et  robuste, compter nombre de li et de a
    soup = BeautifulSoup(echanges["res"], features='html.parser')
    liste = soup.find_all("li")
    liens = soup.find_all("a")
    assert len(liste) == 3
    assert len(liens) == 3
    # test exact très fragile
    liste_de_posts = '<ol class="">\n<li><a href="premier.html" class="">premier</a></li>\n<li><a href="milieu.html" class="">milieu</a></li>\n<li><a href="dernier.html" class="">dernier</a></li>\n</ol>\n'
    # ne doit pas etre """..."""
    assert  echanges["res"]  == liste_de_posts

@given("le répertoire de destination n'est pas vide")
def dossier_non_vide(echanges):
    print(echanges['conf']['outputPath'])    
    fichier = echanges['conf']['outputPath'] + "new.html" 
    with open(fichier, "w+") as f:
        f.write("non vide")
    assert os.path.exists(fichier)  # contrôle vs test
    assert len(os.listdir(echanges['conf']['outputPath'])) == 2
    # bien isoler des autres tests
    # .keep seul fichier avant

@then("le dossier de destination est vide")
def dossier_vide(echanges):
    assert len(os.listdir(echanges['conf']['outputPath'])) == 1
    # .keep seul fichier