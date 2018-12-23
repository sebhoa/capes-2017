#! /usr/bin/env python3

"""
Résolution exos info du CAPES 2017
Auteur : Sébastien Hoarau
Date   : 2018.12.23
"""

# ----------------------------------
# --
# -- PROBLEME I
# --
# ----------------------------------

DIGITS = list(range(1,10))
SET_DIGITS = set(range(1,10))

# --
# -- PARTIE A
# --

def ligne_complet(grille, i):
    return sorted(grille[i]) == DIGITS

def colonne_complet(grille, i):
    return sorted(grille[x][i] for x in range(9)) == DIGITS

def carre_complet(grille, i):
    row_deb = (i // 3) * 3
    row_fin = row_deb + 3
    col_deb = (i % 3) * 3
    col_fin = col_deb + 3
    return sorted(grille[x][y] for y in range(col_deb, col_fin)
            for x in range(row_deb, row_fin)) == DIGITS

def complet(grille):
    for i in range(9):
        if not ligne_complet(grille, i) or\
            not colonne_complet(grille, i) or\
            not carre_complet(grille, i):
            return False
    return True


def ligne(grille, i):
    return {grille[i][j] for j in range(9) if grille[i][j]}

# La version pour  le CAPES
#
# def ligne(grille, i):
#     chiffre = []
#     for j in range(9):
#         if grille[i][j]:
#             chiffre.append(grille[i][j])
#     return chiffre


def colonne(grille, i):
    return {grille[j][i] for j in range(9) if grille[j][i]}


# La version pour le CAPES
#
# def carre(grille, i, j):
#     icoin = 3 * (i // 3)
#     jcoin = 3 * (j // 3)
#     chiffre = []
#     for i in range (icoin, icoin + 3):
#         for j in range (jcoin, jcoin + 3):
#             if grille[i][j]:
#                 chiffre.append(grille[i][j])
#     return chiffre


def carre(grille, i, j):
    icoin = 3 * (i // 3)
    jcoin = 3 * (j // 3)
    return {grille[x][y] for y in range(jcoin, jcoin+3) 
        for x in range(icoin, icoin + 3) if grille[x][y]}
 
# La version pour le CAPES
#
# def conflit(grille, i, j):
#     l_conflit = []
#     l_conflit.extend(ligne(grille, i))
#     l_conflit.extend(colonne(grille, j))
#     l_conflit.extend(carre(grille, i, j))
#     return l_conflit

def conflit(grille, i, j):
    return ligne(grille, i) | colonne(grille, j) | carre(grille, i, j)

# version CAPES
#
# def chiffres_ok(grille, i, j):
#     ok = []
#     l_conflit = conflit(grille, i, j)
#     for k in DIGITS:
#         if k not in l_conflit:
#             ok.append (k)
#     return ok

def chiffres_ok(grille, i, j):
    return SET_DIGITS - conflit(grille, i, j)

# --
# -- PARTIE B
# --


def nb_possible(grille, i, j):
    return len(chiffres_ok(grille, i, j))


def un_tour(grille):
    for i in range(9):
        for j in range(9):
            if grille[i][j] == 0:
                candidats = chiffres_ok(grille, i, j)
                if len(candidats) == 1:
                    grille[i][j] = candidats[0]
                    return True
    return False


def complete(grille):
    changement = True
    while changement and not complet(grille):
        changement = un_tour(grille)
    return changement


# --
# -- PARTIE C
# --


def case_suivante(pos):
    x, y = pos
    y += 1
    if y == 9:
        y = 0
        x += 1
    return [x, y]



def aff(g):
    for l in g:
        print(l)
    input('Press return')

def backtracking(grille, pos):
    """
    pos est une liste d´e signant une case du sudoku ,
    [0 ,0] pour le coin en haut `a gauche .
    """
    if pos == [9, 0] :
        return True
    else:
        i, j = pos
        if grille[i][j]:
            return backtracking(grille, case_suivante(pos))
        else:
            for k in chiffres_ok(grille, i, j):
                grille[i][j] = k
                if backtracking(grille, case_suivante(pos)):
                    return True
            grille[i][j] = 0
            return False



M= [[2, 0, 0, 0, 9, 0, 3, 0, 0], [0, 1, 9, 0, 8, 0, 0, 7, 4],
[0, 0, 8, 4, 0, 0, 6, 2, 0], [5, 9, 0, 6, 2, 1, 0, 0, 0],
[0, 2, 7, 0, 0, 0, 1, 6, 0], [0, 0, 0, 5, 7, 4, 0, 9, 3],
[0, 8, 5, 0, 0, 9, 7, 0, 0], [9, 3, 0, 0, 5, 0, 8, 4, 0],
[0, 0, 2, 0, 6, 0, 0, 0, 1]]

VIDE = [[0] * 9 for _ in range(9)]

G =  [[0,6,0,0,0,0,2,0,5],[4,0,0,9,2,1,0,0,0],
[0,7,0,0,0,8,0,0,1],[0,0,0,0,0,5,0,0,9],
[6,4,0,0,0,0,0,7,3],[1,0,0,4,0,0,0,0,0],
[3,0,0,7,0,0,0,6,0],[0,0,0,1,4,6,0,0,2],
[2,0,6,0,0,0,0,1,0]]

# print(chiffres_ok(M, 0, 1))

backtracking(VIDE, [0,0])
aff(VIDE)
