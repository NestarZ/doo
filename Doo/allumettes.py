#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Jeu d'allumettes:

On dispose d'un nombre n d'allumettes au depart
A tour de role on peut prendre de 1 a 3 allumettes
Le vainqueur est celui qui prend la derniere allumette

Les joueurs sont notes 0 et 1
On affiche combien il y a d'allumettes encore en jeu
Quel est le tour en cours
Quel est le joueur qui a le trait

une configuration sera le nombre d'allumettes en jeu et le tour en cours
ce sera donc ici une paire
"""
# on importe ce dont on a besoin
from abstract import Game, Player, partie # pas manche
import random # utile pour le joueur aléatoire

# la classe pour le jeu

class allumettes(Game):
    """
    La classe generique pour des jeux a deux joueurs
    """
    def __init__(self,allumettes=10):
        """
        constructeur de classe, joue le meme role que initialisation
        Il va falloir creer la configuration initiale
        *args : parametre necessaire a l'initialisation
        **kwargs : parametre nomme necessaire a l'initialisation
        """
        if allumettes < 0 or allumettes > 16 :
            allumettes = 10
        self.configuration = allumettes,1


    @property
    def configuration(self):
        """
        renvoie la configuration courante du jeu
        """
        return self.__etat

    @configuration.setter
    def configuration(self,newcfg):
        """
        On fait ici les controles pour s'assurer que tout ce passe
        pour le mieux, on peut a ce niveau sauvegarder l'ancienne
        configuration (par exemple pour gerer un historique)

        utilisation
        monJeu = game()
        monJeu.configuration = nouvelle_configuration
        """
        assert isinstance(newcfg,(list,tuple))
        assert len(newcfg) == 2
        for i in range(2):
            assert isinstance(newcfg[i],int)
        self.__etat = newcfg

    def __str__(self):
        """
        renvoie la chaine a affiche lors d'un print
        joue le meme role que affichage
        """
        _all,_tr = self.configuration
        _msg = "Il reste %d allumettes c'est le tour %d"
        return _msg % (_all,_tr)

    @classmethod
    def regles(cls):
        """ affiche les regles du jeux """
        _msg = """
        A chaque tour on peut prendre 1, 2 ou 3 allumettes
        Le gagnant est celui qui prend la derniere allumette
        """

        return _msg

    def adversaire(self,joueur):
        """ renvoie l'autre joueur """
        return (joueur+1) % 2


    def gagnant(self,joueur):
        """ renvoie True si l'etat est une victoire pour le joueur """
        return self.perdant(self.adversaire(joueur))


    def perdant(self,joueur):
        """ renvoie True si l'etat est une defaite pour le joueur """
        return (self.configuration[0] == 0)


    def finPartie(self,joueur):
        """ renvoie True si la partie est terminee """
        return self.perdant(joueur) or self.perdant(self.adversaire(joueur))

    def listeCoups(self,joueur):
        """ renvoie la liste des coups autorises pour le joueur """
        _allumettes = self.configuration[0]
        return list(range(1,min(3,_allumettes)+1))

    def joue(self,joueur,coup):
        """
        renvoie une nouvelle configuration
        apres que le joueur a effectue son coup
        """
        _oldA,_oldT = self.configuration
        return _oldA - coup, _oldT+1

    def evaluation(self,joueur):
        """
        evalue numeriquement la situation dans lequel se trouve le joueur
        """
        if self.perdant(joueur): return -10
        if self.gagnant(joueur): return 10
        return 0

# codes specifiques aux joueurs

class humain(Player):
    """
    La classe humain derive de la classe player
    """
    def __init__(self,monNom):
        self.nom = monNom

    def choixCoup(self,unJeu,joueur):
        """ renvoie le coup choisi par le joueur
        le coup est obligatoirement un coup appartenant a
        listeCoups(joueur)
        """
        super(humain,self).choixCoup(unJeu,joueur) # verification facultative
        _possibles = unJeu.listeCoups(joueur) # les possibles
        _coup = -1 # un truc impossible
        while _coup not in _possibles :# On redemande tant que coup non légal
            _coup = int(input("nombre d'allumettes a prendre ? %s " %\
                              _possibles))
        return _coup

class aleatoire(Player):
    """
    La classe aleatoire derive de la classe player
    """
    def __init__(self):
        self.nom = "ordi aleatoire"

    def choixCoup(self,unJeu,joueur):
        """ renvoie un coup aleatoire
        le coup est obligatoirement un coup appartenant a
        listeCoups(joueur)
        """
        super(aleatoire,self).choixCoup(unJeu,joueur)
        _possibles = unJeu.listeCoups(joueur)
        return random.choice(_possibles)

# petit utilitaire pour me simplifier la tache, pas nécessaire
def affichage(unjeu,unjoueur):
    """ juste des print et des assert """
    assert isinstance(unjeu,Game), "pas un jeu conforme"
    assert isinstance(unjoueur,Player), "pas un joueur conforme"
    print(unjoueur,'a le trait')
    print(unjeu)
    
# fonction principale permettant de simuler une partie

def partie(funA=None,funB=None):
    """
    funA et funB sont des fonctions pour les joueurs A et B
    elles recoivent en entree un etat et un joueur, elles renvoient un coup
    par defaut on fait jouer  humain contre aleatoire

    partie doit
    1. afficher les regles du jeu
    2. faire jouer alternativement le joueur A et le joueur B
    3. afficher les informations
    4. s'arreter quand la partie est terminee
    5. afficher qui a gagné
    """
    if not isinstance(funA,Player): funA = humain('A')
    if not isinstance(funB,Player): funB = aleatoire()

    print (allumettes.regles())
    joueurs = (funA,funB)
    _choix = int(input("combien d'allumettes au depart ? "))
    unJeu = allumettes(_choix)
    _jtrait = 0
    while not unJeu.finPartie(_jtrait):
        affichage(unJeu,joueurs[_jtrait])
        # joueurs[0](unJeu,0) c'est joueurs[0].choixCoup(unJeu,0)
        _coup = joueurs[_jtrait](unJeu,_jtrait)
        unJeu.configuration = unJeu.joue(_jtrait,_coup)
        _jtrait = unJeu.adversaire(_jtrait)

    # quand on sort le perdant est celui qui doit joueur donc
    _gagnant = unJeu.adversaire(_jtrait)
    print("%s a gagne en %d tours" % (joueurs[_gagnant].nom,
                                      unJeu.configuration[1]-1))



#------- partie non nécessaire mais permet de construire calmement ----#
def test_fonctions():
    """ tests simplissimes pour vérifier que tout va bien
    On regarde le cas ou il n'y a que 2 allumettes dans le jeu
    On regarde le cas ou il y a 25 allumettes dans le jeu
    """
    print("test de l'acces aux regles")
    print ( allumettes.regles() )
    print("test reussi")
    for i in (2,25):
        jtrait = 0
        jeu = allumettes(i)
        moi = humain('Marcel')
        lui = aleatoire()
        
        affichage(jeu,moi)
        # pas plus de coups que d'allumettes
        # pas plus de 3 allumettes a prendre
        print('test: listeCoups')
        assert(len(jeu.listeCoups(jtrait)) == min(3,i))
        # un humain ne peut jouer qu'un coup autorise
        print('test: humain')
        _choix = moi(jeu,jtrait)
        assert(_choix in jeu.listeCoups(jtrait))
        print('subtest: joue')
        _ncfg = jeu.joue(jtrait,_choix)
        # joue renvoie un etat
        assert(isinstance(_ncfg,tuple))
        assert(len(_ncfg) == 2)
        assert(_ncfg[0]+_choix == jeu.configuration[0])
        assert(_ncfg[1] - 1 == jeu.configuration[1])
        # un ordi aleatoire ne peut faire qu'un coup autorise
        print('test: aleatoire')
        _choix = lui(jeu,jtrait)
        assert(_choix in jeu.listeCoups(jtrait))
        print('subtest: joue')
        _ncfg = jeu.joue(jtrait,_choix)
        # joue renvoie un etat
        assert(isinstance(_ncfg,tuple))
        assert(len(_ncfg) == 2)
        assert(_ncfg[0]+_choix == jeu.configuration[0])
        assert(_ncfg[1] - 1 == jeu.configuration[1])

        # un joueur c'est 0 ou 1
        print('test: adversaire')
        assert(jeu.adversaire(jtrait) in (0,1))
        print('tests pour %d allumettes ok' % i)
        print ('_'*10)

    input("**** fin des tests       appuyez <entree> ****")

if __name__ == "__main__" :
    _ok = "oO0Yy"
    _choix = input("Voulez-vous lancer les tests des fonctions ? (%s) " % _ok)
    if _choix in _ok : test_fonctions()

    print("lancement d'une partie")
    partie()


