from pathlib import Path
import os
import yaml
# from os import path
# from datetime import datetime, timezone
import shutil
import git
# depuis Webserver OK
from datetime import datetime
import argparse

"""pour publier sur des hébergeurs tels : GithubPages

- méthode : pas encore fixé sur class, getter/setter, properties, dataclass
"""

class PersonalWebPage:

    def __init__(self, configurationFichier=None, dossierMdDestination=None, dossierHtmlDestination=None, dossierMdSource=None, dossierHtmlSource=None):
        """charger à lavolonté du client

        - par fichier de conf par défaut
        - par fichier de conf spécifique indiqué par le client
        - par paramètres settés à la demande par le client
        """
        if configurationFichier == None and dossierMdDestination == None:
            print("utiliser le fichier de configuration par defaut")
            dirname = os.path.dirname(__file__)
            self.configurationFichier = os.path.join(dirname, "conf.yaml")
            # self.__setter_exemple()
            self.configuration = self.__recuperer_configuration()
            print("configuration :", self.configuration)
            self.assigner_variables_configuration()
        elif configurationFichier != None:
            print("utiliser un fichier de configuration specifique")
            dirname = os.path.dirname(__file__)
            self.configurationFichier = os.path.join(dirname, configurationFichier)
            self.configuration = self.__recuperer_configuration()
            print("configuration :", self.configuration) # debug
            # propre : tester existence d'un ensemble de clés et signifier si erreur
            self.assigner_variables_configuration()       
        elif dossierMdDestination != None:
            print("utiliser les attributs a la demande")
            self.configurationFichier = "non pris en compte" 
            self.dossierMdDestination = dossierMdDestination
            self.dossierHtmlDestination = dossierHtmlDestination
            self.dossierMdSource = dossierMdSource
            self.dossierHtmlSource = dossierHtmlSource

        self.message = self.recupererCmdLine()
        print("message transmis ou non :", self.message)

    def __recuperer_configuration(self):
        """méthode privée pour initialiser les paramètres

        - est utilisée optionnellement
        """
        myConf = self.configurationFichier
        extension = str(myConf).lower().endswith(('.yml', '.yaml'))
        fichier = Path(myConf).is_file()
        print("le chemin du fichier de configuration est:", myConf)
        print("la ressource a la bonne extension:", extension)
        print("la ressource est bien un fichier:", fichier)
        if extension and fichier:
            with open(myConf) as f:
                try:
                    conf = yaml.load(f, Loader=yaml.FullLoader)
                    return conf
                except Exception as e:
                    print('erreur fichier mal formate')
                    print(e)
                    exit(2)
        else:
            print('erreur fichier de configuration')
            exit(1)

    def assigner_variables_configuration(self):
        variables = ["dossierMdDestination", "dossierHtmlDestination", "dossierMdSource", "dossierHtmlSource"]
        erreurs = list()
        for key in variables:
            if key not in (self.configuration):
                erreurs.append(key)
            else:
                setattr(self, key, self.configuration[key])  # auto assignation
                print("cle :", key, "- value :", self.configuration[key])
        if len(erreurs) >= 1:
            print("cles manquantes :", erreurs)
            exit(1)
        else:
            print("assignation de toutes les variables utiles de configuration :", vars(self))

    def recupererCmdLine(self):  # pragma: no cover
        """recuperer les arguments en console

        - que le message de commit pour l('instant)
        """
        parser = argparse.ArgumentParser()
        parser.add_argument("-m", "--message", help="message de commit")
        message = None
        try:
            args = parser.parse_args()
            if args.message:
                message = args.message
                print("message de commit :", self.message)
        except:
            print("soumettre le message avec -m ou --message puis '...'")
        return message

    def vider_les_repertoires(self):
        """utilisée en test teardown
        """
        here = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        print("md lu dans : ", self.dossierMdDestination )
        print("html lu dans : ", self.dossierHtmlDestination)
        files = Path(f'{here}/{self.dossierMdDestination}').rglob('*.*')
        files2 = Path(f'{here}/{self.dossierHtmlDestination}').rglob('*.*')
        # chainer/merger generator
        def chained_generator():
                yield from files
                yield from files2
        # generator object Path.rglob
        for file in chained_generator():
            print("traiter le fichier :", file)
            if file.name.startswith("."):
                print("ne pas supprimer :", file.name)       
            else:
                print("supprimer :", file)
                file.unlink()

    def copier_les_repertoires(self):
        here = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        shutil.copytree(f'{here}/{self.dossierHtmlSource}', f'{here}/{self.dossierHtmlDestination}', dirs_exist_ok=True)
        shutil.copytree(f'{here}/{self.dossierMdSource}', f'{here}/{self.dossierMdDestination}', dirs_exist_ok=True)
        
    def deployer_les_changements(self):
        """diff ne voit que les changements, pas les nouveautés
        """
        dirname = os.path.dirname(__file__)
        direp = os.path.join(dirname, "../../dev4use/")
        print("repo visé :", direp)
        repo = git.Repo(direp)
        # debug uniquement
        # print(repo.git.status())  
        
        # inutile, que pour le reporting console
        news = repo.untracked_files
        print(str(len(news)), "nouveaux fichiers :", news)
        # inutile, que pour le reporting console
        diffs = repo.index.diff(None)  # repo.head.commit
        fichiers = list()
        fix = os.path.abspath(__file__)
        chemin = str(fix).replace("marss/WebServer/PersonalWebPage.py", "dev4use")
        print("chemin :", chemin)
        for d in diffs:
            fichiers.append(direp + d.a_path)
        print(str(len(diffs)), "changements :", fichiers)

        repo.git.add('--all') # OK pour tout je pense
        
        actual = str(datetime.now())
        if self.message == None:
            # si message non fourni
            repo.index.commit(f"mise à jour automatique du contenu {actual}")  # KO bug avec now ?
        else:
            repo.index.commit(self.message)
        origin = repo.remote(name='origin')  # OK
        origin.push()  # OK 
   