#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""version : STANDARD
lanceur du programme
logique apparente dedans, avec boucle par fichier
"""

import os
import marss


def main():

    myConf = marss.recupererCmdLine()  # sys.argv[1:]
    if myConf is None:  # CONF fixe
        dirname = os.path.dirname(__file__)  # FIX
        print('configuration fixe')
        myConf = os.path.join(dirname, "../Conf/conf.yaml")
    conf = marss.recupererTouteLaConf(myConf)  # TODO: controler yaml
    # BUG-042 : assigner variable à conf

    mdFiles = marss.listerFichiersExtensionRepertoire()
    referentiel = marss.creerReferentielPagesLiens(mdFiles)
    menuListe = marss.creerLiensMenu(referentiel)  # + extraitDeMarkdown(texte) ?
    marss.aideLoggerFichier("sous menu", menuListe['EB'])
    # menuHtml = marss.afficherMenu(menuListe)  # FIX-023 page active VousEtesIci
    marss.aideLoggerFichier("listeMarkdown", mdFiles)
    marss.aideLoggerFichier("listeAvecHtml", referentiel)
    marss.aideLoggerFichier("listeLiens", menuListe)
    marss.supprimerFichiersDuRepertoireHtml()
    marss.recreerDossierMediaDeplacerStyle()  # BUG-
    marss.deplacerDossierMedia()

    # pour changer extension hyperlien markdown
    pattern = r'(?<=\]\().*?(?=\s|\))'
    changer = dict()
    changer['old'] = ".md"
    changer['new'] = ".html"
    changer['contenu'] = "(../Media"
    changer['site'] = "(Media"

    inFooter = conf['footerLiens']

    for element in referentiel:
        famille = element[0]  # EVOL-lien-categorie
        fileName = element[2]
        title = element[1]
        filePath = element[3]
        md_text = marss.lireLeMarkdown(filePath)
        md_text = marss.remplacerExtensionDansContenu(md_text, pattern, changer)
        md_text = marss.remplacerPathMedia(md_text, changer)
        menuHtml = marss.afficherMenu(menuListe, fileName)
        footer = marss.afficherLiensFooter(menuListe, fileName)
        precedent, suivant = marss.liensPrecedentSuivant(liste=menuListe[famille], courant=fileName)
        if famille != inFooter:
            dateModification = marss.dateMiseAjour(filePath)
            tailleFichier = marss.nombreDeMots(md_text)
            tempsFichier = marss.tempsDeLecture(tailleFichier)
            infos = marss.afficherInfosPost(precedent, suivant, dateModification, tailleFichier, tempsFichier)
        else:
            infos = ""
        html = marss.ajouterEtTransformerEnHtml(infos, md_text, title, famille, menuHtml, footer, "post")
        marss.creerFichierHtml(fileName, html)

    for element in menuListe:  # EVOL-page-categorie
        if element != inFooter:
            marss.aideLoggerFichier("générer une page par rubrique", element)
            if element not in conf['familles']:
                print("a faire :", f"ajouter la categorie {element} en configuration")
                titre = conf['familles']['default']['titre'] + " " + element
                description = conf['familles']['default']['description'] + " " + element
                title = element
            else:
                titre = conf['familles'][element]['titre']
                description = conf['familles'][element]['description']
                title = conf['familles'][element]['titre']
            md_text = f"<h1>Catégorie :  {element}</h1>"  # bug si en md supprime ol
            md_text += "<p>" + titre + "</p>"
            md_text += "<p>" + description + "</p>"
            marss.aideLoggerFichier(f"sous menu dynamique pour : {element}", menuListe[element])
            menuCat = marss.afficherPostsDeCategorie(menuListe[element], referentiel)  # EVOL
            footer = marss.afficherLiensFooter(menuListe, "index.html")
            famille = ""  # EVOL-lien-categorie
            infos = ""
            html = marss.ajouterEtTransformerEnHtml(infos,
                                                    md_text
                                                    + menuCat,
                                                    title, famille, menuCat, footer, "categorie", True)
            # ci dessus, par True, forcer desactivation menu en accueil
            marss.creerFichierHtml(element + ".html", html, False)

    md_text = marss.lireLeMarkdown('home')
    title = conf['projet']  # BUG-042
    menuHtml = marss.afficherMenu(menuListe, "index.html")
    footer = marss.afficherLiensFooter(menuListe, "index.html")
    famille = ""  # EVOL-lien-categorie
    infos = ""
    html = marss.ajouterEtTransformerEnHtml(infos,
                                            md_text
                                            + "<div class='plan'>"
                                            + menuHtml + "</div>",
                                            title, famille, menuHtml, footer, "home", True)
    # ci dessus, par True, forcer desactivation menu en accueil
    marss.creerFichierHtml("index.html", html, False)

    marss.lancerServeurDebug()


# pragma: exclude file
if __name__ == "__main__":
    main()
