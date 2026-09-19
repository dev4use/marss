# ChangeLog

Suivi des changements de version par classement antéchronologique.   
Puisqu'il s'agit de la version PR pour PREMIUM,   
les fonctionnalités supplémentaires de la version STANDARD sont explicitées.  

## PR-0.1.0 - 2026-09-26

Version intiale de l'applicatif.

### Ajouts

1. **site** : publication automatique du site sur Git :
   - Le site web  statique final du dossier "WebSite" est directement délivré dans un autre dossier de votre ordinateur.
   - Ce dossier peut pointer sur un autre dépôt, par exemple un dépôt de type GithubPages.
   - Une fois dans le dossier, Git le pousse par exemple dans votre dépôt GithubPages "<pseudo|org>.github.io" où la mise à jour est automatiquement publiée sur le web.
   - Exemple pour [le site de développment de Marss](https://github.com/dev4use/dev4use.github.io)
   - Le dossier "Content" est également copié afin de garder les documents initiaux avant enrichissement html.
   - Le dossier Content n'est pas publié sur le web puisque ce dossier a juste vocation d'être archivé.
   - Pour utiliser la foncionnalité en console : ```python WebServer```
