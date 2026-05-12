"""actions qualite

- badge de comptage de fonctions et lignes de code
"""
from pathlib import Path
import anybadge
import sys
import json

myDir = Path(__file__).parents[1]
sys.path.insert(0, str(myDir))  # translate from posixPath

from Code import marss
from inspect import getmembers, isfunction

nombre_fonctions = len(getmembers(marss, isfunction))
badge = anybadge.Badge('fonctions', nombre_fonctions, default_color='green')
badge.write_badge('Doc/fonctions.svg', overwrite=True)

with open(str(myDir) + "/Doc/code-marss.json", "r") as f:
    data = json.load(f)
    taille_code = data['summary']['totalCodeCount']

badge = anybadge.Badge('code', taille_code, default_color='blue')
badge.write_badge('Doc/code.svg', overwrite=True)