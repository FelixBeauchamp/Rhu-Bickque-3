import ArduinoCom
import OpenRBCom

import sys
import os

algo_cube_path = os.path.join(sys.path[1], "Algo_Cube")
print(algo_cube_path)
sys.path.append(algo_cube_path)

from Algo_Ass import solve, cube, optimize


def mapping_sequence():
    mapp = ['G', 'B', 'G', 'B', 'G', 'B', 'G', 'B', 'G', 'O', 'R', 'O', 'R', 'O', 'R', 'O', 'R', 'O', 'B', 'G', 'B',
            'G', 'B', 'G', 'B', 'G', 'B', 'R', 'O', 'R', 'O', 'R', 'O', 'R', 'O', 'R', 'Y', 'W', 'Y', 'W', 'Y', 'W',
            'Y', 'W', 'Y', 'W', 'Y', 'W', 'Y', 'W', 'Y', 'W', 'Y', 'W']
    for move in solve.sequence_camera:
        if move[0] == 'M':
            OpenRBCom.sendmessage(move)
        elif move[0] == 'S':
            # call fonction camera
            # add face map to the map list
            print("SNAP")
        else:
            ArduinoCom.sendmessage(move)
    stg = solve.reformat(mapp)
    print(stg)
    print('   ' + stg[0:3] + '\n   ' + stg[3:6] + '\n   ' + stg[6:9] + '\n' + stg[9:21] + '\n' + stg[21:33] + '\n' +
          stg[33:45] + '\n   ' + stg[45:48] + '\n   ' + stg[48:51] + '\n   ' + stg[51:])
    return stg


def solving(map_string):
    c = cube.Cube(map_string)
    print("Solving:\n", c)
    orig = cube.Cube(c)
    solver = solve.Solver(c)
    solver.solve()
    solver.moves = optimize.optimize_moves(solver.moves)
    solver.translate()
    print(f"{len(solver.moves)} moves: {' '.join(solver.moves)}")
    print(f"{len(solver.sequence_motors)} motors moves: {' - '.join(solver.sequence_motors)}")

    for moves in solver.sequence_motors:
        if moves[0] == 'M' or moves[0] == 'H':
            OpenRBCom.sendmessage(moves)
        else:
            ArduinoCom.sendmessage(moves)


if __name__ == '__main__':
    # 0- Initialisation
    print("Initialisation: OPENING/HOMING")
    OpenRBCom.openport()
    ArduinoCom.openportarduino()
    ArduinoCom.sendmessage('OXOY')
    OpenRBCom.sendmessage('HOMING')

    # 1- Wait for user input before clamping the cube
    input("Press Enter to clamp the cube")
    ArduinoCom.sendmessage('CXCY')

    # 2- Starting the mapping sequence
    input("Press Enter to start the mapping sequence")
    cube_map = mapping_sequence()

    # 2- Solving the cube
    input("Press Enter to start solving")

    solving(cube_map)
    ArduinoCom.closeportarduino()
    OpenRBCom.closeport()
