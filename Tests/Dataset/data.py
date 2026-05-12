from pathlib import Path


version_actuelle = "ST-2.0.0"  # peu d'intérêt à ce test si ce n'est s'assurer que tests à jour

# referentiel propre
propre_pagesMarkdown = [ Path('/home/user/Documents/marss/Tests/Dataset/Content-reference/DEV-kiss.md'),
        Path('/home/user/Documents/marss/Tests/Dataset/Content-reference/DEV-langage-et-langue.md'),
        Path('/home/user/Documents/marss/Tests/Dataset/Content-reference/FOOTER-a-propos.md')
]
propre_listeAvecHtml = [('DEV','kiss','DEV-kiss.html', Path('/home/user/Documents/marss/Tests/Dataset/Content-reference/DEV-kiss.md')),
                ('DEV','langage et langue','DEV-langage-et-langue.html', Path('/home/user/Documents/marss/Tests/Dataset/Content-reference/DEV-langage-et-langue.md')),
                ('FOOTER','a propos','FOOTER-a-propos.html', Path('/home/user/Documents/marss/Tests/Dataset/Content-reference/FOOTER-a-propos.md'))
]  # referentiel pour generation
propre_listeLiens = {'BUG':[{'label': 'kiss','url': 'DEV-kiss.html'},
                            {'label': 'langage et langue','url': 'DEV-langage-et-langue.html'}],
                    'FOOTER':[{'label': 'a propos','url': 'FOOTER-a-propos.html'}]
}
propre_pagesHtml = [Path('/home/user/Documents/marss/Tests/Dataset/Content-reference/DEV-kiss.md'),
                 Path('/home/user/Documents/marss/Tests/Dataset/Content-reference/DEV-langage-et-langue.md'),
                 Path('/home/user/Documents/marss/Tests/Dataset/Content-reference/FOOTER-a-propos.md')
]  # pour controle attendu

contenuMd_avecLiensMd = """
# Titre

Ceci est un paragraphe   
- [lien 1](url-1.md) ici

Et encore [là](web-2.md)
"""
expected_contenuMd_avecLiensHtml = """
# Titre

Ceci est un paragraphe   
- [lien 1](url-1.html) ici

Et encore [là](web-2.html)
"""

contenuMd_avecTitres= """
# Titre

Edito

## Sous titre 1

Paragraphe 1

## Sous titre 2

Paragraphe 2
"""