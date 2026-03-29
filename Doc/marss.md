Module marss
============

Functions
---------

`recupererCmdLine(myConf=None)`
:   recuperer arguments console
    - configuration yaml
    - serveur en fond, stop, down -> goto with exit

`recupererTouteLaConf(myConf)`
:   point de depart de tout
    permet de tout deporter pour portabilite
    mis en global pour la lib : contrainte de taille method(arg) pour PEP8

`listerFichiersExtensionRepertoire()`
:   recuperer la liste des fichiers .md
    aurait pu etre moins generique
    nom plus metier : recupererListeMarkup

`creerReferentielPagesLiens(mdFiles)`
:   Referentiel propre :
    objectif : eviter des nettoyages rendondants effectues par fonction
    solution : zip des listes : (category, label, page, url)
    note : + nettoyage si path windows pose probleme ?

`creerLiensMenu(referentiel)`
:   sortie de liste de dict par group
    result['BUG'] = [{'label':'BUG 0001 le win..','url':'winpath.html'}]
    dépendance : pas de conf

`afficherMenu(liens, vousEtesIci)`
:   menu html de plan de site
    Tracabilite: test_afficherMenu

`afficherLiensFooter(liens, vousEtesIci)`
:   liste à plat de liens légaux et autres
    Beaucoup (trop ?) de duplication de code
    peut être null, sans lien

`lireLeMarkdown(file)`
:   recuperation du contenu .md
    besoin du path reel vers md :
    garder la liste originelle : listerFichiersExtensionRepertoire = ROBUSTESSE
    OU se fier au referentiel enrichi

`remplacerExtensionDansContenu(content, pattern, changer)`
:   remplacer une extension trouvee dans un pattern
    - remplacer par exemple l'hyperlien markdown [](.md) par .html
    - retourner le contenu avec le remplacement effectue

`ajouterEtTransformerEnHtml(md_text, title, menu, footer, typeDePage, menuVisible=False)`
:   sortie html enrichie
    en plus du contenu, ajout du titre et des menus page et site

`creerFichierHtml(fileName, html, post=True)`
:   ecriture des fichiers html
    REMANIER filename est fourni par autre source
    ENLEVER inputExtension, outputExtension

`supprimerFichiersDuRepertoireHtml()`
:   nettoyage du site statique
    RISQUE: avoir tout supprime sans pouvoir rien recreer
    verifier faisabilite de la creation avant

`recreerDossierMediaDeplacerStyle()`
:   " recuperation de la feuille de style

`lancerServeurDebug()`
: