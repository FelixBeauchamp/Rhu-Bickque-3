import ArduinoCom
import OpenRBCom
# import traitement_image

import sys
import os

algo_cube_path = os.path.join(sys.path[1], "Algo_CFOP")
print(algo_cube_path)
sys.path.append(algo_cube_path)

from Algo_CFOP import solver, cube


def mapping_sequence():
    mapp = []
    # Iterate through the camera motor sequence and analizing the
    for move in solver.sequence_camera:
        if move[0] == 'M':
            OpenRBCom.sendmessage(move)
        elif move[0] == 'S':
            temp = traitement_image.faceofdacube()
            mapp.extend(temp)
        else:
            ArduinoCom.sendmessage(move)
    map_array = solver.reformat(mapp)
    cb = cube.Cube(map_array)
    print(cb)
    return map_array


def solving(map_array):
    c = cube.Cube(map_array)
    print("Solving:\n", c)
    solution = solver.Solver(c)
    solution.solveCube(optimize=True)
    moves = solution.getMoves(decorated=True)
    print(moves)

    moves_list = solver.Solver.reformat(moves)
    print(f"{len(moves_list)} moves: {' '.join(moves_list)}")
    solution.translate(moves_list)
    print(f"{len(solution.sequence_motors)} moves: {' '.join(solution.sequence_motors)}")

    for moves in solution.sequence_motors:
        if moves[0] == 'M' or moves[0] == 'H':
            OpenRBCom.sendmessage(moves)
        else:
            ArduinoCom.sendmessage(moves)


if __name__ == '__main__':
    # # 0- Initialisation
    # print("Initialisation: OPENING/HOMING")
    # OpenRBCom.openport()
    # ArduinoCom.openportarduino()
    # ArduinoCom.sendmessage('OXOY')
    # OpenRBCom.sendmessage('HOMING')
    #
    # # 1- Wait for user input before clamping the cube
    # input("Press Enter to clamp the cube")
    # ArduinoCom.sendmessage('CXCY')
    #
    # # 2- Starting the mapping sequence
    # input("Press Enter to start the mapping sequence")
    # cube_map = mapping_sequence()
    #
    # # 2- Solving the cube
    # input("Press Enter to start solving")
    #
    # solving(cube_map)
    # ArduinoCom.closeportarduino()
    # OpenRBCom.closeport()

    print("Initialisation: OPENING/HOMING")
    OpenRBCom.openport()
    ArduinoCom.openportarduino()
    cb = cube.Cube()
    balls = solver.Solver(cb)
    for moves in balls.Dictio:
        input("Movement: " + moves)
        ArduinoCom.sendmessage('OXOY')
        OpenRBCom.sendmessage('HOMING')
        sequence = balls.Dictio[moves]
        sequence_motors = []
        for j in range(len(sequence)):
            sequence_motors.extend(balls.servo[sequence[j]])
        for marde in sequence_motors:
            input("next movement: " + marde)
            if marde[0] == 'M' or marde[0] == 'H':
                OpenRBCom.sendmessage(marde)
            else:
                ArduinoCom.sendmessage(marde)
    ArduinoCom.closeportarduino()
    OpenRBCom.closeport()
