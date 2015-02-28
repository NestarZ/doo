#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "mmc <marc-michel.corsini@u-bordeaux.fr>"


try:
    # changer XXXX par le nom de votre fichier
    # changer YYYY par la classe du jeu
    from tp01a import Doo as ze_class
    from tp01a import J_ATT, J_DEF, BLANCS, NOIRS, ROI, VIDE

    # NE PAS MODIFIER CE QUI SUIT
except Exception as _e :
    print(_e)
    exit()
finally:
    from abstract import Game
        

def check_property(prop,letter='E'):
    """ un test valide dans un try/except """
    _rep = ''
    try:
        assert(prop)
        _rep += '.'
    except:
        _rep += letter
    finally:
        return _rep
#------------------ petits outils ------------------------------#
class Resultat(object):
    """ permet de construire un exemple avec les valeurs attendues """
    def __init__(self,*args,cpt=None):
        """ des args non nommés + 1 nommé """
        self.__args = args
        self.__cpt = cpt

    def __str__(self):
        _str = "%s %d\n" % self.cfg
        _str += "Joueur a le trait %s\n" % self.trait
        _str += "finPartie %s\n" % self.finPartie
        _str += "listeCoups %d\n" % self.listeCoups
        _str += "gagnant %s\n" % self.gagnant
        _str += "perdant %s\n" % self.perdant
        return _str
    
    @property
    def cfg(self): return self.__args[0],self.cpt
    @property
    def jtrait(self): return self.__args[1]
    @property
    def joueur(self): return self.__args[2]
    @property
    def cpt(self):
        if not( self.__cpt is None ): return self.__cpt
        if self.jtrait == J_DEF:
            return 14
        else:
            return 13
    @property
    def trait(self): return self.jtrait == self.joueur
    @property
    def finPartie(self): return self.__args[3]
    @property
    def listeCoups(self): return self.__args[4]
    @property
    def gagnant(self): return self.__args[5]
    @property
    def perdant(self): return self.__args[6]
    


def voisinage8(p):
    """ voisinage pour NOIRS/ROI """
    return __voisinage(p,lambda a,b: (a*b != a+b))
def voisinage4(p):
    """ voisinage pour BLANCS/Prise Any """
    return __voisinage(p,lambda a,b: (a != b and a != -b))

def pos2coord(p):
    """ passage d'un int à une paire """
    return (p-p%3)//3,p%3
def coord2pos(i,j):
    """ passage d'une paire à un int """
    return i*3+j

# __voisinage: helper ne devrait pas etre accédée par l'utilisateur
def __voisinage(p,test):
    """ renvoie le voisinage de p en fonction du test 4 ou 8 voisins """
    assert( p in range(12) )
    v = [ (i,j) for i in (-1,0,1) for j in (-1,0,1) if test(i,j) ]
    assert( len(v) in (4,8) )
    i,j = pos2coord(p)
    return [ coord2pos(i+di,j+dj) for (di,dj) in v
             if (i+di) in range(4) if (j+dj) in range(3) ]

def test_voisinage(cfg,joueur,listCps, err='E'):
    """ on regarde si les coups sont valables """
    _lst = ''
    if joueur == J_DEF: pierres = [ NOIRS, ROI ] ; me = [ BLANCS ]
    if joueur == J_ATT: pierres = [ BLANCS ] ; me = [ NOIRS, ROI ]
    if cfg[1] < 8 : return _lst
    for a,b in listCps:
        prop = (cfg[0][a] in me)
        _lst += check_property( prop, err )
        if isinstance(b,int): # déplacement
            prop = (cfg[0][b] == VIDE)
            if joueur == J_DEF: vicinity = voisinage4(a)
            if joueur == J_ATT: vicinity = voisinage8(a)
            prop = prop and (b in vicinity)
        else: # capture
            x1,x2 = pos2coord(a)
            _coords = [ (x1,x2) ]
            prop = True
            for u in b :
                prop = prop and (cfg[0][u] == VIDE) # liste de cases vides
                u1,u2 = pos2coord(u)
                _coords.append( (u1,u2) )
            _sz = len( _coords )
            for i in range(_sz -1):
                x1,x2 = _coords[i]
                vicinity1 = voisinage4(coord2pos(x1,x2))
                j = i+1 # suivant dans la liste
                u1,u2 = _coords[j]
                w = coord2pos( (x1+u1)//2,(x2+u2)//2 ) # w entre x et u
                vicinity2 = voisinage4(coord2pos(u1,u2))
                prop = prop and (w in vicinity1) and (w in vicinity2)
                prop = prop and (cfg[0][w] in pierres) # prises ennemies

        _lst += check_property( prop, err )
        if err in _lst: print("ERREUR",cfg,joueur,a,b)
    return _lst
        
def generate_config():
    """ crée une configuration possible pour débuter phase 2 """
    import random
    # On pioche au hasard la position du Roi et de 3 attaquants
    _l = random.sample( [ _ for _ in range(12) if (_ != 4 and _ != 7)],4)
    _t = [ BLANCS for _ in range(12) ] # rempli de défenseurs
    _t[4] = VIDE # Position du Doo
    _t[ _l[0] ] = ROI # Placement du Roi
    for x in _l[1:]: _t[x] = NOIRS # Placement des attaquants
    return _t # renvoie le tablier construit

def build_base():
    """ crée plusieurs configurations
        0: valable en fin de pose cf generate_config
        1: un seul pion noir en Doo
        2: un noir en Doo & un blanc
        3: un blanc en Doo, entouré de noirs
        4: symétrique de 3
        5: un noir bloqué
        6: un blanc bloqué
        7: un blanc seul (correpond a init)
        8 et suivants : cas pour listeCoups
    """
    _cfg = { 1: [VIDE, VIDE, VIDE,
                VIDE, NOIRS, VIDE,
                VIDE, VIDE, VIDE,
                VIDE, VIDE, VIDE],
            2: [VIDE, VIDE, VIDE,
                VIDE, NOIRS, VIDE,
                VIDE, BLANCS, VIDE,
                VIDE, VIDE, VIDE],
            3: [VIDE, NOIRS, VIDE,
                NOIRS, BLANCS, ROI,
                VIDE, NOIRS, VIDE,
                VIDE, VIDE, VIDE],
            4: [VIDE, BLANCS, VIDE,
                BLANCS, ROI, BLANCS,
                VIDE, BLANCS, VIDE,
                VIDE, VIDE, VIDE],
            5: [BLANCS, BLANCS, ROI,
                VIDE, BLANCS, BLANCS,
                VIDE, VIDE, BLANCS,
                VIDE, VIDE, VIDE],
            6: [NOIRS, NOIRS, BLANCS,
                VIDE, VIDE, NOIRS,
                VIDE, VIDE, ROI,
                VIDE, VIDE, VIDE],
            7: [VIDE, VIDE, VIDE,
                VIDE, VIDE, VIDE,
                VIDE, BLANCS, VIDE,
                VIDE, VIDE, VIDE],
            8: [BLANCS,ROI,VIDE,
                VIDE,NOIRS,VIDE,
                VIDE,VIDE,NOIRS,
                BLANCS,NOIRS,VIDE],
            9: [BLANCS,VIDE,VIDE,
                VIDE, VIDE,VIDE,
                VIDE, NOIRS, VIDE,
                VIDE, VIDE, VIDE],
            10: [BLANCS,VIDE,VIDE,
                VIDE, VIDE,VIDE,
                VIDE, ROI, VIDE,
                VIDE, VIDE, VIDE],
            11: [ROI,VIDE,VIDE,
                VIDE, VIDE,VIDE,
                VIDE, BLANCS, VIDE,
                VIDE, VIDE, VIDE],
            12:[BLANCS,VIDE,VIDE,
                VIDE, VIDE,VIDE,
                VIDE, VIDE, BLANCS,
                ROI, BLANCS,VIDE],
            13: [ROI,VIDE,VIDE,
                VIDE, BLANCS,VIDE,
                VIDE, VIDE, VIDE,
                VIDE, VIDE, VIDE],
            14: [NOIRS,VIDE,VIDE,
                VIDE, BLANCS,VIDE,
                VIDE, VIDE, VIDE,
                VIDE, VIDE, VIDE],

    }

    _cfg[0] = generate_config()# On ajoute en 0 un tablier rempli
    # On veut tester listeCoups, finPartie, gagnant, perdant
    # 2 cas de figure: J_ATT a le trait, J_DEF a le trait
    # les calculs sont faits à la main
    _resultat = set()
    # cfg, qui_devrait, qui_demande, finP, nbCoups, gagnant, perdant
    # 0 tablier rempli début phase 2 [-1 abbreviation pour >= 1]
    _resultat.add( Resultat(_cfg[0],J_ATT,J_ATT,False,-1,False,False) )
    _resultat.add( Resultat(_cfg[0],J_ATT,J_DEF,False,0,False,False) )
    _resultat.add( Resultat(_cfg[0],J_DEF,J_ATT,False,0,False,False,cpt=8) )
    _resultat.add( Resultat(_cfg[0],J_DEF,J_DEF,False,-1,False,False,cpt=8) )
    # Noir en Doo seul
    _resultat.add( Resultat(_cfg[1],J_ATT,J_ATT,True,0,True,False) )
    _resultat.add( Resultat(_cfg[1],J_ATT,J_DEF,True,0,False,True) )
    _resultat.add( Resultat(_cfg[1],J_DEF,J_ATT,True,0,True,False) )
    _resultat.add( Resultat(_cfg[1],J_DEF,J_DEF,True,0,False,True) )
    # Noir en Doo et Blanc a cote
    _resultat.add( Resultat(_cfg[2],J_ATT,J_ATT,True,0,True,False) )
    _resultat.add( Resultat(_cfg[2],J_ATT,J_DEF,True,0,False,True) )
    _resultat.add( Resultat(_cfg[2],J_DEF,J_ATT,True,0,True,False) )
    _resultat.add( Resultat(_cfg[2],J_DEF,J_DEF,True,0,False,True) )
    # Blanc en Doo entouré de Noir
    _resultat.add( Resultat(_cfg[3],J_ATT,J_ATT,False,11,False,False) )
    _resultat.add( Resultat(_cfg[3],J_ATT,J_DEF,False,0,False,False) )
    _resultat.add( Resultat(_cfg[3],J_DEF,J_ATT,False,0,False,False) )
    _resultat.add( Resultat(_cfg[3],J_DEF,J_DEF,False,1,False,False) )
    # Roi en Doo, entouré de 4
    _resultat.add( Resultat(_cfg[4],J_ATT,J_ATT,True,0,True,False) )
    _resultat.add( Resultat(_cfg[4],J_ATT,J_DEF,True,0,False,True) )
    _resultat.add( Resultat(_cfg[4],J_DEF,J_ATT,True,0,True,False) )
    _resultat.add( Resultat(_cfg[4],J_DEF,J_DEF,True,0,False,True) )
    # 5 noir est bloqué
    _resultat.add( Resultat(_cfg[5],J_ATT,J_ATT,True,0,False,True) )
    _resultat.add( Resultat(_cfg[5],J_ATT,J_DEF,True,0,True,False) )
    _resultat.add( Resultat(_cfg[5],J_DEF,J_ATT,False,0,False,False) )
    _resultat.add( Resultat(_cfg[5],J_DEF,J_DEF,False,5,False,False) )
    # 6 blanc en coin, bloqué
    _resultat.add( Resultat(_cfg[6],J_ATT,J_ATT,False,10,False,False) )
    _resultat.add( Resultat(_cfg[6],J_ATT,J_DEF,False,0,False,False) )
    _resultat.add( Resultat(_cfg[6],J_DEF,J_ATT,True,0,False,True) )
    _resultat.add( Resultat(_cfg[6],J_DEF,J_DEF,True,0,True,False) )
    # 7 fin de jeu, BLANCS seul
    _resultat.add( Resultat(_cfg[7],J_ATT,J_DEF,True,0,True,False) )
    _resultat.add( Resultat(_cfg[7],J_ATT,J_ATT,True,0,False,True) )
    _resultat.add( Resultat(_cfg[7],J_DEF,J_DEF,True,0,True,False) )
    _resultat.add( Resultat(_cfg[7],J_DEF,J_ATT,True,0,False,True) )
    # Blanc seul et premier coup
    _resultat.add( Resultat(_cfg[7],J_ATT,J_ATT,False,14,False,False,cpt=1) )
    _resultat.add( Resultat(_cfg[7],J_ATT,J_DEF,False,0,False,False,cpt=1) )
    # Blanc seul et second coup 
    _resultat.add( Resultat(_cfg[7],J_DEF,J_ATT,False,0,False,False,cpt=2) )
    _resultat.add( Resultat(_cfg[7],J_DEF,J_DEF,False,45,False,False,cpt=2) )
    # Blanc seul et troisieme coup
    _resultat.add( Resultat(_cfg[7],J_ATT,J_ATT,False,20,False,False,cpt=3) )
    _resultat.add( Resultat(_cfg[7],J_ATT,J_DEF,False,0,False,False,cpt=3) )
    # 8: coup forcé pour les blancs qui permettent à Noir de gagner
    _resultat.add( Resultat(_cfg[8],J_ATT,J_DEF,False,0,False,False) )
    _resultat.add( Resultat(_cfg[8],J_ATT,J_ATT,False,3+5+3+3,False,False) )
    _resultat.add( Resultat(_cfg[8],J_DEF,J_DEF,False,1,False,False) )
    _resultat.add( Resultat(_cfg[8],J_DEF,J_ATT,False,0,False,False) )
    # 9: Voisinage sans prise
    _resultat.add( Resultat(_cfg[9],J_ATT,J_DEF,False,0,False,False) )
    _resultat.add( Resultat(_cfg[9],J_ATT,J_ATT,False,8,False,False) )
    _resultat.add( Resultat(_cfg[9],J_DEF,J_DEF,False,2,False,False) )
    _resultat.add( Resultat(_cfg[9],J_DEF,J_ATT,False,0,False,False) )
    # 10: Voisinage sans prise pour ROI
    _resultat.add( Resultat(_cfg[10],J_ATT,J_DEF,False,0,False,False) )
    _resultat.add( Resultat(_cfg[10],J_ATT,J_ATT,False,8,False,False) )
    _resultat.add( Resultat(_cfg[10],J_DEF,J_DEF,False,2,False,False) )
    _resultat.add( Resultat(_cfg[10],J_DEF,J_ATT,False,0,False,False) )
    # 11: Voisinage sans prise pour BLANCS
    _resultat.add( Resultat(_cfg[11],J_ATT,J_DEF,False,0,False,False) )
    _resultat.add( Resultat(_cfg[11],J_ATT,J_ATT,False,3,False,False) )
    _resultat.add( Resultat(_cfg[11],J_DEF,J_DEF,False,4,False,False) )
    _resultat.add( Resultat(_cfg[11],J_DEF,J_ATT,False,0,False,False) )
    # 12: Voisinage avec prise
    _resultat.add( Resultat(_cfg[12],J_ATT,J_DEF,False,0,False,False) )
    _resultat.add( Resultat(_cfg[12],J_ATT,J_ATT,False,3,False,False) )
    _resultat.add( Resultat(_cfg[12],J_DEF,J_DEF,False,7,False,False) )
    _resultat.add( Resultat(_cfg[12],J_DEF,J_ATT,False,0,False,False) )
    # 13 ROI: pas de diagonale en prise
    _resultat.add( Resultat(_cfg[13],J_ATT,J_DEF,False,0,False,False) )
    _resultat.add( Resultat(_cfg[13],J_ATT,J_ATT,False,2,False,False) )
    _resultat.add( Resultat(_cfg[13],J_DEF,J_DEF,False,4,False,False) )
    _resultat.add( Resultat(_cfg[13],J_DEF,J_ATT,False,0,False,False) )
    # 14 NOIRS: pas de diagonale en prise
    _resultat.add( Resultat(_cfg[14],J_ATT,J_DEF,False,0,False,False) )
    _resultat.add( Resultat(_cfg[14],J_ATT,J_ATT,False,2,False,False) )
    _resultat.add( Resultat(_cfg[14],J_DEF,J_DEF,False,4,False,False) )
    _resultat.add( Resultat(_cfg[14],J_DEF,J_ATT,False,0,False,False) )
    return _resultat

def debug_configuration():
    """ permet de regarder pas à pas les problèmes des configurations tests """
    _out = build_base()
    p = ze_class()
    for x in _out: # config tests
        p.configuration = x.cfg # On force la valeur
        print(p) # votre affichage
        if x.listeCoups !=-1 :
            _diag = (p.finPartie(x.joueur) == x.finPartie and
                len(p.listeCoups(x.joueur)) == x.listeCoups and
                p.gagnant(x.joueur) == x.gagnant and
                p.perdant(x.joueur) == x.perdant)
        else:
            _diag = (p.finPartie(x.joueur) == x.finPartie and
                len(p.listeCoups(x.joueur)) >= 1 and
                p.gagnant(x.joueur) == x.gagnant and
                p.perdant(x.joueur) == x.perdant)
            
        if not _diag :
            print("ERREUR",x) ; print("... found")
            print(p.finPartie(x.joueur),len(p.listeCoups(x.joueur)),
                  p.gagnant(x.joueur),p.perdant(x.joueur))
            input("<enter>")
        print('******')
        
def test_etat( cfg, testPose = True, err='E' ):
    """ on reçoit un état, on vérifie qu'il est conforme """
    _lstr = ''
    # bonne structure
    prop = (len(cfg) == 2)
    _lstr += check_property( prop, err )
    if err in _lstr: return _lstr
    # bon type
    _t,_c = cfg
    prop = ( isinstance(_t,(tuple,list)) and isinstance(_c,(int,float)) )
    _lstr += check_property( prop, err )
    if err in _lstr: return _lstr
    # bon contenu
    _all = [ _t.count(NOIRS), _t.count(ROI), _t.count(BLANCS),
             _t.count(VIDE) ]
    prop = (sum(_all) == 12)
    _lstr += check_property( prop, err )
    _max = [ 3,1,7,12 ]
    for i in range(4):
        prop = (_all[i] <= _max[i])
        _lstr += check_property( prop, err )
    prop = ( _c >= 1 )
    _lstr += check_property( prop, err )
    if err in _lstr: return _lstr
    if _c < 9  and testPose:
        _lstr += test_etat_pose( _t, _c, _all, err )
    return _lstr

def test_etat_pose( tab, cpt, list_count, err = 'E' ):
    """ on reçoit un état, on vérifie qu'il est conforme """
    _lstr = ''
    _n = list_count[0] + list_count[1]
    _b = list_count[2]
    if cpt in (1,3,5,7) :
        prop = ( _b == cpt and _n == cpt // 2 )
        _lstr += check_property( prop, err )
    elif cpt in (2,4,6,8):
        prop = ( _n == cpt // 2 and _b == cpt -1 )
        _lstr += check_property( prop, err )
    if cpt == 2:
        prop = (tab[1] in (BLANCS,VIDE) and
                tab[3] in (BLANCS,VIDE) and
                tab[5] in (BLANCS,VIDE))
        _lstr += check_property( prop, err )
    _lstr += check_property( tab[4] == VIDE )
    return _lstr
    
    
# tests de chaque méthodes
def test_initialisation():
    """ on regarde si l'initialisation est conforme
        test configuration en lecture
    """
    projet = ze_class()
    _lstr = test_etat( projet.configuration )
    if 'E' in _lstr: return _lstr
    _c0 = [ VIDE, VIDE, VIDE,
            VIDE, VIDE, VIDE,
            VIDE, BLANCS, VIDE,
            VIDE, VIDE, VIDE ]
    _cfg0 = projet.configuration
    _lstr += check_property( _cfg0[1] == 1 )
    _lstr += check_property( _cfg0[0] == _c0 )
    return _lstr


def test_str():
    """ on regarde si on a un affichage """
    _lstr = ''
    projet = ze_class()
    prop = (isinstance(projet.__str__(),str))
    return check_property( prop )

def test_regles():
    """ regles renvoie une chaine de caracteres """
    _lstr = ''
    projet = ze_class()
    prop = ( isinstance(projet.regles(),str) )
    _lstr += check_property( prop )
    _msg = """
        ICI ON MET LES REGLES DU JEU
        """
    prop = ( projet.regles() != _msg )
    _lstr += check_property( prop )

    return _lstr

def test_configuration():
    """ vérification de configuration en écriture """
    _lstr = ''
    projet = ze_class()
    _cfg = [BLANCS,ROI,VIDE,
            VIDE,NOIRS,VIDE,
            VIDE,VIDE,NOIRS,
            BLANCS,NOIRS,VIDE], 13
    projet.configuration = _cfg
    prop = ( projet.configuration == _cfg )
    _lstr += check_property( prop )
    return _lstr
    
def test_adversaire():
    """ vérification de la fonction adversaire """
    _lstr = ''
    projet = ze_class()
    prop = ( projet.adversaire(J_ATT) == J_DEF )
    _lstr += check_property( prop )
    prop = ( projet.adversaire(J_DEF) == J_ATT )
    _lstr += check_property( prop )
    return _lstr

def test_gagnant():
    """ vérification de gagnant """
    _lstr = ''
    _out = build_base()
    projet = ze_class()
    for x in _out: # config test
        projet.configuration = x.cfg
        prop = (projet.gagnant(x.joueur) == x.gagnant)
        _lstr += check_property( prop )
    return _lstr

def test_perdant():
    """ vérification de perdant """
    _lstr = ''
    _out = build_base()
    projet = ze_class()
    for x in _out: # config test
        projet.configuration = x.cfg
        prop = (projet.perdant(x.joueur) == x.perdant)
        _lstr += check_property( prop )

    return _lstr

def test_finPartie():
    """ vérification de finPartie """
    _lstr = ''
    _out = build_base()
    projet = ze_class()
    for x in _out: # config test
        projet.configuration = x.cfg
        prop = (projet.finPartie(x.joueur) == x.finPartie)
        _lstr += check_property( prop )

    return _lstr

def test_listeCoups():
    """ vérification de listeCoups """
    # si pas mon tour : [] ::DONE::
    # si noir a gagné : [] ::DONE::
    # A: si noir et coup < 8 : elements (type,pos) ::DONE::
    # B: si blanc et coup < 8 : elements (p1,p2) & p1 < p2 ::DONE::
    # si noir et coup > 8 et pas prise : 8 voisins ::DONE::
    # si blanc et coup > 8 et pas prise : 4 voisins ::DONE::
    # C: si noir et coup > 8 et prise : 8 voisins + 4 voisins ::DONE::
    # si blanc et coup > 8 et prise : prises ::DONE::
    _lstr = ''
    projet = ze_class()
    # A
    lcps = projet.listeCoups( J_ATT )
    for x,y in lcps:
        prop = ( x in (ROI,NOIRS) and y in [0,2,6,8,9,10,11] )
        _lstr += check_property( prop )
        if 'E' in _lstr : return _lstr
    # B
    _old,_cpt = projet.configuration
    _old[0] = ROI
    projet.configuration = _old,_cpt+1
    lcps = projet.listeCoups( J_DEF )
    for x,y in lcps:
        prop = ( x in (1,2,3,5,6,8,9,10,11) and
                 y in [2,3,5,6,8,9,10,11] and
                 x < y )
        _lstr += check_property( prop )
        if 'E' in _lstr : return _lstr
    
    _out = build_base()
    for x in _out: # config test
        projet.configuration = x.cfg
        if x.listeCoups != -1:
            prop = (len(projet.listeCoups(x.joueur)) == x.listeCoups)
        else:
            prop = (len(projet.listeCoups(x.joueur)) >= 1)
            
        _lstr += check_property( prop )

        if x.listeCoups != 0 :
            _out = test_voisinage(x.cfg,x.joueur,
                                    projet.listeCoups(x.joueur), err='X')
            if 'X' in _out : return _lstr+'E'
            _lstr += '.'

    # C pour les ATTQ
    for WHO in (NOIRS, ROI): # doit avoir le meme comportement
        _cfg = [ WHO, BLANCS, VIDE,
                VIDE, BLANCS, BLANCS,
                VIDE, NOIRS, VIDE,
                VIDE, VIDE, VIDE ]
        projet.configuration = _cfg, 13
        lcps = projet.listeCoups( J_ATT )
        prop = (len( lcps ) == 8)
        _lstr += check_property( prop )
        for x,y in lcps :
            if isinstance(y,(list,tuple)):
                prop = ( x in (0,7) and len(y) == 1 )
            else:
                if x == 0: prop = (y == 3)
                else: prop = ( y in (3,6,8,9,10,11) )

            _lstr += check_property( prop )
    # C pour les DEFS/ATTQ
    _cfg = [ VIDE, NOIRS, VIDE,
             VIDE, BLANCS, ROI,
             BLANCS, NOIRS, VIDE,
             VIDE, VIDE, VIDE ]
    projet.configuration = _cfg,14
    lcps = projet.listeCoups( J_DEF )
    prop = len(lcps) == 1
    _lstr += check_property( prop )
    for x,y in lcps:
        prop = isinstance(y,(list,tuple)) and len(y) == 3
        _lstr += check_property( prop )
    projet.configuration = _cfg,13
    lcps = projet.listeCoups( J_ATT )
    prop = len(lcps) == 3+2+5+1
    _lstr += check_property( prop )
        
    return _lstr

def test_joue():
    """ vérification de joue """
    # pas d'effet de bord ::DONE::
    # cpt -> cpt+1 ::DONE::
    # la prise fait ce qu'il faut ::DONE::
    # le déplacement fait ce qu'il faut ::DONE::
    import random
    _lstr = ''
    _out = build_base()
    projet = ze_class()
    for x in _out: # config test
        projet.configuration = x.cfg
        if x.listeCoups != 0:
            _pot = projet.listeCoups(x.joueur)
            _choix = random.choice( _pot )
            _rep = projet.joue( x.joueur, _choix )
            _lstr += test_etat( _rep, False, 'X' ) # pas de test pose
            if 'X' in _lstr: return _lstr
            prop = (projet.configuration[0] != _rep) # pas d'effet de bord
            _lstr += check_property( prop, '4' )
            if '4' in _lstr: return _lstr
            prop = (projet.configuration[1]+1 == _rep[1]) # bon increment
            _lstr += check_property( prop, '5' )
            if '5' in _lstr: return _lstr

            # On ne vérifie pas que les coups sont justes
            # On vérifie que les effets obtenus sont ceux attendus
            if x.cpt > 7 : # On est en phase duel
                pion = x.cfg[0][_choix[0]] # la position de départ est occupée
                prop = (pion in (NOIRS,ROI,BLANCS))
                _lstr += check_property( prop )
                if isinstance(_choix[1],int): #déplacement
                    prop = (x.cfg[0][_choix[1]] == VIDE)
                    _lstr += check_property( prop )
                    prop = (_rep[0][_choix[0]] == VIDE and
                            _rep[0][_choix[1]] == pion)
                    _lstr += check_property( prop )
                else: # prise
                    for _ in _choix[1]:
                        prop = (x.cfg[0][_] == VIDE)
                        _lstr += check_property( prop )
                    _sz = len( _choix[1] )
                    prop = ( x.cfg[0].count(VIDE) + _sz ==\
                             _rep[0].count( VIDE ) )
                    _lstr += check_property( prop )
    return _lstr

def test_evaluation():
    """ vérification de evaluation """
    # min = -max ::DONE::
    # min < eval < max ::DONE::
    _lstr = ''
    _out = build_base()
    projet = ze_class()
    _val = { 'min': set([]), 'max': set([]), 'other': set([]) }
    for x in _out: # config test
        projet.configuration = x.cfg
        if x.perdant:
            _val['min'].add( projet.evaluation( x.joueur ) )
        elif x.gagnant:
            _val['max'].add( projet.evaluation( x.joueur ) )
        else:
            _val['other'].add( projet.evaluation( x.joueur ) )

    prop = ( len(_val['min']) == 1 )
    _lstr += check_property( prop, '1' )
    if '1' in _lstr: return _lstr
    prop = ( len(_val['max']) == 1 )
    _lstr += check_property( prop, '2' )
    if '2' in _lstr: return _lstr
    x = _val['min'].pop()
    y = _val['max'].pop()
    prop = ( x == -y )
    _lstr += check_property( prop, '3' )
    if '3' in _lstr: return _lstr
    for z in _val['other']:
        prop = ( x < z < y )
        _lstr += check_property( prop, '4' )
        if '4' in _lstr: return _lstr

    return _lstr

# le code principal
def main():
    """ le programme de tests """

    _attr = [ 'regles','configuration','adversaire','gagnant','perdant',
              'finPartie','listeCoups', 'joue', 'evaluation' ]
    _str =""
    projet = ze_class()

    _sep = '\n'+'_'*75#+'\n'
    _totest = []
    for x in _attr:
        try:
            assert( hasattr(projet,x) )
            _totest.append(x) # on ne teste que ce qui est defini
            _str += '.'
        except:
            _str +='\n%s absent' % x

    _str += _sep
    _prop = isinstance(projet,Game)
    _str += '\nis a Game: %s' % check_property( _prop )
    try:
        _str += '\n__init__: ' + test_initialisation()
    except:
        _str += '\n__init__: E'
    finally:
        _str += _sep
        
    try:
        _str += '\n__str__: ' + test_str()
    except:
        _str += '\n__str__: E'
    finally:
        _str += _sep

    _success, _errors = 0,0
    for x in _totest:
        test = 'test_'+x
        try:
            _out = eval(test)()
            _ok = _out.count('.')
            _success += _ok
            _errors += len(_out) - _ok
            _str += '\n%s: ' % x + _out
        except:
            _str += '\n%s:E' % x
            _errors += 1
        finally:
            _str += _sep

    return _str,_success,_errors

if __name__ == '__main__' :
    _msg,_s,_e = main()
    _tot = _s+_e
    _grate = 100 * _s / _tot
    print('TESTS:',_msg,'\ntests reussis: %d/%d (%.2f%%) ' % (_s,_tot,_grate) )
    print("Normalement 659/659")
    print("test_XXX(): permet de tester individuellement la methode XXX")
    print("debug_configuration(): permet de regarder des etats testés")
