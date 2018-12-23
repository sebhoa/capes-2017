# Problème n°1

## Partie A : Généralités

### Résultats préliminaires

#### Somme 45

Pour une grille complétée, chaque ligne, chaque colonne et chaque bloc (carré 3x3) contient **exactement** les nombres 1, 2,... jusqu'à 9. Et 1 + 2 + ... + 9 = 45. Si on considère une grille de sudoku alors chaque chiffre ne pouvant apparaitre plusieurs fois, la seule autre valeur possible est le 0 et alors la somme ne fera plus 45... La réciproque est donc vraie.


#### Les fonctions `complet_...` 

Seule la fonction `ligne_complet` était demandé. C'est aussi la plus simple : on a directement une ligne avec la modélisation choisie, en liste de listes. Pour les autres il faut utiliser des compréhensions de liste où comme ci-dessous des expressions génératrices passées à la fonction `sorted` pour obtenir une liste triée à comparer avec la liste `[1, 2, 3, 4, 5, 6, 7, 8, 9]` que nous avons stockée dans la variable `DIGITS` 

```python
def ligne_complet(grille, i):
    return sum(grille[i]) == 45

def colonne_complet(grille, i):
    return sum(grille[x][i] for x in range(9)) == 45

def carre_complet(grille, i):
    row_deb = (i // 3) * 3
    row_fin = row_deb + 3
    col_deb = (i % 3) * 3
    col_fin = col_deb + 3
    return sum(grille[x][y] for y in range(col_deb, col_fin)
            for x in range(row_deb, row_fin)) == 45
```

#### La fonction `complet` 

Assez simple : pour chaque entier de 0 à 8, correspondant à un numéro de ligne, de colonne ou de bloc, cette ligne, cette colonne et ce bloc doivent être complet, sinon on retourne `False`.

```python
def complet(grille):
    for i in range(9):
        if not ligne_complet(grille, i) or\
            not colonne_complet(grille, i) or\
            not carre_complet(grille, i):
            return False
    return True
```

### Fonctions annexes

#### Fonction `ligne`

La fonction complétée :

```python
def ligne(grille, i):
    chiffre = []
    for j in range(9):
        if grille[i][j]:
            chiffre.append(grille[i][j])
    return chiffre
```

Je préfère cette version :smile: qui retourne un emsemble (`set`)
```python
def ligne(grille, i):
    return {grille[i][j] for j in range(9) if grille[i][j]}
```

Et la version pour la colonne :

```python
def colonne(grille, i):
    return {grille[j][i] for j in range(9) if grille[j][i]}
```

#### Coordonnées des blocs

`(i,j)` dans `[0;8] x [0;8]` alors `i//3` correspond à la ligne de bloc de la case `(i,j)` et `j//3` correspond à la colonne de ce bloc.

La ligne de la cellule en haut à gauche d'un bloc `ibloc, jbloc` vaut `ibloc * 3` (0, 3 ou 6) et c'est pareil pour la colonne. D'où le résultat.

#### Fonction `carre`

```python
def carre(grille, i, j):
    icoin = 3 * (i // 3)
    jcoin = 3 * (j // 3)
    chiffre = []
    for i in range (icoin, icoin + 3):
        for j in range (jcoin, jcoin + 3):
            if grille[i][j]:
                chiffre.append(grille[i][j])
    return chiffre
```

Là encore nous utiliserons plutôt cette version :

```python
def carre(grille, i, j):
    icoin = 3 * (i // 3)
    jcoin = 3 * (j // 3)
    return {grille[x][y] for y in range(jcoin, jcoin+3) 
        for x in range(icoin, icoin + 3) if grille[x][y]}
```

#### Fonction `conflit`

Avec les listes on peut faire cela comme ça :
```python
def conflit(grille, i, j):
    l_conflit = []
    l_conflit.extend(ligne(grille, i))
    l_conflit.extend(colonne(grille, j))
    l_conflit.extend(carre(grille, i, j))
    return l_conflit
```

Mais avec les ensembles, en utilisant l'union ensembliste :
```python
def conflit(grille, i, j):
    return ligne(grille, i) | colonne(grille, j) | carre(grille, i, j)
```

#### Fonction `chiffres_ok`

```python
def chiffres_ok(grille, i, j):
    ok = []
    l_conflit = conflit(grille, i, j)
    for k in DIGITS:
        if k not in l_conflit:
            ok.append (k)
    return ok
```
et la version ensembliste :

```python
SET_DIGITS = set(range(1,10))

def chiffres_ok(grille, i, j):
    return SET_DIGITS - conflit(grille, i, j)
```


## Partie B : Algorithme naïf

#### Fonction `nb_possible`

```python
def nb_possible(grille, i, j):
    return len(chiffres_ok(grille, i, j))
```

#### Fonction `un_tour`

Leur version corrigée :
```python
def un_tour(L):
    for i in range(9):
        for j in range(9):
            if L[i][j] == 0:
                if nb_possible(L, i, j) == 1:
                    L[i][j] = chiffres_ok(L, i, j)[0]
                    return True
    return False
```
Je préfère la mienne où on ne calcule pas deux fois les `chiffres_ok` 

```python
def un_tour(grille):
    for i in range(9):
        for j in range(9):
            if grille[i][j] == 0:
                candidats = chiffres_ok(grille, i, j)
                if len(candidats) == 1:
                    grille[i][j] = candidats[0]
                    return True
    return False
```

#### Fonction `complete`

```python
def complete(grille):
    changement = True
    while changement:
        changement = un_tour(grille)
    return complet(grille)
```

## Partie C : Backtracking

#### Case suivante

```python
def case_suivante(pos):
    x, y = pos
    y += 1
    if y == 9:
        y = 0
        x += 1
    return x, y
```

#### Backtracking

```python
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
```

#### Appels à `Backtracking`

Nous avons 81 - p cases à remplir. Si la solution est la dernière configuration testée alors nous aurons appelé `n0` fois la fonction `backtracking` pour résoudre la grille sauf la première case vide. Où `n0` est le nombre de possibilités pour la première case. Nous aurons `n1` possibilités pour la 2e case vide traitée soit `n0 * n1` appels pour ces 2 cases. Ainsi de suite pour les 81 - p cases au total.

Chacun de `n_i` étant inférieur ou égal à 9, on obtient une majoration de `9^{81 - p}` pour le nombre d'appels à la fonction `Backtracking`. 

#### Retour
 
```python
def solution_sudoku(L):
    return backtracking(L, [0 ,0])
```

La fonction `solution_sudoku` retourne `True` si la grille a plusieurs solution (`L` sera instanciée à la première solution trouvée). On obtient une solution en partant d'une grille vide.


# Problème n°2



