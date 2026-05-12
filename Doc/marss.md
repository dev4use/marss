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
    - EVOL : deportee dasn une fonction dediee un peu dupliquee

`afficherLiensFooter(liens, vousEtesIci)`
:   liste a plat de liens legaux et autres
    
    - beaucoup (trop ?) de duplication de code
    - le retour peut etre null, sans lien
    - style : ul class = postFooter /  li class active si post en cours

`helper_fichierCorrespondance(ref, search)`
:   recuperer le path du fichier md
    
    - search : avec le nom de fichier html
    - ref : le referentiel des pages pour correspondance
    - retrouver le path du fichier md : position 4 du tuple ci dessous
    (   'BUG',
        '040 nom categorie dans lien post',
        'BUG-040-nom-categorie-dans-lien-post.html',
         PosixPath('/home/user/Documents/marss/Content/BUG-040-nom-categorie-dans-lien-post.md')

`lireLeMarkdown(file)`
:   recuperation du contenu .md
    
    - besoin du path reel vers md

`extraitDeMarkdown(texte)`
:   recuperation d'un extrait du chapo sous h1
    
    - prérequis : h1, h2, contenu sous h1
    - entrant : texte markdown
    - sortant : texte avec [...] si tronque

`remplacerExtensionDansContenu(content, pattern, changer)`
:   remplacer une extension trouvee dans un pattern
    
    - remplacer par exemple l'hyperlien markdown [](.md) par .html
    - retourner le contenu avec le remplacement effectue
    - le  nom la aussi aurait pu etre plus métier DDD

`remplacerPathMedia(content, changer)`
:   Remplacer le lien vers les medias images
    
    - Dans content, est "../Media"
    - Dans WebSite, est "Media"

`afficherPostsDeCategorie(liens, referentiel)`
:   afficher les posts par catégorie
    
    - fonction de type integration : appelle d'autres fonctions

`liensPrecedentSuivant(courant='', liste='')`
:   presenter les liens de post : precedent suivant
    
    - intercepter le contexte : post courant, categorie courante, type de page
    - cibler le contexte : posts de la categorie
    - sortie : dictionnaires vides ou avec clés url label pour precedent et suivant

`dateMiseAjour(pathFichier)`
:   date de mise a jour du fichier markdown
    
    - entrant : chemin PathLib du fichier markdown
    - sortant : date formattee

`nombreDeMots(text)`
:   compter le nombre de mots, hors balises markdown
    
    - depuis : https://github.com/gandreadis/markdown-word-count/blob/master/mwc/counter.py

`tempsDeLecture(totalDeMots)`
:   estimer le temps de lecture
    
    - entrant : nombre de mots en integer
    - sortant : temps avec unite de temps

`afficherInfosPost(precedent, suivant, modif, mots, temps)`
:   afficher des informations liees au post
    
    - lien precedent suivant
    - date de modification et temps de lecture (bientôt)

`ajouterEtTransformerEnHtml(infos, md_text, title, famille, menu, footer, typeDePage, menuVisible=False)`
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

`deplacerDossierMedia()`
:   recuperation des images

`lancerServeurDebug()`
:   lancement du serveur de debug
    
    - ouverture optionnelle (par conf) du navigateur