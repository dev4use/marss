# ChangeLog

Suivi des changements de version par classement antéchronologique.

## ST-1.0.0 - 2026-04-11

### Ajouts

1. **légalité** : dossier de test automatique
1. **code** : contrôles de la taille du code avec pygount
1. code : contrôles des normes de codage avec flake8
1. code : génération de la documentation de code avec pdoc3
1. **test** : tests automatiques en BDD Gherkin avec pytest-bdd
1. test : test du contenu html avec BeautifulSoup bs4
1. test : contrôle de couverture du code par les tests
1. test : rapports de qualité en doc
1. test:  badges de qualité en readme principal
1. **debug**: en dossier "Logs", suivi des étapes d'enrichissement des inventaires de page

### Suppressions

1. code : retrait de code mort dans marss.py

### Changements

1. code : module/package Code avec __init__ et __main__

## ST-0.2.0 - 2026-03-22

Version plus conforme d'un  point de vue légal et ergonomique.

### Ajouts

1. **légalité** : footer avec les mentions légales ou d'autres pages repérées par un préfixe choisi en configuration
1. légalité : la licence OpenSource est dans le dépôt de code source
1. **navigation** : le lien de la page en cours se distingue des autres liens 
1. **code** : le numéro de version de l'applicatif est en footer et géré par configuration

### Correctifs

1. **design** : menus site et page plus aérés, moins collés au header du site

### Bugs

1. Voir le BUG-048 sur le site de démonstration : tilde markdown de texte barré non supporté
1. Voir le BUG-049 sur le site de démonstration : liste numérotée de niveau 2 en chiffres romains (préférence pour chiffres arabes)

## ST-0.1.0 - 2026-03-17

Version intiale de l'applicatif.

### Ajouts

1. **contenu** : fichier markdown avec pour recommandation un préfixe en majuscule (majuscule non obligatoire)
2. contenu : attribution d'une catégorie unique au post en se basant sur le préfixe majuscule
1. contenu : attribution d'une catégorie par défaut en cas d'absence de préfixe et avertissement en console
1. contenu : contenu markdown recherché dans un dossier unique
1. **design** : présentation épurée de type markdown avec effet mono page
2. **navigation** : accès au plan de site sur chaque page
3. navigation : accès au plan de page sur chaque page
4. navigation : gestion en configuration de l'affichage des plans par défaut à l'arrivée sur une page : site, page, rien
5. navigation : masquer/afficher le plan de navigation sur chaque page
6. navigation : transformation html d'un lien initial markdown vers une source .md interne
1. **template** : générateur de menu directement dans le module
1. template : générateur de page directement dans le menu
1. template : mécanique particulière pour gérer l'accueil à partir d'un fichier txt
1. **code** : module en fonctions sans classes mais avec documentation
1. code : lanceur appelant explicitement et chronologiquement chaque fonction pour faciliter la compréhension et le debug
1. code : écrit et documenté en français et orienté "métier" (Domain Driven Development like)
1. **site** : site statique délivré dans un dossier dédié avec son média css
1. site : site lancé par un serveur de debug sur le navigateur par défaut



