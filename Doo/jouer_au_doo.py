from tp01b import partie, Human
from arbres import IA
from tp01a import *
from evaluations import evaluation6, evaluation5, evaluation4

level = {1: evaluation4, 2: evaluation5, 3: evaluation6}

force = int(input("force: "))
difficulte = min(3, max(1, int(input("difficulte (1: facile, 2: moyen, 3: difficile): "))))
partie(Human(), IA(force, 4, level[difficulte]))
