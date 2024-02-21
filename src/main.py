# import ArduinoCom
# import OpenRBCom
import sys
print(sys.path)
sys.path.append('C:\\Users\\Poste\\Desktop\\Sessions GRO_UdeS\\S4_GRO\\Projet\\Code\\Rhu-Bickque-3\\Algo_Cube')

from Algo_Cube import solve



def mapping_sequence():
    mapp = ['G', 'B', 'G', 'B', 'G', 'B', 'G', 'B', 'G', 'O', 'R', 'O', 'R', 'O', 'R', 'O', 'R', 'O', 'B', 'G', 'B', 'G', 'B', 'G', 'B', 'G', 'B', 'R', 'O', 'R', 'O', 'R', 'O', 'R', 'O', 'R', 'Y', 'W', 'Y', 'W', 'Y', 'W', 'Y', 'W', 'Y', 'W', 'Y', 'W', 'Y', 'W', 'Y', 'W', 'Y', 'W']
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
    print(stg[0:2]+'\n'+stg[3:5]+'\n'+stg[6:8]+'\n'+stg[9:20]+'\n'+stg[21:32]+'\n'+stg[33:44]+'\n'+stg[45:47]+'\n'+stg[48:50]+'\n'+stg[51:53])
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
