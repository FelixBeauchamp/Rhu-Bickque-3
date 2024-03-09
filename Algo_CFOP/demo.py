from cube import Cube
from solver import Solver
from helper import getScramble

# cb = Cube()
cb = Cube([[['B', 'G', 'O'], ['R', 'G', 'Y'], ['W', 'R', 'R']], [['G', 'Y', 'W'], ['B', 'O', 'B'], ['Y', 'O', 'B']],
           [['G', 'G', 'W'], ['W', 'B', 'G'], ['Y', 'O', 'G']], [['R', 'O', 'O'], ['R', 'R', 'B'], ['Y', 'R', 'B']],
           [['O', 'Y', 'G'], ['W', 'W', 'B'], ['O', 'G', 'R']], [['B', 'W', 'R'], ['W', 'Y', 'O'], ['Y', 'Y', 'W']]])
#  5
# 3012
#  4
# scramble = getScramble(10)
# print("Scramble:", scramble)
# cb.doMoves(scramble)

print(cb)

solver = Solver(cb)
solver.solveCube(optimize=True)
moves = solver.getMoves(decorated=True)
print(moves)

moves_list = Solver.reformat(moves)
print(f"{len(moves_list)} moves: {' '.join(moves_list)}")
solver.translate(moves_list)
print(f"{len(solver.sequence_motors)} moves: {' '.join(solver.sequence_motors)}")
