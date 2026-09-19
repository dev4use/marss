import sys
import os
# depuis Sandbox OK
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from WebServer import PersonalWebPage as p

pp = p.PersonalWebPage()  # configuration par défaut#
# pour test
# pp = p.PersonalWebPage(configurationFichier="indiqué")
# pp = p.PersonalWebPage(configurationFichier="../Conf/conf.yaml")
# pp = p.PersonalWebPage(configurationFichier="conf.yaml")
# personalWebPage = p.PersonalWebPage(dossierMdDestination="GitHubContent", dossierHtmlDestination="GitHubStatic")
# print("vars :", vars(pp))
pp.vider_les_repertoires()
pp.copier_les_repertoires()
pp.deployer_les_changements()
