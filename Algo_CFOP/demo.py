from cube import Cube
from solver import Solver
from helper import getScramble

# cb = Cube()
cb = Cube([[['W', 'O', 'W'], ['B', 'O', 'G'], ['Y', 'O', 'Y']], [['B', 'B', 'B'], ['W', 'W', 'W'], ['G', 'G', 'G']],
           [['Y', 'R', 'Y'], ['B', 'R', 'G'], ['W', 'R', 'W']], [['B', 'B', 'B'], ['Y', 'Y', 'Y'], ['G', 'G', 'G']],
           [['O', 'W', 'R'], ['O', 'G', 'R'], ['O', 'Y', 'R']], [['R', 'W', 'O'], ['R', 'B', 'O'], ['R', 'Y', 'O']]])
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
