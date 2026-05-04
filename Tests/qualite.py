"""actions qualite

- badge de comptage de fonctions
"""
from pathlib import Path
import anybadge
import sys

myDir = Path(__file__).parents[1]
sys.path.insert(0, str(myDir))  # translate from posixPath

from Code import marss
from inspect import getmembers, isfunction

nombre_fonctions = len(getmembers(marss,isfunction))
badge = anybadge.Badge('fonctions', nombre_fonctions, default_color='green')
badge.write_badge('Doc/fonctions.svg', overwrite=True)
