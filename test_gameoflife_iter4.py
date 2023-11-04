# Coderetreat @2023 - Arolla

# vivant + <=1     voisin  ----> Meurt
# vivant + >=4     voisins ----> Meurt
# vivant + {2, 3}  voisins ----> Conserve son statut
# vide   + 3       voisins ----> Survit
# Business
# Il nous a demandé de modéliser la grille :
# - en gardant uniquement les cellules vivantes
# - rille sans bornes
NEXT_STATE = {
    0: (lambda _ : False),
    1: (lambda _ : False),
    2: (lambda ost : ost),
    3: (lambda _ : True),
    5: (lambda _ : False),#>=4
    4: (lambda _ : False),#>=4
    6: (lambda _ : False),#>=4
    7: (lambda _ : False),#>=4
    8: (lambda _ : False),#>=4
}
def neigbours_count(board: set[(int, int)], i: int, j: int) -> int:
    """
    pour chaque cellules vivantes tester sur le set l'existance des voisin (i, j-1), ....
    à chaque existance on ajoute 1 au count.
    """
    count = 0
    dif = [-1, 0, 1]
    for r in dif:
        for c in dif:
            if (i+r, j+c)!=(i,j) and (i+r, j+c) in board:
                count += 1
    return count

def cell_next_state(board: set[(int, int)], i: int, j: int) -> bool :
    fn = NEXT_STATE[neigbours_count(board, i, j)]#est une fonction
    old_state = (i, j) in board
    return fn(old_state)

def find_spawn_candidat(board: set[(int, int)]) -> set((int, int)):
    res = set()
    dif = [-1, 0, 1]
    for (i,j) in board:
        # 1 : found candidat cells around the current cell (i, j)
        candidat = set()
        for r in dif:
            for c in dif:
                cell = (i+r, j+c)
                if cell!=(i,j):
                    candidat.add(cell)
        # 2 : check for each candidat cell its next_state
        for (ii, jj) in candidat:
            if (ii, jj) not in board and cell_next_state(board, ii, jj):
                res.add((ii, jj))
    return res

def game_of_life(board: set[(int, int)]) -> set[(int, int)]:
    """
    board : est un ensemble des coordonnées (i,j) des cellules vivantes
    """
    xs = set([(i, j)  for (i, j) in board if cell_next_state(board, i, j)])
    return xs.union(find_spawn_candidat(board))


# Tests
def test_dummy():
    assert True

def test_4_cells_empty_board_neigbours_count():
    board = set()# non surv cell
    assert neigbours_count(board, 0, 0)==0

def test_4_cells_board_with_2_cell_surv_neigbours_count():
    """
    . #
    # .
    """
    board = set([(0, 1), 
             (1, 0)])
    assert neigbours_count(board, 0, 0)==2
    assert neigbours_count(board, 1, 0)==1
    assert neigbours_count(board, 0, 1)==1
    assert neigbours_count(board, 1, 1)==2

def test_find_spawn_candidat_empty_baord():
    board = set()
    spanw_candidat = find_spawn_candidat(board)
    assert spanw_candidat==set()

def test_find_spawn_candidat_not_empty_baord():
    """
    . . .
    # . .
    . # #
    """
    board = set([(1,0), (2, 1), (2, 2)])
    spanw_candidat = find_spawn_candidat(board)
    assert spanw_candidat==set([(1, 1)])

def test_empty_board():
    board = set()
    new_board = game_of_life(board)
    assert new_board==board

def test_1_cell_surv_board():
    """
    #
    """
    board = set([(1, 0)])
    new_board = game_of_life(board)
    assert new_board==set()

def test_2_cell_surv_board():
    """
    # #
    """
    board = set([(0, 0), (0, 1)])
    new_board = game_of_life(board)
    assert new_board==set()

def test_3_cell_surv_board():
    """
    # #
    # .
    """
    board = set([(0, 0), (0, 1), (1, 0)])
    new_board = game_of_life(board)
    """
    # #
    # #
    """
    assert new_board==set([(0, 0), (0, 1), (1, 0), (1, 1)])

def test_4_cell_surv_board():
    """
    # #
    # #
    """
    board = set([(0, 0), (0, 1), (1, 0), (1, 1)])
    new_board = game_of_life(board)
    assert new_board==set([(0, 0), (0, 1), (1, 0), (1, 1)])

def test_2_cells_surv_board():
    """
    # . .
    . # .
    . . .
    """
    board = set([(0,0), (1, 0)])
    new_board = game_of_life(board)
    assert new_board==set()

def test_3_cells_surv_board():
    """
    . . .
    # . .
    . # #
    """
    board = set([(1,0), (2, 1), (2, 2)])
    new_board = game_of_life(board)
    """
    . . .
    . # .
    . # .
    """
    assert new_board==set([(1, 1), (2, 1)])
    new_board = game_of_life(new_board)
    assert new_board==set()

def test_9_cells_surv_board():
    """
    . . . . .
    . # # # .
    . # # # .
    . # # # .
    . . . . .
    """
    board = set([(i, j) for i in range(3) for j in range(3)])
    new_board = game_of_life(board)

    """
    . . # . .
    . # . # .
    # . . . #
    . # . # .
    . . # . .
    """
    assert new_board==set([(0, 0), (3, 1), 
                            (-1, 1), (2, 0), 
                            (1, -1), (0, 2), 
                            (2, 2), (1, 3)])