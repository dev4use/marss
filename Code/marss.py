#!/usr/bin/env python
# -*- coding: utf-8 -*-
# version : Standard
"""fonctions procedurales du site statique

- partir d'un ensemble de fichiers .md pour aboutir a un ensemble de fichiers html navigables
- ordre d'exposition respectant la cinematique de transformation et d'enrichissement de la donnee
"""

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
import pprint
import contextlib


def recupererCmdLine(myConf=None):  # pragma: no cover
    """recuperer les arguments en console

    configuration yaml
    plus tard : serveur en fond, up et down ?
    """
    parser = argparse.ArgumentParser()  # sys.argv[1:]
    parser.add_argument("-V", "--version", help="version", action="store_true")
    parser.add_argument("-C", "--configuration", help="path de configuration")
    args = parser.parse_args()

    if args.version:
        print("MARSS : gardez vos idées sur terre")  # en plus de __version__
    if args.configuration:  # FIX long args
        print("emplacement specifique de la configuration : " + args.configuration)
        if os.path.isfile(args.configuration) is True:
            print("configuration bien trouvee")
            myConf = args.configuration  # CONF en argument
        else:
            print("--- configuration non trouvee ---")
            exit(1)
    return myConf


def recupererTouteLaConf(myConf):
    """point de depart de tout, recuperer la conf

    - portabilite de la configuration avec fichier deporte
    - mis en global pour la lib
    - en profite pour supprimer le fichier de log à cette etape
    """
    extension = str(myConf).lower().endswith(('.yml', '.yaml'))
    fichier = Path(myConf).is_file()
    # fichier = True
    print("le chemin du fichier de configuration est:", myConf)
    print("la ressource a la bonne extension:", extension)
    print("la ressource est bien un fichier:", fichier)
    if extension and fichier:  # and contenu
        with open(myConf) as f:
            try:
                global conf
                conf = yaml.load(f, Loader=yaml.FullLoader)
                with contextlib.suppress(FileNotFoundError):
                    os.remove(conf['logs'])
                return conf
            except Exception as e:
                print('erreur fichier mal formate')
                print(e)
                exit(2)
    else:
        print('erreur fichier de configuration')
        exit(1)


def aideLoggerFichier(etape, donnees):
    """visualiser les formats d'echange a chaque etape

    - refentiels logges en mode "pretty"
    """
    pp = pprint.PrettyPrinter(indent=4, width=100)
    donnees = pp.pformat(donnees)
    with open(conf['logs'], mode="a+", encoding='UTF-8') as f:
        sep = "" if Path(conf['logs']).stat().st_size == 0 else "\n"
        # gestion de premiere ligne ci dessus
        f.write(f"{sep}---------------- {etape} ----------------\n")
        f.write(donnees)
        # f.write(str(donnees))
        # # pp.pprint(donnees) argument must be str, not None
        # argument must be str, not None
        # pp.pprint(donnees, stream=f)


def listerFichiersExtensionRepertoire():
    """recuperer la liste des fichiers .md

    - aurait pu etre moins generique
    - nom plus metier DDD : recupererListeMarkup
    - entrants : fichiers d'un repertoire
    - sortants : [ Path('/home/marss/Content/BUG-040-nom-categorie-dans-lien-post.md'), ...]
    """
    inPath = conf['inputPath']
    inExt = conf['inputExtension']
    myList = sorted(Path(inPath).glob('**/*' + inExt))  # FIX-0005
    return myList


def creerReferentielPagesLiens(mdFiles):
    """referentiel propre

    - objectif : eviter des nettoyages rendondants effectues par fonction
    - solution : zip des listes : (category, label, page, url)
    - note : + nettoyage si path windows pose probleme
    - entrants : [Path('/home/marss/Content/BUG-040-nom-categorie-dans-lien-post.md'), ...]
    - sortants : [('BUG', '040 nom categorie dans lien post',
    'BUG-040-nom-categorie-dans-lien-post.html',
    Path('/home/marss/Content/BUG-040-nom-categorie-dans-lien-post.md')), ('EB', ...)]
    """
    inExt = conf['inputExtension']
    outExt = conf['outputExtension']
    category = []
    label = []
    page = []
    url = mdFiles
    global compteur
    compteur = 1

    for f in mdFiles:
        if platform.system() == "Windows":   # pragma: no cover
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
            print("--- WARNING : fichier " + str(f) + " sans prefixe ---")
            category.append('HOME')
            # TODO: sur de vouloir cat par defaut ?
            categorie = 'HOME'  # FIX-020

        unLabel = str(unFichierMd).replace("_", " ").replace("-", " ")  # - sep
        unLabel = unLabel.replace(inExt, "")  # - extension
        unLabel = unLabel.replace(categorie, "")  # FIX-020
        unLabel = unLabel.strip()  # FIX-BUG-050 enlever espace devant

        if unLabel in label:  # FIX-0006
            DOUBLON = True
            compteur += 1
            print("--- WARNING : fichier " + str(f) + " avec doublon de nom ---")
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
    """sortie de liste de dict par group

    - entrants : [('BUG', '040 nom categorie dans lien post',
     'BUG-040-nom-categorie-dans-lien-post.html',
      Path('/home/marss/Content/BUG-040-nom-categorie-dans-lien-post.md')), ('EB', ...)]
    - sortants : {'BUG': [{'label': '040 nom categorie dans lien post',
     'url': 'BUG-040-nom-categorie-dans-lien-post.html'}, ... ], 'EB': [...]}
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
    """menu html de plan de site

    - liste au format ul/li de l'ensemble des pages
    - style : ul class = postCategorie / span title / li class active si post en cours
    - EVOL : deportee dasn une fonction dediee un peu dupliquee
    """
    inFooter = conf['footerLiens']
    menu = ''
    for k, v in liens.items():
        if k != inFooter:  # EVOL footer
            nombrePostsCategorie = str(len(v))
            menu += '<ul class="postCategorie" id=' + k + '>'
            menu += '<span title=' + k + '>'
            menu += '<a class="diff" href="' + k + '.html">' + k + '</a> (' + nombrePostsCategorie + ')</span>\n'
            for e in v:
                if vousEtesIci == e['url']:
                    menu += '<li><a href="' + e['url'] + '" class="active">' + e['label'] + '</a></li>\n'
                else:
                    menu += '<li><a href="' + e['url'] + '">' + e['label'] + '</a></li>\n'
            menu += '</ul>\n'
    return menu


def afficherLiensFooter(liens, vousEtesIci):
    """liste a plat de liens legaux et autres

    - beaucoup (trop ?) de duplication de code
    - le retour peut etre null, sans lien
    - style : ul class = postFooter /  li class active si post en cours
    """
    inFooter = conf['footerLiens']
    menu = ''
    for k, v in liens.items():
        if k == inFooter:  # EVOL footer
            menu += '<ul class="postFooter">\n'
            for e in v:
                if vousEtesIci == e['url']:
                    menu += '<li><a href="' + e['url'] + '" class="active">' + e['label'] + '</a></li>\n'
                else:
                    menu += '<li><a href="' + e['url'] + '">' + e['label'] + '</a></li>\n'
            menu += '</ul>\n'
    return menu


def afficherPostsDeCategorie(liens):
    menu = ''
    menu += '<ol class="">\n'
    for e in liens:
        menu += '<li><a href="' + e['url'] + '" class="">' + e['label'] + '</a></li>\n'
        # tuple indices must be integers or slices, not str
    menu += '</ol>\n'
    return menu


def lireLeMarkdown(file):
    """recuperation du contenu .md

    - besoin du path reel vers md
    """
    if file == 'home':
        file = conf['home']
    f = open(file, "r")
    md_text = f.read()
    return md_text


def remplacerExtensionDansContenu(content, pattern, changer):
    """remplacer une extension trouvee dans un pattern

    - remplacer par exemple l'hyperlien markdown [](.md) par .html
    - retourner le contenu avec le remplacement effectue
    - le  nom la aussi aurait pu etre plus métier DDD
    """
    # liste a remplacer
    aRemplacer = re.findall(pattern, content)
    # liste remplacee
    enRemplacement = list()
    for el in aRemplacer:
        el = el.replace(changer['old'], changer['new'])
        list.append(enRemplacement, el)
    # dictionnaire avec cle/valeur de type aRemplacer/enRemplacement
    aFaire = dict(zip(aRemplacer, enRemplacement))
    # application du traitement
    resultat = reduce(lambda a, kv: a.replace(*kv), aFaire.items(), content)

    return resultat


def liensPrecedentSuivant(courant="", liste=""):
    """presenter les liens de post : precedent suivant

    - intercepter le contexte : post courant, categorie courante, type de page
    - cibler le contexte : posts de la categorie
    - sortie : dictionnaires vides ou avec clés url label pour precedent et suivant
    """
    array = liste
    place = [courant == i['url'] for i in array].index(True)
    size = len(array)
    dernier = size-1
    precedent = dict()
    suivant = dict()
    # precedent = "..."
    # suivant = "..."
    if size >= 3:
        precedent['url'] = array[place-1]['url']
        precedent['label'] = array[place-1]['label']
        if place != dernier:
            suivant['url'] = array[place+1]['url']  # erreur si dernier
            suivant['label'] = array[place+1]['label']
        else:
            suivant['url'] = array[0]['url']  # aller au premier
            suivant['label'] = array[0]['label']
    elif size == 2:
        if place != dernier:
            suivant['url'] = array[place+1]['url']  # erreur si dernier
            suivant['label'] = array[place+1]['label']
        else:
            precedent['url'] = array[place-1]['url']
            precedent['label'] = array[place-1]['label']
    else:
        pass
    return precedent, suivant


def afficherInfosPost(precedent, suivant):
    """afficher des informations liees au post

    - lien precedent suivant
    - date de modification et temps de lecture (bientôt)
    """
    html = ""
    html += f"< <a href=\"{precedent['url']}\">{precedent['label']}</a> |"
    html += " ... "
    html += f"| <a href=\"{suivant['url']}\">{suivant['label']}</a> >"
    return html


def ajouterEtTransformerEnHtml(infos, md_text, title, famille, menu, footer, typeDePage, menuVisible=False):
    """sortie html enrichie

    - en plus du contenu, ajout du titre et des menus page et site
    """
    # FIX-023 - typeDePage apportera support pour multiple template
    # AM-002 + pouvoir forcer desactiver (comme en accueil)
    version = conf['version']
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
        pass

    # pourrait etre realisé à part, et ici, assemblage
    md = markdown.Markdown(extensions=['toc', 'fenced_code'])  # Majuscule obligee FIX-0012
    content = md.convert(md_text)
    toc = md.toc  # anticipation externalisation

    html = '<html><head><title>' + title + '</title>'
    html += '<meta http-equiv="Content-type" content="text/html;'
    html += 'charset=utf-8" />'
    html += '<link rel="stylesheet" href="/media/style.css" media="all">'
    html += '</head><body class="markdown-body">\n'  # EVOL-css-markdown class="markdown-body"

    if typeDePage == "home":
        html += '<a href="./" class="active">accueil</a>'  # AM-001  header
    elif famille == conf['footerLiens'] or typeDePage == "categorie":  # exclure categorie footer
        html += '<a href="./" class="">accueil</a>'
    else:
        html += '<a href="./">accueil</a> > <a class="diff" href="' + famille + '.html">' + famille + '</a>'
        # EVOL-lien-categorie
        # EVOL-page-categorie "categorie" lien comme home,
        # contenu : title_conf, presentation_conf, liens : 1 rubrique, liens avec saut de ligne

    html += '<input type="radio" id="men" name="menu"'
    html += f' value="site" class="cache" {statusSite}>'  # AM-002
    html += '<label for="men">Menu du site</label>'

    html += '<input type="radio" id="tdm" name="menu"'
    html += f' value="page" class="cache" {statusPage}>'  # AM-002
    html += '<label for="tdm">Menu de la page</label>'

    html += '<input type="radio" id="rien" name="menu"'
    html += ' value="fermer" class="cache">'
    html += '<label for="rien">(FERMER MENU)</label>\n'  # header

    html += '<div class="menu">' + menu + '</div></header>\n'  # nav
    # html += toc + '\n<article>' + content + '</article>\n'
    html += toc + '\n<article>'
    if typeDePage == "post" and famille != conf['footerLiens']:
        html += infos
    html += content
    if typeDePage == "post" and famille != conf['footerLiens']:
        html += infos
    html += '</article>\n'
    html += '<footer></footer>' \
            '<div id="finish"><p class="infos">généré depuis ' \
            '<a href="https://github.com/dev4use/marss" class="trademark">Marss ' \
            f'{version}</a> </p>'
    # html += ' #  BOF fonction imbriquee
    html += footer + '</div>'  # TODO: liens FOOTER conf
    html += '</body></html>'  # FIX-0004
    return html


def creerFichierHtml(fileName, html, post=True):  # AM-
    """ecriture des fichiers html

    - TODO: REMANIER filename est fourni par autre source
    - TODO: ENLEVER inputExtension, outputExtension
    """
    outPath = conf['outputPath']
    inExt = conf['inputExtension']  # inutile en generation index
    outExt = conf['outputExtension']  # inutile en generation index
    fOutput = outPath + str(fileName)  # FIX Linux
    if post:
        fOutput = fOutput.replace(inExt, outExt)  # pas en generation index
    print('creation de ', fOutput)  # pour info en console
    z = open(fOutput, "w")
    z.write(html)
    z.close()


def supprimerFichiersDuRepertoireHtml():
    """nettoyage du site statique

    - RISQUE: avoir tout supprime sans pouvoir rien recree
    - verifier faisabilite de la creation avant ?
    """
    outPath = conf['outputPath']
    print(f"---- nettoyage du dossier site {outPath} -----")
    files = glob.glob(outPath + '*')  # pour eviter /media/
    print("-> pages trouvees :", files)
    for f in files:
        if path.isfile(f):
            print('suppression de', f)
            os.remove(f)
    shutil.rmtree(os.path.join(outPath, 'media'), ignore_errors=True)


def recreerDossierMediaDeplacerStyle():
    """recuperation de la feuille de style
    """
    outPath = conf['outputPath']
    fichierCss = conf['style']  # TODO pouvoir en parser plusieurs ?
    os.mkdir(outPath + 'media')  # FIX Linux
    shutil.copy(fichierCss, outPath + 'media/style.css')  # TODO pas en dur


def lancerServeurDebug():  # pragma: no cover
    """lancement du serveur de debug

    - ouverture optionnelle (par conf) du navigateur
    """
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
