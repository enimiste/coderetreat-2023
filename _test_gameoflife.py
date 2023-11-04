# Coderetreat @2023 - Arolla

# vivant + <=1     voisin  ----> Meurt
# vivant + >=4     voisins ----> Meurt
# vivant + {2, 3}  voisins ----> Conserve son statut
# vide   + 3       voisins ----> Survit
# Business
NEXT_STATE = {
    0: (lambda _ : 0),
    1: (lambda _ : 0),
    2: (lambda ost : ost),
    3: (lambda _ : 1),
    4: (lambda _ : 0),#>=4
    5: (lambda _ : 0),#>=4
    6: (lambda _ : 0),#>=4
    7: (lambda _ : 0),#>=4
    8: (lambda _ : 0),#>=4
}
def neigbours_count(board, i, j):
    count = 0
    dir = [-1, 0, 1]
    for k in dir:
        for p in dir:
            r = i+k
            c = j+p
            if r>=0 and c>=0 and r<len(board) and c<len(board[0]) and (k, p)!=(0,0):
                count += board[r][c]
    """
    neigbours = [[i, j-1], [i-1, j-1], [i-1, j], [i-1, j+1], [i, j+1], [i+1, j+1], [i+1, j], [i+1, j-1]]
    for r, c in neigbours:
        if r>=0 and c>=0 and r<len(board) and c<len(board[0]):
            count += board[r][c]
     """
    return count

def cell_next_state(board, i, j):
    return NEXT_STATE[neigbours_count(board, i, j)](board[i][j])

def game_of_life(board):
    new_board = []
    i=0
    for r in board:
        j=0
        new_row = []
        new_board.append(new_row)
        for c in r:
            new_row.append(cell_next_state(board, i, j))
            j += 1
        i += 1
    return new_board

""" 
def game_of_life(board):
    count = sum(map(lambda x : sum(x), board))
    if count<=2:
        return list(map(lambda x : list(map(lambda y: 0, x)), board))
    if len(board) == 2:
        if count >= 3:
            return [[1, 1], [1, 1]]
        else:
            return list(map(lambda x : list(map(lambda y: 0, x)), board))
    if len(board) == 3:
        if count == 1:
            return list(map(lambda x : list(map(lambda y: 0, x)), board))
    return board
"""
# Tests
def test_dummy():
    assert True

def test_empty_board_neigbours_count():
    board = []
    assert neigbours_count(board, 0, 0)==0

def test_4_cells_empty_board_neigbours_count():
    board = [[0, 0], [0, 0]]
    assert neigbours_count(board, 0, 0)==0
    assert neigbours_count(board, 1, 0)==0
    assert neigbours_count(board, 0, 1)==0
    assert neigbours_count(board, 1, 1)==0

def test_4_cells_board_with_2_cell_surv_neigbours_count():
    board = [[0, 1], 
             [1, 0]]
    assert neigbours_count(board, 0, 0)==2
    assert neigbours_count(board, 1, 0)==1
    assert neigbours_count(board, 0, 1)==1
    assert neigbours_count(board, 1, 1)==2

def test_empty_board_one_cell():
    board = []
    new_board = game_of_life(board)
    assert len(new_board)==0


def test_empty_board_4_cells():
    board = [[0, 0], [0, 0]]
    new_board = game_of_life(board)
    assert new_board==board

def test_1_cell_surv_board_4_cells():
    board = [[1, 0], [0, 0]]
    new_board = game_of_life(board)
    assert new_board==[[0, 0], [0, 0]]

def test_2_cell_surv_board_4_cells():
    board = [[1, 1], [0, 0]]
    new_board = game_of_life(board)
    assert new_board==[[0, 0], [0, 0]]

def test_3_cell_surv_board_4_cells():
    board = [[1, 1], [1, 0]]
    new_board = game_of_life(board)
    assert new_board==[[1, 1], [1, 1]]

def test_4_cell_surv_board_4_cells():
    board = [[1, 1], [1, 1]]
    new_board = game_of_life(board)
    assert new_board==[[1, 1], [1, 1]]

def test_empty_board_9_cells():
    board = [[0, 0, 0], 
             [0, 0, 0],
             [0, 0, 0]]
    new_board = game_of_life(board)
    assert new_board==board


def test_empty_board_9_cells():
    board = [[1, 0, 0], 
             [0, 0, 0],
             [0, 0, 0]]
    new_board = game_of_life(board)
    assert new_board==[[0, 0, 0], 
                        [0, 0, 0],
                        [0, 0, 0]]
    
def test_3_cells_surv_board_9_cells():
    board = [[1, 0, 0], 
             [1, 1, 0],
             [0, 0, 0]]
    new_board = game_of_life(board)
    assert new_board==[[1, 1, 0], 
                        [1, 1, 0],
                        [0, 0, 0]]
    
def test_4_cells_surv_board_9_cells():
    board = [[1, 1, 0], 
             [1, 1, 0],
             [0, 0, 0]]
    new_board = game_of_life(board)
    assert new_board==[[1, 1, 0], 
                        [1, 1, 0],
                        [0, 0, 0]]
    
def test_2_cells_surv_board_9_cells():
    board = [[1, 0, 0], 
             [1, 0, 0],
             [0, 0, 0]]
    new_board = game_of_life(board)
    assert new_board==[[0, 0, 0], 
                        [0, 0, 0],
                        [0, 0, 0]]

    