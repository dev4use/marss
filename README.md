# MARSS (MAR-kdown S-imple web-S-ite)

*Slogan : Pour garder vos idées sur terre*

Clin d'oeil à la conquête spatiale.  
Jouer à se donner de grandes ambitions, mais trop grandes, avec deux S dans le nom.  
Parce qu'il existe tant de générateur de site statique, et que cela peut sembler si fantastique, alors que...  
Cela peut être fait en peu de lignes de code (du moins au départ), et beaucoup de dérision et de pédagogie.   

- Contenu markdown.
- Code en python.
- Exposition html d'un site statique.


## Comment installer l'application

Pré-requis :
- python sur l'environnement de travail (voire un environnement virtuel python),
- un installateur de paquet ou gestionnaire de dépendance tel que pip,
- console de commande shell (plutot de type linux, comme git bach dans windows).

Depuis la racine du projet, en ligne de commande :
```
# installer les paquets

pip install -r requirements.txt
```

## Comment utiliser l'application


1. Dans le dossier **Content**, gérer le contenu sous forme de fichiers markdown avec ```l'extension .md``` puisque c'est un site statique de transformation de markdown en html. 
1. Dans le dossier **Conf**, un fichier yaml permet de gérer la configuration de manière explicite.
1. Pour la version STANDARD de l'applicatif qui est non intrusive en méta données, ajouter au nom de fichier```le préfixe en majuscule < PREF- >```qui permet de déterminer la catégorie unique d'appartenance du billet.
1. Pour publier ou prévisualiser le contenu, ouvrir la console depuis le dossier du dépôt Git.
    ```
    # A la racine du 'repository' (et dans l'environnement virtuel ?) taper

    python Code/app.py

    # Visualiser les informations de débuggage en console
    # Le navigateur par défaut s'ouvre avec le site statique.

    # Ne fermer ou arrêter la console que pour arrêter le serveur

    CTRL + C
    ```
1. Pour publier ailleurs le site statique, dans ce premier niveau de la version STANDARD,  
l'utilisateur est libre de ses actions.
1. Pour avoir un aperçu du résultat, [consulter la démonstration en ligne](https://dev4use.github.io/)

## Comment vérifier la qualité de l'application

Pour vérifier la qualité de l'application, certains tests qualité sont lancés et les résultats sont dans [la documentation](Doc).  

- Taille du code et proportions de commentaires.
- Rapport de violation des normes de codage.
- Documentation du code source.

Pour lancer les analyses et rapports :

```
# A la racine du repository

pdoc --config sort_identifiers=False --force --html --output-dir Doc/ Code/marss.py \
& pdoc --config sort_identifiers=False --force --output-dir=Doc/ Code/marss.py \
& pygount Code/marss.py --format=json | python -m json.tool > Doc/code-marss-$(date '+%Y%m%d').json \
& flake8 --max-line-length=121 --max-doc-length=99 --format=pylint --ignore=W503 --statistics --output-file=Doc/qualite-marss-$(date '+%Y%m%d').txt Code/
```

## Comment tester l'application

L'application utilise le format de description Gherkin BDD pour les tests.  
Il est ainsi possible de voir et comprendre le comportement du système.  
Le comportement du système est retracé à travers [les features en BDD](Tests/Features/).  
Pour lancer les tests :

```
# A la racine du repository

python -m pytest Tests
```

