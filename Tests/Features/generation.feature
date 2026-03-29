
Feature: Générer le site statique
    Opérations de :
    - récupération
    - transformation
    - enrichissement
    - présentation
    - publication

    @nominal
    Scenario: récupérer la configuration interne
        Given Je Ne Précise Pas La Configuration 
        When je récupère la configuration
        Then Je Recois La Configuration par défaut

    @alternatif
    Scenario: récupérer la configuration externe
        Given Je Précise La Configuration
        When je récupère la configuration
        Then Je Recois La Configuration Personnalisée 

    @erreur
    Scenario: récupérer la configuration avec erreur de chemin
        Given j'indique une configuration inexistante
        When Je récupère la configuration inexistante
        Then Je reçois une erreur de chemin

    @erreur
    Scenario: récupérer la configuration avec erreur de format
        Given J'ai une configuration mal formatée
        When Je récupère la configuration mal formatée
        Then Je reçois une erreur de format
    
    @robustesse
    Scenario: récupérer le contenu
        Given Le Contenu A Des Fichiers Markdown Parmi D'autres Extensions
        When Je Récupère Les Fichiers
        Then Je Recois La Liste Des Fichiers Markdown
        Then Les Fichiers D'autres Extensions Sont Absents

    @nominal
    Scenario: récupérer les fichiers markdown présents en contenu
        Given le contenu n'a que du markdown
        When Je Récupère Les Fichiers
        Then Je Recois La Liste Des Fichiers Markdown Exclusivement
    
    @nominal
    Scenario: récupérer les fichiers html, labels et catégories
        Given la liste des markdowns propre est prête
        When je demande cette liste en lien html avec catégorie
        Then je reçois une liste ordonnée par catégorie
        Then j'ai un label pour chaque lien
        Then chaque lien est vers un fichier html
        Then le fichier source md est consigné

    @robustesse
    Scenario: récupérer des fichiers html, parfois incomplets
        Given la liste des markdowns parfois sans préfixe est prête
        When je demande cette liste en lien html avec catégorie
        Then j'ai une catégorie par défaut pour une page sans préfixe

    @nominal
    Scenario: récupérer les liens de toutes les pages
        Given le référentiel complet des pages est disponible
        When je demande la liste finale des liens
        Then j'ai une liste de libellé url

    @nominal
    Scenario: afficher le menu du site
        Given la liste de libellé url
        When je demande le menu des pages
        Then j'ai une liste par catégorie
        Then j'ai toutes les pages dans les bonnes catégories

    Scenario: afficher les liens du footer
        Given le préfixe footer est <presence_configuration> en configuration
        Given les pages correspondant au préfixe footer sont <presence_page>
        When je demande le menu footer
        Then j'ai le menu footer <presence_menu> en pied de page

        @nominal
        Examples: présenter les liens en footer
          | presence_configuration | presence_page | presence_menu |
          | present                |    presentes  |    present    |

        @robustesse
        Examples: ne pas présenter les liens en footer
          | presence_configuration   | presence_page | presence_menu |
          | absent                   |    absentes   |    absent     |
          | present                  |    absentes   |    absent     |


    Scenario: disposer de tous les fichiers du site statique
        Given est finalisé "le referentiel des pages"
        Given est finalisé "chaque menu"
        Given est finalisé "chaque contenu html"
        When on nettoie le dossier destination
        When on dépose "le dossier media" dans le dossier
        When on dépose "le fichier html de chaque contenu" dans le dossier
        Then on a "le style css du site" présent dans le dossier
        Then on a "chaque fichier html du contenu" présent dans le dossier
