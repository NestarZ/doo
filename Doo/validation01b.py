#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "mmc <marc-michel.corsini@u-bordeaux.fr>"


try:
    # changer XXXX par le nom de votre fichier
    import tp01b as tp
    # NE PAS MODIFIER CE QUI SUIT

except Exception as _e :
    print(_e)
    exit()
finally:
    try:
        from validation01a import ze_class
        from validation01a import J_ATT, J_DEF, NOIRS, ROI, BLANCS, VIDE
        from validation01a import debug_configuration, build_base
    except Exception as _e :
        print(_e)
        exit()
    from abstract import Player, manche, partie
    import inspect
    import sys

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

#---- tools ------------------------------------------------------------#
def test_Player(cls):
    _lstr = ''
    prop = issubclass(cls,Player)
    _lstr += check_property( prop )
    p = ze_class()
    _out = build_base()
    player = cls()
    
    for x in _out: # test des configurations
        p.configuration = x.cfg # charge la configuration
        if x.listeCoups == 0 : # pas de coup jouable: None
            _diag = ( player( p, x.joueur ) is None )
        else: # Coup jouable: appartenance
            _diag = ( player( p, x.joueur ) in p.listeCoups( x.joueur ) )
        _lstr += check_property( _diag )
        if cls == tp.First and x.listeCoups != 0: # cas particulier pour First
            _diag = ( player( p, x.joueur ) == p.listeCoups( x.joueur )[0] )
            _lstr += check_property( _diag )

    return _lstr

def subtest_seq( seq ):
    """
        regarde si une séquence de jeu est dans le bon format
        on ne verifie pas si les positions sont valides, juste
        si on a bien une liste de coups compatibles avec les
        contraintes
    """
    _lstr = ''
    prop = isinstance( seq, (tuple,list) )
    _lstr += check_property( prop, 'C1' )
    if _lstr[-1] == '1' : return _lstr
    prop = len(seq) > 7
    _lstr += check_property( prop, 'C2' )
    if _lstr[-1] == '2' : return _lstr
    i = 1
    for coup in seq :
        prop = (len(coup) == 2 )
        _lstr += check_property( prop, 'C3' )
        if _lstr[-1] == '3' : return _lstr
        x,y = coup
        if i < 8 : # Pose
            _possibles = list( range(12) )
            _possibles.remove(4)
            _possibles.remove(7)
            
            if i%2 == 1 : # J_ATT
                prop = (x in (ROI,NOIRS) and y in _possibles)
                _lstr += check_property( prop, 'C4' )
                if _lstr[-1] == '4' :
                    return _lstr
            else:
                prop = (x in _possibles and y in _possibles and x < y)
                _lstr += check_property( prop, 'C5' )
                if _lstr[-1] == '5' : return _lstr

        else: # Duel
            prop = x in range(12)
            prop = prop and isinstance(y, (int,list,tuple) )
            _lstr += check_property( prop, 'C6' )
            if _lstr[-1] == '6' : return _lstr
            if isinstance(y,int):
                prop = y in range(12)
            else:
                prop = True
                for _ in y: prop = prop and _ in range(12)
            _lstr += check_property( prop, 'C7' )
            if _lstr[-1] == '7' : return _lstr
            
            
            if i%2 == 1 and not isinstance(y,int): # J_ATT
                prop = len(y) == 1
            else:
                prop = True # pas de contraintes pour J_DEF

            _lstr += check_property( prop, 'C8' )
            if _lstr[-1] == '8' : return _lstr
        i += 1 # On passe au coup suivant
    return _lstr

#------ les test_XXX() -------------------------------------------------#

def test_First():
    """ permet de tester la class First """
    return test_Player( tp.First )

def test_Random():
    """ permet de tester la class Random """
    _lstr =''
    return test_Player( tp.Random )

def test_Human():
    """ permet de tester la class Humain """
    _lstr =''
    _lstr += test_Player( tp.Human )
    return _lstr
    
def test_cycling():
    """ permet de tester la détection d'un cycle """
    _datas = ( [ (1,2), (2,3), (3,1), (4,2), (1,2), (2,3) ],
               [ (1,2), (2,3), (3,[1]), (4,2), (1,2), (2,3) ],
               )
    _expect = (True, False)
    _head = ( [], [ (i,j) for i in range(3) for j in range(2) ],
              [ (i,j) for i in range(3) for j in range(3) ] )
    _lstr =''
    _args = inspect.getfullargspec( tp.cycling ).args
    _lstr += check_property( len(_args) == 1 )
    for x in _head:
        for i in range(2) :
            _lstr += check_property( tp.cycling( x+_datas[i] ) == _expect[i] )
        prop = tp.cycling(x+_datas[0]+_datas[1]) == _expect[1]
        _lstr += check_property( prop )
        prop = tp.cycling(x+_datas[1]+_datas[0]) == _expect[0]
        _lstr += check_property( prop )
    return _lstr

def test_manche():
    """ permet de tester le fonctionnement d'une manche """
    _lstr =''
    _args = inspect.getfullargspec( tp.manche ).args
    _lstr += check_property( len(_args) == 2 )
    try:
        _a = tp.manche( None, None )
    except Exception as _e:
        print( _e )
        return _lstr+'A'
    _lstr += check_property( not _a is None, 'R' )
    if 'R' == _lstr[-1]: return _lstr
    _lstr += check_property( len(_a) == 3, 'T' )
    if 'T' in _lstr : return _lstr
    try:
        p = tp.First()
    except Exception as _e:
        print(_e)
        return _lstr+'B'
    q = tp.First()
    _out = [ ]
    _args = ( ( p, None), ( None, p), ( p, p ), ( p, q ) )
    for x in _args:
        _r = tp.manche( *x )
        _out.append( _r )
        _lstr += check_property( len(_r) == 3 )
        if 'E' in _lstr : return _lstr[:-1]+"%s" % _args.index(x)
        _lstr += check_property( _a == _r )
        if 'E' in _lstr : return _lstr[:-1]+"%s" % _args.index(x)

    # Maintenant on étudie les valeurs renvoyées
    _lstr += check_property( isinstance(_a[0],int), 'M1' )
    if '1' == _lstr[-1] : return _lstr
    _lstr += check_property( isinstance(_a[1],int), 'M2' )
    if '2' == _lstr[-1] : return _lstr
    _lstr += check_property( isinstance(_a[2],(list,tuple)), 'M3' )
    if '3' == _lstr[-1] : return _lstr
    _lstr += check_property( 0 <= _a[0] <= 3, 'M4')
    if '4' == _lstr[-1] : return _lstr
    _lstr += check_property( 8 <= _a[1], 'M5' )
    if '5' == _lstr[-1] : return _lstr
    # Le compteur indique le prochain coup à jouer, pas le nombre joué
    _lstr += check_property( _a[1] == len(_a[2])+1, 'M6' )
    if '6' == _lstr[-1] : return _lstr
    _lstr += subtest_seq( _a[2] ) # controle l'historique
    return _lstr

def test_partie():
    """ permet de tester le fonctionnement d'une partie """
    _lstr =''
    _args = inspect.getfullargspec( tp.partie ).args
    _lstr += check_property( len(_args) == 3 )
    try:
        _a = tp.partie( None, None )
    except Exception as _e:
        print( _e )
        return _lstr+'A'

    # Maintenant on étudie les valeurs renvoyées
    _lstr += check_property( isinstance( _a, (tuple,list)), 'P1')
    if '1' == _lstr[-1]: return _lstr
    _lstr += check_property( len(_a) == 2, 'P2')
    if '2' == _lstr[-1]: return _lstr
    _lstr += check_property( isinstance(_a[0], (tuple,list)), 'P3')
    if '3' == _lstr[-1]: return _lstr
    _lstr += check_property( len(_a[0]) == 2, 'P4')
    if '4' == _lstr[-1]: return _lstr
    _lstr += check_property( isinstance( _a[0][0], int ) and
                             isinstance( _a[0][1], int ), 'P5')
    if '5' == _lstr[-1]: return _lstr
    ## P6 & P7 : validation impossible pour le moment
    ## _lstr += check_property( _a[0][0] != _a[0][1], 'P6')
    ## if '6' == _lstr[-1]: return _lstr
    ## _lstr += check_property( max(* _a[0]) >= 5, 'P7')
    ## if '7' == _lstr[-1]: return _lstr
    _lstr += check_property( isinstance( _a[1], dict ), 'Pa')
    if 'a' == _lstr[-1]: return _lstr
    _lstr += check_property( len( _a[1] ) %2 == 0, 'Pb')
    if 'b' == _lstr[-1]: return _lstr
    _lstr += check_property( len( _a[1] ) > 3, 'Pc')
    if 'c' == _lstr[-1]: return _lstr
    
    return _lstr

def test_replay():
    """ permet de tester le fonctionnement d'un replay """
    _lstr = ''
    _args = inspect.getfullargspec( tp.replay ).args
    _lstr += check_property( len(_args) == 1 )
    try:
        _a = tp.replay( [] )
    except Exception as _e:
        print( _e )
        return _lstr+'A'
    return _lstr

def main(human=True):
    _sep = '\n'+'_'*75#+'\n'
    _str = ''
    _attr = [ 'First', 'Random', 'Human', 'cycling', 'manche', 'partie',
              'replay' ]
    _totest = []
    for x in _attr:
        try:
            assert( hasattr(tp,x) )
            _totest.append(x) # on ne teste que ce qui est defini
            _str += '.'
        except:
            _str +='\n%s absent' % x

    _str += _sep

    if not human and 'Human' in _totest: _totest.remove('Human')
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
    # petite astuce pour éviter de tester Human
    if len(sys.argv) == 1: status = True
    else: status = False
    _msg,_s,_e = main(status)
    _tot = _s+_e
    _grate = 100 * _s / _tot
    print('TESTS:',_msg,'\ntests reussis: %d/%d (%.2f%%) ' % (_s,_tot,_grate) )
    print("Normalement _/_")
    print("test_XXX(): permet de tester individuellement la methode XXX")
    print("debug_configuration(): permet de regarder des etats testés")
