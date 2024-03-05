from cube import Cube
from solver import Solver
from helper import getScramble

# cb = Cube()
cb = Cube([[['G', 'G', 'B'], ['B', 'B', 'W'], ['R', 'R', 'R']], [['Y', 'B', 'Y'], ['R', 'R', 'O'], ['W', 'O', 'B']],
           [['G', 'R', 'W'], ['G', 'G', 'B'], ['W', 'B', 'Y']], [['O', 'O', 'W'], ['R', 'O', 'O'], ['R', 'G', 'G']],
           [['Y', 'G', 'B'], ['W', 'W', 'Y'], ['B', 'Y', 'O']], [['G', 'Y', 'O'], ['W', 'Y', 'W'], ['R', 'Y', 'O']]])

"""
scramble = getScramble(10)
print("Scramble:", scramble)
cb.doMoves(scramble)
"""
print(cb)

solver = Solver(cb)
solver.solveCube(optimize=True)
moves = solver.getMoves(decorated=True)
print(moves)

moves_list = Solver.reformat(moves)
print(f"{len(moves_list)} moves: {' '.join(moves_list)}")
solver.translate(moves_list)
print(f"{len(solver.sequence_motors)} moves: {' '.join(solver.sequence_motors)}")

# simplifier les duoR R → Ri
