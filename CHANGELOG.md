# ChangeLog

Suivi des changements de version par classement antéchronologique.

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


### Changements

### Correctifs

### Supression

