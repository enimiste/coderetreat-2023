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

def draw_with_dim(board: set[(int, int)], row_bounds: (int, int), columns_bounds: (int, int)) -> list[str]:
    if row_bounds is None or columns_bounds is None:
        return list()
    res = list()
    for i in range(row_bounds[0], row_bounds[1]+1):
        line = list()
        for j in range(columns_bounds[0], columns_bounds[1]+1):
            if (i, j) in board:
                line.append(" @ ")
            else:
                line.append(" . ")
        res.append("".join(line))
    return res

def draw(board: set[(int, int)]) -> (list[str], (int, int), (int, int)):
    if len(board)==0:
       return (list(), (0,0), (0,0))
    for c in board:
        first = c
        break
    row_bounds = [first[0], first[0]]#(min, max)
    columns_bounds = [first[1], first[1]]
    for (i, j) in board:
        if i<row_bounds[0]:
            row_bounds[0]=i
        elif i>row_bounds[1]:
            row_bounds[1]=i
        if j<columns_bounds[0]:
            columns_bounds[0]=j
        elif j>columns_bounds[1]:
            columns_bounds[1]=j
    row_bounds[0] -= 1
    row_bounds[1] += 1
    columns_bounds[0] -= 1
    columns_bounds[1] += 1
    return (draw_with_dim(board, row_bounds, columns_bounds), row_bounds, columns_bounds)

def main():
    import random
    import os
    from time import sleep
    import signal
    import sys

    def signal_handler(signal, frame):
        print("")
        print('You pressed Ctrl+C!')
        sys.exit(0)

    def reset_drawing(iteration):
        os.system("clear")
        print("Game Of Life (Iter=" + str(iteration) + ", Speed=1sec) :")
        print("")
        print("")

    signal.signal(signal.SIGINT, signal_handler)

    board = set([(i, j) for i in range(10) for j in range(10) if random.random()>0.5])
    #board = set([(i, j) for i in range(3) for j in range(3)])
    iteration = 1

    max_line = 0
    while True:
        lines, row_bounds, columns_bounds = draw(board)
        reset_drawing(iteration)
        for line in lines:
            print(line)
    
        board = game_of_life(board)
        if len(board)==0:
            """
            To keep the last empty grid on screen
            """
            reset_drawing(iteration)
            lines = draw_with_dim(board, row_bounds, columns_bounds)
            for line in lines:
                print(line)
            print("")
            print("Game over")
            break
        max_line = max(max_line, len(lines))
        for _ in range(0, max_line-len(lines)+1):
            print("")
        iteration += 1
        sleep(1)

if __name__ == "__main__":
    main()