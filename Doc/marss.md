Module marss
============
fonctions procedurales du site statique

- partir d'un ensemble de fichiers .md pour aboutir a un ensemble de fichiers html navigables
- ordre d'exposition respectant la cinematique de transformation et d'enrichissement de la donnee

Functions
---------

`recupererCmdLine(myConf=None)`
:   recuperer les arguments en console
    
    configuration yaml
    plus tard : serveur en fond, up et down ?

`recupererTouteLaConf(myConf)`
:   point de depart de tout, recuperer la conf
    
    - portabilite de la configuration avec fichier deporte
    - mis en global pour la lib
    - en profite pour supprimer le fichier de log à cette etape

`aideLoggerFichier(etape, donnees)`
:   visualiser les formats d'echange a chaque etape
    
    - refentiels logges en mode "pretty"

`listerFichiersExtensionRepertoire()`
:   recuperer la liste des fichiers .md
    
    - aurait pu etre moins generique
    - nom plus metier DDD : recupererListeMarkup
    - entrants : fichiers d'un repertoire
    - sortants : [ Path('/home/marss/Content/BUG-040-nom-categorie-dans-lien-post.md'), ...]

`creerReferentielPagesLiens(mdFiles)`
:   referentiel propre
    
    - objectif : eviter des nettoyages rendondants effectues par fonction
    - solution : zip des listes : (category, label, page, url)
    - note : + nettoyage si path windows pose probleme
    - entrants : [Path('/home/marss/Content/BUG-040-nom-categorie-dans-lien-post.md'), ...]
    - sortants : [('BUG', '040 nom categorie dans lien post',
    'BUG-040-nom-categorie-dans-lien-post.html',
    Path('/home/marss/Content/BUG-040-nom-categorie-dans-lien-post.md')), ('EB', ...)]

`creerLiensMenu(referentiel)`
:   sortie de liste de dict par group
    
    - entrants : [('BUG', '040 nom categorie dans lien post',
     'BUG-040-nom-categorie-dans-lien-post.html',
      Path('/home/marss/Content/BUG-040-nom-categorie-dans-lien-post.md')), ('EB', ...)]
    - sortants : {'BUG': [{'label': '040 nom categorie dans lien post',
     'url': 'BUG-040-nom-categorie-dans-lien-post.html'}, ... ], 'EB': [...]}

`afficherMenu(liens, vousEtesIci)`
:   menu html de plan de site
    
    - liste au format ul/li de l'ensemble des pages
    - style : ul class = postCategorie / span title / li class active si post en cours

`afficherLiensFooter(liens, vousEtesIci)`
:   liste a plat de liens legaux et autres
    
    - beaucoup (trop ?) de duplication de code
    - le retour peut etre null, sans lien
    - style : ul class = postFooter /  li class active si post en cours

`lireLeMarkdown(file)`
:   recuperation du contenu .md
    
    - besoin du path reel vers md

`remplacerExtensionDansContenu(content, pattern, changer)`
:   remplacer une extension trouvee dans un pattern
    
    - remplacer par exemple l'hyperlien markdown [](.md) par .html
    - retourner le contenu avec le remplacement effectue
    - le  nom la aussi aurait pu etre plus métier DDD

`ajouterEtTransformerEnHtml(md_text, title, menu, footer, typeDePage, menuVisible=False)`
:   sortie html enrichie
    
    - en plus du contenu, ajout du titre et des menus page et site

`creerFichierHtml(fileName, html, post=True)`
:   ecriture des fichiers html
    
    - TODO: REMANIER filename est fourni par autre source
    - TODO: ENLEVER inputExtension, outputExtension

`supprimerFichiersDuRepertoireHtml()`
:   nettoyage du site statique
    
    - RISQUE: avoir tout supprime sans pouvoir rien recree
    - verifier faisabilite de la creation avant ?

`recreerDossierMediaDeplacerStyle()`
:   recuperation de la feuille de style

`lancerServeurDebug()`
:   lancement du serveur de debug
    
    - ouverture optionnelle (par conf) du navigateur