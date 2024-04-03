import ArduinoCom
import OpenRBCom
import traitement_image
import keyboard
import time

import sys
import os

algo_cube_path = os.path.join(sys.path[1], "Algo_CFOP")
print(algo_cube_path)
sys.path.append(algo_cube_path)

from Algo_CFOP import solver, cube

port_Arduino = 'COM7'
port_OpenRB = 'COM6'


def initialisation():
    print("Initialisation: OPENING/HOMING")
    OpenRBCom.openport(port_OpenRB)
    ArduinoCom.openportarduino(port_Arduino)
    ArduinoCom.sendmessage('OXOY')
    time.sleep(4)
    OpenRBCom.sendmessage('HOMING')


def clamp():
    print("Press Enter to clamp the cube")
    ArduinoCom.sendmessage('CXCY')


def mapping_sequence():
    print("Press Enter to start the mapping sequence")
    mapp = ['O', 'B', 'B', 'G', 'G', 'Y', 'O', 'G', 'R', 'W', 'B', 'W', 'Y', 'W', 'G', 'B', 'W', 'W',
            'B', 'B', 'Y', 'O', 'B', 'B', 'G', 'Y', 'G', 'G', 'R', 'B', 'W', 'Y', 'G', 'R', 'O', 'G',
            'R', 'R', 'Y', 'W', 'O', 'W', 'Y', 'R', 'Y', 'O', 'Y', 'O', 'O', 'R', 'R', 'W', 'O', 'R']

    # Iterate through the camera motor sequence and analizing the
    # mapp = []
    # for move in solver.sequence_camera:
    #     if move[0] == 'M':
    #         OpenRBCom.sendmessage(move)
    #     elif move[0] == 'S':
    #         print('SNAP')
    #         temp = traitement_image.faceofdacube()
    #         mapp.extend(temp)
    #     else:
    #         ArduinoCom.sendmessage(move)
    # print(mapp)
    map_array = solver.reformat(mapp)
    c = cube.Cube(map_array)
    print("Solving:\n")
    print(c)
    return map_array


def solving_moves(map_array):
    c = cube.Cube(map_array)
    print("Solving:\n", c)
    solution = solver.Solver(c)
    solution.solveCube(optimize=True)
    mov = solution.getMoves(decorated=True)
    print(mov)

    moves_list = solver.Solver.reformat(mov)
    print(f"{len(moves_list)} moves: {' '.join(moves_list)}")
    array_of_arrays = solution.translate(moves_list)
    print(f"{len(solution.sequence_motors)} moves: {' '.join(solution.sequence_motors)}")

    MEGA_MOVES = [moves_list, solution.sequence_motors, array_of_arrays]
    input(MEGA_MOVES)
    return MEGA_MOVES


def do_move(move):
    print(move)
    if move[0] == 'M' or move[0] == 'H':
        OpenRBCom.sendmessage(move)
    else:
        ArduinoCom.sendmessage(move)


def close_ports():
    ArduinoCom.sendmessage('OXOY')
    ArduinoCom.closeportarduino()
    OpenRBCom.closeport()


if __name__ == '__main__':
    input("MEGAWHAAAT")
    initialisation()
    clamp()
    deez = mapping_sequence()
    balls = solving_moves(deez)
    for dicks in balls:
        do_move(dicks)
    close_ports()

    # print("Initialisation: OPENING/HOMING")
    # OpenRBCom.openport(port_OpenRB)
    # ArduinoCom.openportarduino(port_Arduino)
    # cb = cube.Cube()
    # balls = solver.Solver(cb)
    # # Flag to track if 'p' key has been pressed
    # p_pressed = False
    # g_pressed = False
    # input("bibos ass")
    # ArduinoCom.sendmessage('OXOY')
    # input("bibos dick")
    # OpenRBCom.sendmessage('HOMING')
    # for moves in balls.Dictio:
    #     print("\n Movement: " + moves)
    #     p_pressed = False
    #     g_pressed = False
    #     while not g_pressed and not p_pressed:
    #         if keyboard.is_pressed('g'):
    #             g_pressed = True
    #             # print("bibos ass")
    #             # ArduinoCom.sendmessage('OXOY')
    #             # print("bibos dick")
    #             # OpenRBCom.sendmessage('HOMING')
    #             sequence = balls.Dictio[moves]
    #             sequence_motors = []
    #             for j in range(len(sequence)):
    #                 sequence_motors.extend(balls.servo[sequence[j]])
    #             for marde in sequence_motors:
    #                 input("Motor: " + marde)
    #                 if marde[0] == 'M' or marde[0] == 'H':
    #                     OpenRBCom.sendmessage(marde)
    #                 else:
    #                     ArduinoCom.sendmessage(marde)
    #             time.sleep(0.5)
    #         elif keyboard.is_pressed('p'):
    #             p_pressed = True
    #             time.sleep(0.25)
    # ArduinoCom.closeportarduino()
    # OpenRBCom.closeport()
