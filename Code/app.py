#!/usr/bin/env python
# -*- coding: utf-8 -*-
# version : LIGT : listing html en listing de repertoire

import os
import marss
from pathlib import Path # Debug

if __name__ == "__main__":

    # print("execution du programme marss version "+marss.__version__)
    # FIX linux : a reprendre lorsque passera en package

    myConf = marss.recupererCmdLine()  # sys.argv[1:]
    if myConf is None:  # CONF fixe
        dirname = os.path.dirname(__file__)  # FIX
        print('configuration fixe')
        myConf = os.path.join(dirname, "../Conf/conf.yaml")
    conf = marss.recupererTouteLaConf(myConf)  # TODO: controler yaml
    # BUG-042 : assigner variable à conf

    mdFiles = marss.listerFichiersExtensionRepertoire()
    referentiel = marss.creerReferentielPagesLiens(mdFiles)
    menuListe = marss.creerLiensMenu(referentiel)
    # menuHtml = marss.afficherMenu(menuListe)  # FIX-023 page active WIP ; ousEtesIci

    marss.supprimerFichiersDuRepertoireHtml()
    marss.recreerDossierMediaDeplacerStyle()  # BUG-

    # pour changer extension hyperlien markdown
    pattern = r'(?<=\]\().*?(?=\s|\))'
    changer = dict()
    changer['old'] = ".md"
    changer['new'] = ".html"

    for element in referentiel:
        fileName = element[2]
        title = element[1]
        filePath = element[3]
        md_text = marss.lireLeMarkdown(filePath)
        md_text = marss.remplacerExtensionDansContenu(md_text, pattern, changer)
        menuHtml = marss.afficherMenu(menuListe, fileName)
        footer = marss.afficherLiensFooter(menuListe, fileName)
        html = marss.ajouterEtTransformerEnHtml(md_text, title, menuHtml, footer, "post")
        marss.creerFichierHtml(fileName, html)

    md_text = marss.lireLeMarkdown('home')
    title =  conf['projet']  # BUG-042
    menuHtml = marss.afficherMenu(menuListe, "index.html") 
    footer = marss.afficherLiensFooter(menuListe, "index.html")
    html = marss.ajouterEtTransformerEnHtml(md_text+"<div class='plan'>"+menuHtml+"</div>", title, menuHtml, footer, "home", True)
    # ci dessus, par True, forcer desactivation menu en accueil
    marss.creerFichierHtml("index.html", html, False)

    marss.lancerServeurDebug()
