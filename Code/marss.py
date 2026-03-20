#!/usr/bin/env python
# -*- coding: utf-8 -*-
# version : Standard : ST-0.0.0

import markdown
import yaml
from pathlib import Path
import http.server
import webbrowser
import os
from os import path
import glob
from operator import itemgetter
from itertools import groupby
import re
from functools import reduce
import shutil
import argparse
import platform


def recupererCmdLine(myConf=None):  # sys.argv[1:]
    """ recuperer arguments console
    - configuration yaml
    - serveur en fond, stop, down -> goto with exit
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-V", "--version", help="version", action="store_true")
    parser.add_argument("-C", "--configuration", help="path de configuration")
    args = parser.parse_args()

    if args.version:
        print("MARSS : gardez vos idées sur terre")  # en plus de __version__
    if args.configuration:  # FIX long args
        print("emplacement specifique de la configuration : "+args.configuration)
        if os.path.isfile(args.configuration) is True:
            print("configuration bien trouvee")
            myConf = args.configuration  # CONF en argument
        else:
            print("--- configuration non trouvee ---")
            exit(1)
    return myConf


def recupererTouteLaConf(myConf):
    """ point de depart de tout
    permet de tout deporter pour portabilite
    mis en global pour la lib : contrainte de taille method(arg) pour PEP8
    """
    extension = str(myConf).lower().endswith(('.yml', '.yaml'))
    fichier = Path(myConf).is_file()
    # contenu = isinstance(myConf, dict)
    # if Path(myConf).is_file(): INITIAL
    if extension and fichier: #  and contenu
        # print('OK')
        #exit(0)
        with open(myConf) as f:
            try:
                global conf
                conf = yaml.load(f, Loader=yaml.FullLoader) #  PYTEST yaml.scanner.ScannerError
                return conf
            except Exception as e:
                print('erreur fichier mal formate')  # KO avant au load ! (texte, variable)
                print(e)
                exit(1)
    else:
        print('erreur fichier de configuration')
        exit(1)


def listerFichiersExtensionRepertoire():
    """ recuperer la liste des fichiers .md
    aurait pu etre moins generique
    nom plus metier : recupererListeMarkup
    """
    global conf
    inPath = conf['inputPath']
    inExt = conf['inputExtension']
    myList = sorted(Path(inPath).glob('**/*'+inExt))  # FIX-0005
    return myList


def creerReferentielPagesLiens(mdFiles):
    """ Referentiel propre :
    objectif : eviter des nettoyages rendondants effectues par fonction
    solution : zip des listes : (category, label, page, url)
    note : + nettoyage si path windows pose probleme ?
    """
    global conf
    inExt = conf['inputExtension']
    outExt = conf['outputExtension']
    category = []
    label = []
    page = []
    url = mdFiles
    global compteur
    compteur = 1

    for f in mdFiles:
        if platform.system() == "Windows":
            unFichierMd = str(str(f).split('\\')[-1])
        else:
            unFichierMd = str(str(f).split('/')[-1])  # FIX-008

        categorie = ""
        # FIX-020 : 3e position mis en 2e et ajout de "categorie"
        pattern = re.compile("-")  # fichiers sans prefixe
        if pattern.search(str(unFichierMd)):
            unPrefixe = str(str(unFichierMd).split('-')[0])  # FIX-0007
            # TODO: categorie seulement si aussi uppercase
            category.append(unPrefixe)
            categorie = unPrefixe  # FIX-020
        else:
            print("--- WARNING : fichier "+str(f)+" sans prefixe ---")
            # exit()
            category.append('HOME')
            # TODO: sur de vouloir cat par defaut ?
            categorie = 'HOME'  # FIX-020

        unLabel = str(unFichierMd).replace("_", " ").replace("-", " ")  # - sep
        unLabel = unLabel.replace(inExt, "")  # - extension
        unLabel = unLabel.replace(categorie, "")  # FIX-020

        if unLabel in label:  # FIX-0006
            DOUBLON = True
            compteur += 1
            print("--- WARNING : fichier "+str(f)+" avec doublon de nom ---")
            label.append(unLabel + " " + str(compteur))
        else:
            DOUBLON = False
            label.append(unLabel)

        if DOUBLON is True:  # FIX-0006
            outExt = "_" + str(compteur) + "" + outExt

        unFichierHtml = str(unFichierMd).replace(inExt, outExt)
        page.append(unFichierHtml)
    referentiel = zip(category, label, page, url)
    referentiel = sorted(referentiel, key=itemgetter(0))
    return referentiel


def creerLiensMenu(referentiel):
    """ sortie de liste de dict par group
    result['BUG'] = [{'label':'BUG 0001 le win..','url':'winpath.html'}]
    """
    result = {}
    for key, group in groupby(referentiel, lambda x: x[0]):
        liens = []
        for element in group:  # sur d'y etre
            descriptif = {}
            descriptif['label'] = element[1]
            # TODO: enlever 1er mot en uppercase ici ou avant
            descriptif['url'] = element[2]
            liens.append(descriptif)  # element[1]
        result[key] = liens  # 'test'
    return result


def afficherMenu(liens, vousEtesIci):  # FIX-023 
    """ menu html de plan de site
    Tracabilite: test_afficherMenu
    """
    global conf
    inFooter = conf['footerLiens']
    menu = ''
    for k, v in liens.items():
        if k != inFooter:  # EVOL footer
            #  print(k+" : ul de début de rubrique")
            menu += '<ul class="postCategorie"><span>'+k+'</span>\n'
            for e in v:
                #  print("url : "+e['url']+" et label "+e['label'])
                if vousEtesIci == e['url']:
                    menu += '<li><a href="'+e['url']+'" class="active">'+e['label']+'</a></li>\n'
                else:
                    menu += '<li><a href="'+e['url']+'">'+e['label']+'</a></li>\n'
            #  print(k+" : ul de fin de rubrique")
            menu += '</ul>\n'
    return menu


def afficherLiensFooter(liens, vousEtesIci):
    """ liste à plat de liens légaux et autres
    Beaucoup (trop ?) de duplication de code
    peu être null
    """
    global conf
    inFooter = conf['footerLiens']
    menu = ''
    for k, v in liens.items():
        if k == inFooter:  # EVOL footer
            #  print(k+" : ul de début de rubrique")
            menu += '<ul class="postFooter">\n'
            for e in v:
                #  print("url : "+e['url']+" et label "+e['label'])
                if vousEtesIci == e['url']:
                    menu += '<li><a href="'+e['url']+'" class="active">'+e['label']+'</a></li>\n'
                else:
                    menu += '<li><a href="'+e['url']+'">'+e['label']+'</a></li>\n'
            #  print(k+" : ul de fin de rubrique")
            menu += '</ul>\n'
    return menu


def recupererNomDeFichier(file):
    """ fichier sans path
    DEJA fait par referentiel : creerReferentielPagesLiens
    """
    fileName = str(str(file).split('\\')[-1])
    return fileName


def recupererTitreDeFichier(fileName):
    """ label et titre de fichier
    DEJA fait par referentiel : creerReferentielPagesLiens
    """
    global conf
    inExt = conf['inputExtension']
    fileName = str(fileName).replace("_", " ").replace("-", " ")  # - sep
    fileName = fileName.replace(inExt, "")  # - ext
    return fileName


def lireLeMarkdown(file):
    """ recuperation du contenu .md
    besoin du path reel vers md :
    garder la liste originelle : listerFichiersExtensionRepertoire = ROBUSTESSE
    OU se fier au referentiel enrichi
    """
    if file == 'home':
        global conf
        file = conf['home']
    f = open(file, "r")
    md_text = f.read()  # BUG-orangelabs-02
    return md_text


def remplacerExtensionDansContenu(content, pattern, changer):
    """ remplacer une extension trouvee dans un pattern
    - remplacer par exemple l'hyperlien markdown [](.md) par .html
    - retourner le contenu avec le remplacement effectue
    """
    # liste a remplacer
    aRemplacer = re.findall(pattern, content)
    # liste remplacee
    enRemplacement = list()
    for el in aRemplacer:
        el = el.replace(changer['old'],changer['new'])
        list.append(enRemplacement, el)
    # dictionnaire avec cle/valeur de type aRemplacer/enRemplacement
    aFaire = dict(zip(aRemplacer, enRemplacement))
    # application du traitement
    resultat = reduce(lambda a, kv: a.replace(*kv), aFaire.items(), content)

    return resultat


def ajouterEtTransformerEnHtml(md_text, title, menu, footer, typeDePage, menuVisible=False): 
    """ sortie html enrichie
    en plus du contenu, ajout du titre et des menus page et site
    """
    # FIX-023 - typeDePage apportera support pour multiple template
    # AM-002 + pouvoir forcer desactiver (comme en accueil)
    global conf
    if menuVisible:
        menuVisible = ""
    else:
        menuVisible = conf['menuVisible']
    statusSite = ""
    statusPage = ""
    if menuVisible == "site":
        statusSite = "checked"
    elif menuVisible == "page":
        statusPage = "checked"
    else:
        pass;
 
    md = markdown.Markdown(extensions=['toc','fenced_code'])  # Majuscule obligee FIX-0012
    content = md.convert(md_text)
 
    html = '<html><head><title>'+title+'</title>'
    html += '<meta http-equiv="Content-type" content="text/html;'
    html += 'charset=utf-8" />'
    html += '<link rel="stylesheet" href="/media/style.css" media="all">'
    html += '</head><body class="markdown-body">\n'  # EVOL-css-markdown class="markdown-body"

    if typeDePage == "home":
        html += '<a href="./" class="active">accueil</a>'  # AM-001  header
    else:
        html += '<a href="./">accueil</a>'  # header

    html += '<input type="radio" id="men" name="menu"'
    html += f' value="site" class="cache" {statusSite}>'  # AM-002 
    html += '<label for="men">Menu du site</label>'

    html += '<input type="radio" id="tdm" name="menu"'
    html += f' value="page" class="cache" {statusPage}>'  # AM-002 
    html += '<label for="tdm">Menu de la page</label>'

    html += '<input type="radio" id="rien" name="menu"'
    html += ' value="fermer" class="cache">'
    html += '<label for="rien">(FERMER MENU)</label>\n' # header

    html += '<div class="menu">'+menu+'</div></header>\n'  # nav
    html += md.toc+'\n<article>'+content+'</article>\n'
    html += '<footer></footer><div id="finish"><p class="infos">généré depuis <a href="https://github.com/dev4use/marss" class="trademark">Marss</a></p>'
    # html += ' #  BOF fonction imbriquee
    html += footer + '</div>'  # TODO: liens FOOTER conf
    html += '</body></html>'  # FIX-0004
    return html


def creerFichierHtml(fileName, html, post=True):  # AM-
    """ ecriture des fichiers html
    REMANIER filename est fourni par autre source
    ENLEVER inputExtension, outputExtension
    """
    global conf
    outPath = conf['outputPath']
    inExt = conf['inputExtension']  # inutile en generation index
    outExt = conf['outputExtension'] # inutile en generation index
    fOutput = outPath + str(fileName)  # FIX Linux
    if post:
        fOutput = fOutput.replace(inExt, outExt) # pas en generation index
    print('creation de '+fOutput)  # pour info en console
    z = open(fOutput, "w")
    z.write(html)
    z.close()


def supprimerFichiersDuRepertoireHtml():
    """ nettoyage du site statique
    RISQUE: avoir tout supprime sans pouvoir rien recreer
    verifier faisabilite de la creation avant
    """
    global conf
    outPath = conf['outputPath']
    files = glob.glob(outPath+'*')  # pour eviter /media/
    for f in files:
        if path.isfile(f):
            print('suppression de '+f)
            os.remove(f)
    shutil.rmtree(os.path.join(outPath, 'media'), ignore_errors=True)


def recreerDossierMediaDeplacerStyle():
    """" recuperation de la feuille de style
    """
    global conf
    outPath = conf['outputPath']
    fichierCss = conf['style']  # TODO pouvoir en parser plusieurs ?
    os.mkdir(outPath + 'media')  # FIX Linux
    shutil.copy(fichierCss, outPath + 'media/style.css')  # TODO pas en dur


def lancerServeurDebug():
    global conf
    outPath = conf['outputPath']
    # host = conf['host']
    port = conf['port']
    browser = conf['openBrowser']
    server_address = ("", port)
    url = f"127.0.0.1:{port}"

    server = http.server.HTTPServer
    handler = http.server.CGIHTTPRequestHandler

    web_dir = outPath
    os.chdir(web_dir)
    handler.cgi_directories = ["./"]
    print("Serveur actif sur le port :", port)

    httpd = server(server_address, handler)
    if browser:        
        webbrowser.open(url)
    httpd.serve_forever()
