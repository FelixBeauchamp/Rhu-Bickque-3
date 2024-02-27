# import ArduinoCom
# import OpenRBCom

import sys
import os

algo_cube_path = os.path.join(sys.path[1], "Algo_Cube")
print(algo_cube_path)
sys.path.append(algo_cube_path)

from Algo_Cube import solve


def mapping_sequence():
    mapp = ['G', 'B', 'G', 'B', 'G', 'B', 'G', 'B', 'G', 'O', 'R', 'O', 'R', 'O', 'R', 'O', 'R', 'O', 'B', 'G', 'B',
            'G', 'B', 'G', 'B', 'G', 'B', 'R', 'O', 'R', 'O', 'R', 'O', 'R', 'O', 'R', 'Y', 'W', 'Y', 'W', 'Y', 'W',
            'Y', 'W', 'Y', 'W', 'Y', 'W', 'Y', 'W', 'Y', 'W', 'Y', 'W']
    for move in solve.sequence_camera:
        if move[0] == 'M':
            # OpenRBCom.sendtoRB(move)
            print("cum")
        elif move[0] == 'S':
            # call fonction camera
            print("cum")
        else:
            # ArduinoCom.sendtomega(move)
            print("cum")
    stg = solve.reformat(mapp)
    print(stg)
    print('   ' + stg[0:3] + '\n   ' + stg[3:6] + '\n   ' + stg[6:9] + '\n' + stg[9:21] + '\n' + stg[21:33] + '\n' +
          stg[33:45] + '\n   ' + stg[45:48] + '\n   ' + stg[48:51] + '\n   ' + stg[51:])
    return stg


if __name__ == '__main__':
    # 0- Initialisation
    print("Initialisation: OPENING/HOMING")
    # ArduinoCom.sendtomega('OXOY')
    # OpenRBCom.sendtoRB('HOMING')

    # 1- Wait for user input before clamping the cube
    input("Press Enter to clamp the cube")
    # ArduinoCom.sendtomega('CXCY')

    # 2- Starting the mapping sequence
    input("Press Enter to start the mapping sequence")
    mapping_sequence()
