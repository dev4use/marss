# Test Report (PASSED)

**Generated**: 2026-05-12 18:28:02

## Summary
- **Total Tests**: 34
- **Passed**: 34
- **Failed**: 0
- **Skipped**: 0
- **Total Duration**: 3.17s

## Test Results

---

### Feature: Générer le site statique
- **File**: `generation.feature`




#### [PASS] Scenario: récupérer la configuration interne
- **Status**: PASSED
- **Duration**: 0.03s


**Steps:**

1. [PASS] **Given** Je Ne Précise Pas La Configuration (0.00s)

2. [PASS] **When** je récupère la configuration (0.01s)

3. [PASS] **Then** Je Recois La Configuration par défaut (0.00s)




#### [PASS] Scenario: récupérer la configuration externe
- **Status**: PASSED
- **Duration**: 0.02s


**Steps:**

1. [PASS] **Given** Je Précise La Configuration (0.00s)

2. [PASS] **When** je récupère la configuration (0.01s)

3. [PASS] **Then** Je Recois La Configuration Personnalisée (0.00s)




#### [PASS] Scenario: récupérer la configuration avec erreur de chemin
- **Status**: PASSED
- **Duration**: 0.01s


**Steps:**

1. [PASS] **Given** j'indique une configuration inexistante (0.00s)

2. [PASS] **When** Je récupère la configuration inexistante (0.00s)

3. [PASS] **Then** Je reçois une erreur de chemin (0.00s)




#### [PASS] Scenario: récupérer la configuration avec erreur de format
- **Status**: PASSED
- **Duration**: 0.02s


**Steps:**

1. [PASS] **Given** J'ai une configuration mal formatée (0.00s)

2. [PASS] **When** Je récupère la configuration mal formatée (0.00s)

3. [PASS] **Then** Je reçois une erreur de format (0.00s)




#### [PASS] Scenario: logger les événements
- **Status**: PASSED
- **Duration**: 0.02s


**Steps:**

1. [PASS] **Given** j'ai un fichier de log configuré (0.01s)

2. [PASS] **When** je veux logger un événement (0.00s)

3. [PASS] **Then** je vois apparaître l'événement en log (0.00s)




#### [PASS] Scenario: récupérer le contenu
- **Status**: PASSED
- **Duration**: 0.02s


**Steps:**

1. [PASS] **Given** Le Contenu A Des Fichiers Markdown Parmi D'autres Extensions (0.00s)

2. [PASS] **When** Je Récupère Les Fichiers (0.01s)

3. [PASS] **Then** Je Recois La Liste Des Fichiers Markdown (0.00s)

4. [PASS] **Then** Les Fichiers D'autres Extensions Sont Absents (0.00s)




#### [PASS] Scenario: récupérer les fichiers markdown présents en contenu
- **Status**: PASSED
- **Duration**: 0.02s


**Steps:**

1. [PASS] **Given** le contenu n'a que du markdown (0.00s)

2. [PASS] **When** Je Récupère Les Fichiers (0.01s)

3. [PASS] **Then** Je Recois La Liste Des Fichiers Markdown Exclusivement (0.00s)




#### [PASS] Scenario: récupérer des fichiers markdown en doublon
- **Status**: PASSED
- **Duration**: 0.02s


**Steps:**

1. [PASS] **Given** le contenu a des fichiers au nom identique (0.00s)

2. [PASS] **When** Je Récupère Les Fichiers avec doublon (0.00s)

3. [PASS] **Then** j'ai une alerte concernant les doublons (0.00s)

4. [PASS] **Then** Je Recois La Liste Des doublons avec un nom incrémenté (0.00s)




#### [PASS] Scenario: récupérer les fichiers html, labels et catégories
- **Status**: PASSED
- **Duration**: 0.03s


**Steps:**

1. [PASS] **Given** la liste des markdowns propre est prête (0.01s)

2. [PASS] **When** je demande cette liste en lien html avec catégorie (0.00s)

3. [PASS] **Then** je reçois une liste ordonnée par catégorie (0.00s)

4. [PASS] **Then** j'ai un label pour chaque lien (0.00s)

5. [PASS] **Then** chaque lien est vers un fichier html (0.00s)

6. [PASS] **Then** le fichier source md est consigné (0.00s)




#### [PASS] Scenario: récupérer des fichiers html, parfois incomplets
- **Status**: PASSED
- **Duration**: 0.02s


**Steps:**

1. [PASS] **Given** la liste des markdowns parfois sans préfixe est prête (0.00s)

2. [PASS] **When** je demande cette liste en lien html avec catégorie (0.00s)

3. [PASS] **Then** j'ai une catégorie par défaut pour une page sans préfixe (0.00s)




#### [PASS] Scenario: transformer les liens md
- **Status**: PASSED
- **Duration**: 0.02s


**Steps:**

1. [PASS] **Given** j'ai des contenus md avec lien md (0.00s)

2. [PASS] **When** je veux transformer ces liens md (0.01s)

3. [PASS] **Then** je me retrouve avec des liens html (0.00s)




#### [PASS] Scenario: transformer le chemin image
- **Status**: PASSED
- **Duration**: 0.02s


**Steps:**

1. [PASS] **Given** j'ai des images en contenu md (0.00s)

2. [PASS] **When** je veux transformer ces chemins (0.00s)

3. [PASS] **Then** je me retrouve avec des chemins modifiés (0.00s)




#### [PASS] Scenario: récupérer le contenu md de la page d'accueil
- **Status**: PASSED
- **Duration**: 0.03s


**Steps:**

1. [PASS] **Given** la page d'accueil est en configuration (0.02s)

2. [PASS] **When** je souhaite récupérer le contenu de la page d'accueil (0.00s)

3. [PASS] **Then** le contenu correspond à celui du fichier indiqué en accueil (0.00s)




#### [PASS] Scenario: récupérer le contenu html de la page d'accueil
- **Status**: PASSED
- **Duration**: 0.10s


**Steps:**

1. [PASS] **Given** la page d'accueil est en configuration (0.01s)

2. [PASS] **When** je souhaite récupérer le contenu html de la page d'accueil (0.08s)

3. [PASS] **Then** j'ai le lien accueil actif (0.00s)




#### [PASS] Scenario: créer le fichier html de l'accueil
- **Status**: PASSED
- **Duration**: 0.02s


**Steps:**

1. [PASS] **Given** la page d'accueil est en configuration (0.01s)

2. [PASS] **When** je souhaite créer le fichier html de la page d'accueil (0.00s)

3. [PASS] **Then** le fichier créé s'appelle index.html (0.00s)




#### [PASS] Scenario: récupérer le html d'une page avec menu page actif
- **Status**: PASSED
- **Duration**: 0.02s


**Steps:**

1. [PASS] **Given** le menu de page est en configuration (0.01s)

2. [PASS] **When** je souhaite récupérer le contenu html d'une page forçant le plan de page (0.00s)

3. [PASS] **Then** j'ai le menu page actif (0.00s)




#### [PASS] Scenario: récupérer les liens de toutes les pages
- **Status**: PASSED
- **Duration**: 0.02s


**Steps:**

1. [PASS] **Given** le référentiel complet des pages est disponible (0.00s)

2. [PASS] **When** je demande la liste finale des liens (0.00s)

3. [PASS] **Then** j'ai une liste de libellé url (0.00s)




#### [PASS] Scenario: afficher le menu du site
- **Status**: PASSED
- **Duration**: 0.03s


**Steps:**

1. [PASS] **Given** la liste de libellé url (0.00s)

2. [PASS] **When** je demande le menu des pages (0.01s)

3. [PASS] **Then** j'ai une liste par catégorie (0.01s)

4. [PASS] **Then** j'ai toutes les pages dans les bonnes catégories (0.01s)




#### [PASS] Scenario: identifier les liens des posts précédent et suivant
- **Status**: PASSED
- **Duration**: 0.02s


**Steps:**

1. [PASS] **Given** ma liste comporte 3 posts (0.00s)

2. [PASS] **When** je suis au post milieu (0.00s)

3. [PASS] **Then** j'ai en post precedent premier (0.00s)

4. [PASS] **Then** j'ai en post suivant dernier (0.00s)




#### [PASS] Scenario: identifier les liens des posts précédent et suivant
- **Status**: PASSED
- **Duration**: 0.02s


**Steps:**

1. [PASS] **Given** ma liste comporte 3 posts (0.00s)

2. [PASS] **When** je suis au post dernier (0.00s)

3. [PASS] **Then** j'ai en post precedent milieu (0.00s)

4. [PASS] **Then** j'ai en post suivant premier (0.00s)




#### [PASS] Scenario: identifier les liens des posts précédent et suivant
- **Status**: PASSED
- **Duration**: 0.02s


**Steps:**

1. [PASS] **Given** ma liste comporte 3 posts (0.00s)

2. [PASS] **When** je suis au post premier (0.00s)

3. [PASS] **Then** j'ai en post precedent dernier (0.00s)

4. [PASS] **Then** j'ai en post suivant milieu (0.00s)




#### [PASS] Scenario: identifier les liens des posts précédent et suivant
- **Status**: PASSED
- **Duration**: 0.02s


**Steps:**

1. [PASS] **Given** ma liste comporte 2 posts (0.00s)

2. [PASS] **When** je suis au post milieu (0.00s)

3. [PASS] **Then** j'ai en post precedent premier (0.00s)

4. [PASS] **Then** j'ai en post suivant aucun (0.00s)




#### [PASS] Scenario: identifier les liens des posts précédent et suivant
- **Status**: PASSED
- **Duration**: 0.02s


**Steps:**

1. [PASS] **Given** ma liste comporte 2 posts (0.00s)

2. [PASS] **When** je suis au post premier (0.00s)

3. [PASS] **Then** j'ai en post precedent aucun (0.00s)

4. [PASS] **Then** j'ai en post suivant milieu (0.00s)




#### [PASS] Scenario: identifier les liens des posts précédent et suivant
- **Status**: PASSED
- **Duration**: 0.02s


**Steps:**

1. [PASS] **Given** ma liste comporte 1 posts (0.00s)

2. [PASS] **When** je suis au post premier (0.00s)

3. [PASS] **Then** j'ai en post precedent aucun (0.00s)

4. [PASS] **Then** j'ai en post suivant aucun (0.00s)




#### [PASS] Scenario: récupérer les infos du markdown
- **Status**: PASSED
- **Duration**: 0.02s


**Steps:**

1. [PASS] **Given** mon fichier comporte 200 mots (0.00s)

2. [PASS] **When** je récupère les informations du fichier (0.00s)

3. [PASS] **Then** j'ai la date de modification du fichier (0.00s)

4. [PASS] **Then** j'ai le nombre de mots du fichier (0.00s)

5. [PASS] **Then** j'ai le temps de lecture du fichier (0.00s)




#### [PASS] Scenario: afficher les liens des posts précédent et suivant
- **Status**: PASSED
- **Duration**: 0.01s


**Steps:**

1. [PASS] **Given** ma liste comporte 3 posts (0.00s)

2. [PASS] **When** j'affiche le post milieu (0.00s)

3. [PASS] **Then** j'ai ce résultat < <a href="premier.html">premier</a> | 1920-12-01 - 0 min (150 mots) | <a href="dernier.html">dernier</a> > (0.00s)




#### [PASS] Scenario: afficher les liens des posts précédent et suivant
- **Status**: PASSED
- **Duration**: 0.01s


**Steps:**

1. [PASS] **Given** ma liste comporte 1 posts (0.00s)

2. [PASS] **When** j'affiche le post premier (0.00s)

3. [PASS] **Then** j'ai ce résultat aucun (0.00s)




#### [PASS] Scenario: afficher les posts d'une catégorie
- **Status**: PASSED
- **Duration**: 0.03s


**Steps:**

1. [PASS] **Given** ma liste comporte 3 posts (0.00s)

2. [PASS] **When** j'affiche les posts de la catégorie (0.01s)

3. [PASS] **Then** j'ai mes liens pour chaque post (0.00s)

4. [PASS] **Then** j'ai mon extrait pour chaque post (0.00s)




#### [PASS] Scenario: afficher les liens du footer
- **Status**: PASSED
- **Duration**: 0.02s


**Steps:**

1. [PASS] **Given** le préfixe footer est present en configuration (0.00s)

2. [PASS] **Given** les pages correspondant au préfixe footer sont presentes (0.00s)

3. [PASS] **When** je demande le menu footer (0.01s)

4. [PASS] **Then** j'ai le menu footer present en pied de page (0.00s)




#### [PASS] Scenario: afficher les liens du footer
- **Status**: PASSED
- **Duration**: 0.02s


**Steps:**

1. [PASS] **Given** le préfixe footer est absent en configuration (0.00s)

2. [PASS] **Given** les pages correspondant au préfixe footer sont absentes (0.00s)

3. [PASS] **When** je demande le menu footer (0.00s)

4. [PASS] **Then** j'ai le menu footer absent en pied de page (0.00s)




#### [PASS] Scenario: afficher les liens du footer
- **Status**: PASSED
- **Duration**: 0.02s


**Steps:**

1. [PASS] **Given** le préfixe footer est present en configuration (0.00s)

2. [PASS] **Given** les pages correspondant au préfixe footer sont absentes (0.00s)

3. [PASS] **When** je demande le menu footer (0.01s)

4. [PASS] **Then** j'ai le menu footer absent en pied de page (0.00s)




#### [PASS] Scenario: preparer le dossier de destination
- **Status**: PASSED
- **Duration**: 0.02s


**Steps:**

1. [PASS] **Given** le répertoire destination est connu (0.01s)

2. [PASS] **Given** le répertoire de destination n'est pas vide (0.00s)

3. [PASS] **When** on nettoie le dossier destination (0.00s)

4. [PASS] **Then** le dossier de destination est vide (0.00s)




#### [PASS] Scenario: disposer de tous les fichiers du site statique
- **Status**: PASSED
- **Duration**: 0.06s


**Steps:**

1. [PASS] **Given** est finalisé le referentiel des pages (0.02s)

2. [PASS] **Given** est finalisé chaque menu (0.00s)

3. [PASS] **Given** est finalisé chaque contenu html (0.00s)

4. [PASS] **When** on nettoie le dossier destination (0.00s)

5. [PASS] **When** on dépose le dossier media dans le dossier (0.00s)

6. [PASS] **When** on dépose le dossier image dans le dossier (0.00s)

7. [PASS] **When** on dépose le fichier html de chaque contenu dans le dossier (0.01s)

8. [PASS] **Then** on a le style css du site présent dans le dossier (0.00s)

9. [PASS] **Then** on a le dossier image présent dans le dossier (0.00s)

10. [PASS] **Then** on a chaque fichier html du contenu présent dans le dossier (0.00s)




#### [PASS] Scenario: visualiser le site statique
- **Status**: PASSED
- **Duration**: 2.06s


**Steps:**

1. [PASS] **Given** le site est configuré et le contenu markdown est présent (0.00s)

2. [PASS] **When** je lance la génération du site (1.00s)

3. [PASS] **Then** le site est accessible en serveur de debug (1.04s)

