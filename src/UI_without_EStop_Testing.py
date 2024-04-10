moves = dict(F=['M1_R'], duoF=['M1_180'], Fi=['M1_L'], duoFi=['M1_180'], R=['M4_R'], duoR=['M4_180'],
             Ri=['M4_L'], duoRi=['M4_180'], U=['M2M4_L_F', 'M3_L', 'M2M4_R_F'],
             duoU=['M2M4_L_F', 'M3_180', 'M2M4_R_F'], Ui=['M2M4_L_F', 'M3_R', 'M2M4_R_F'],
             duoUi=['M2M4_L_F', 'M3_180', 'M2M4_R_F'], L=['M2_R'], duoL=['M2_180'], Li=['M2_L'],
             duoLi=['M2_180'], B=['M3_L'], duoB=['M3_180'], Bi=['M3_R'], duoBi=['M3_180'],
             D=['M2M4_L_F', 'M1_R', 'M2M4_R_F'], duoD=['M2M4_L_F', 'M1_180', 'M2M4_R_F'],
             Di=['M2M4_L_F', 'M1_L', 'M2M4_R_F'], duoDi=['M2M4_L_F', 'M1_180', 'M2M4_R_F'],
             M=['M2M4_L_B', 'M2M4_R_F'], duoM=['duoM2M4_B', 'duoM2M4_F'], Mi=['M2M4_R_B', 'M2M4_L_F'],
             duoMi=['duoM2M4_B', 'duoM2M4_F'], E=['M1M3_L_F', 'M2M4_R_B', 'M2M4_L_F', 'M1M3_R_F'],
             duoE=['M1M3_L_F', 'duoM2M4_B', 'duoM2M4_F', 'M1M3_R_F'],
             Ei=['M1M3_L_F', 'M2M4_L_B', 'M2M4_R_F', 'M1M3_R_F'],
             duoEi=['M1M3_L_F', 'duoM2M4_B', 'duoM2M4_F', 'M1M3_R_F'], S=['M1M3_L_B', 'M1M3_R_F'],
             duoS=['duoM1M3_B', 'duoM1M3_F'], Si=['M1M3_R_B', 'M1M3_L_F'],
             duoSi=['duoM1M3_B', 'duoM1M3_F'], f=['M3_L', 'M1M3_R_F'], fi=['M3_R', 'M1M3_L_F'],
             r=['M2_R', 'M2M4_L_F'], ri=['M2_L', 'M2M4_R_F'],
             u=['M2M4_L_F', 'M1_R', 'M1M3_L_F', 'M2M4_R_F'],
             ui=['M2M4_L_F', 'M1_L', 'M1M3_R_F', 'M2M4_R_F'],
             l=['M4_R', 'M2M4_R_F'], li=['M4_L', 'M2M4_L_F'],
             b=['M1_R', 'M1M3_L_F'], bi=['M1_L', 'M1M3_R_F'],
             d=['M2M4_L_F', 'M3_L', 'M1M3_R_F', 'M2M4_R_F'],
             di=['M2M4_L_F', 'M3_R', 'M1M3_L_F', 'M2M4_R_F'], X=['M2M4_L_F'], Xi=['M2M4_R_F'],
             Y=['M2M4_R_F', 'M1M3_R_F', 'M2M4_L_F'], Yi=['M1M3_L_F', 'M2M4_L_F', 'M1M3_R_F'],
             Z=['M1M3_R_F'], Zi=['M1M3_L_F'], duoX=['duoM2M4_F'],
             duoY=['M1M3_L_F', 'duoM2M4_F', 'M1M3_R_F'], duoZ=['duoM1M3_F'])


def print_marde(marde):
    arranged_colors = [
        [' ', ' ', ' ', marde['Top'][0], marde['Top'][1], marde['Top'][2], ' ',
         ' ', ' '],
        [' ', ' ', ' ', marde['Top'][3], marde['Top'][4], marde['Top'][5], ' ',
         ' ', ' '],
        [' ', ' ', ' ', marde['Top'][6], marde['Top'][7], marde['Top'][8], ' ',
         ' ', ' '],
        [marde['Left'][0], marde['Left'][1], marde['Left'][2],
         marde['Front'][0],
         marde['Front'][1], marde['Front'][2], marde['Right'][0],
         marde['Right'][1],
         marde['Right'][2], marde['Back'][0], marde['Back'][1],
         marde['Back'][2]],
        [marde['Left'][3], marde['Left'][4], marde['Left'][5],
         marde['Front'][3],
         marde['Front'][4], marde['Front'][5], marde['Right'][3],
         marde['Right'][4],
         marde['Right'][5], marde['Back'][3], marde['Back'][4],
         marde['Back'][5]],
        [marde['Left'][6], marde['Left'][7], marde['Left'][8],
         marde['Front'][6],
         marde['Front'][7], marde['Front'][8], marde['Right'][6],
         marde['Right'][7],
         marde['Right'][8], marde['Back'][6], marde['Back'][7],
         marde['Back'][8]],
        [' ', ' ', ' ', marde['Bottom'][0], marde['Bottom'][1],
         marde['Bottom'][2], ' ', ' ',
         ' '],
        [' ', ' ', ' ', marde['Bottom'][3], marde['Bottom'][4],
         marde['Bottom'][5], ' ', ' ',
         ' '],
        [' ', ' ', ' ', marde['Bottom'][6], marde['Bottom'][7],
         marde['Bottom'][8], ' ', ' ',
         ' '],
    ]
    for row in arranged_colors:
        print(''.join(row))
    print('Move done applying')



        



def apply_move(marde, move):
    if move == 'R':
        temp_top = [marde['Top'][2], marde['Top'][5], marde['Top'][8]]
        temp_front = [marde['Front'][2], marde['Front'][5], marde['Front'][8]]
        temp_bottom = [marde['Bottom'][2], marde['Bottom'][5], marde['Bottom'][8]]
        temp_back = [marde['Back'][0], marde['Back'][3], marde['Back'][6]]

        marde['Back'][0], marde['Back'][3], marde['Back'][6] = temp_top[::-1]
        marde['Top'][2], marde['Top'][5], marde['Top'][8] = temp_front
        marde['Front'][2], marde['Front'][5], marde['Front'][8] = temp_bottom
        marde['Bottom'][2], marde['Bottom'][5], marde['Bottom'][8] = temp_back[
                                                                                                      ::-1]

        # # Rotation de la face droite dans le sens horaire
        marde['Right'][0], marde['Right'][1], marde['Right'][2], \
            marde['Right'][3], marde['Right'][4], marde['Right'][5], \
            marde['Right'][6], marde['Right'][7], marde['Right'][8] = \
            marde['Right'][6], marde['Right'][3], marde['Right'][0], \
                marde['Right'][7], marde['Right'][4], marde['Right'][1], \
                marde['Right'][8], marde['Right'][5], marde['Right'][2]

    elif move == "Ri":
        apply_move(marde, 'R')
        apply_move(marde, 'R')
        apply_move(marde, 'R')
    elif move == 'duoR':
        apply_move(marde, 'R')
        apply_move(marde, 'R')
    elif move == 'duoRi':
        apply_move(marde, 'R')
        apply_move(marde, 'R')
        apply_move(marde, 'R')
        apply_move(marde, 'R')
        apply_move(marde, 'R')
        apply_move(marde, 'R')
    elif move == 'L':
        temp_top = [marde['Top'][0], marde['Top'][3], marde['Top'][6]]
        temp_front = [marde['Front'][0], marde['Front'][3], marde['Front'][6]]
        temp_bottom = [marde['Bottom'][0], marde['Bottom'][3], marde['Bottom'][6]]
        temp_back = [marde['Back'][2], marde['Back'][5], marde['Back'][8]]

        marde['Back'][2], marde['Back'][5], marde['Back'][8] = temp_bottom[::-1]
        marde['Top'][0], marde['Top'][3], marde['Top'][6] = temp_back[::-1]
        marde['Front'][0], marde['Front'][3], marde['Front'][6] = temp_top
        marde['Bottom'][0], marde['Bottom'][3], marde['Bottom'][6] = temp_front

        # # Rotation de la face droite dans le sens horaire
        marde['Left'][0], marde['Left'][1], marde['Left'][2], \
            marde['Left'][3], marde['Left'][4], marde['Left'][5], \
            marde['Left'][6], marde['Left'][7], marde['Left'][8] = \
            marde['Left'][6], marde['Left'][3], marde['Left'][0], \
                marde['Left'][7], marde['Left'][4], marde['Left'][1], \
                marde['Left'][8], marde['Left'][5], marde['Left'][2]
    elif move == "Li":
        apply_move(marde, 'L')
        apply_move(marde, 'L')
        apply_move(marde, 'L')
    elif move == 'duoL':
        apply_move(marde, 'L')
        apply_move(marde, 'L')
    elif move == 'duoLi':
        apply_move(marde, 'L')
        apply_move(marde, 'L')
        apply_move(marde, 'L')
        apply_move(marde, 'L')
        apply_move(marde, 'L')
        apply_move(marde, 'L')
    elif move == 'U':
        temp_right = [marde['Right'][0], marde['Right'][1], marde['Right'][2]]
        temp_front = [marde['Front'][0], marde['Front'][1], marde['Front'][2]]
        temp_left = [marde['Left'][0], marde['Left'][1], marde['Left'][2]]
        temp_back = [marde['Back'][0], marde['Back'][1], marde['Back'][2]]

        marde['Right'][0], marde['Right'][1], marde['Right'][2] = temp_back
        marde['Front'][0], marde['Front'][1], marde['Front'][2] = temp_right
        marde['Left'][0], marde['Left'][1], marde['Left'][2] = temp_front
        marde['Back'][0], marde['Back'][1], marde['Back'][2] = temp_left

        # # Rotation de la face droite dans le sens horaire
        marde['Top'][0], marde['Top'][1], marde['Top'][2], \
            marde['Top'][3], marde['Top'][4], marde['Top'][5], \
            marde['Top'][6], marde['Top'][7], marde['Top'][8] = \
            marde['Top'][6], marde['Top'][3], marde['Top'][0], \
                marde['Top'][7], marde['Top'][4], marde['Top'][1], \
                marde['Top'][8], marde['Top'][5], marde['Top'][2]
    elif move == "Ui":
        apply_move(marde, 'U')
        apply_move(marde, 'U')
        apply_move(marde, 'U')
    elif move == 'duoU':
        apply_move(marde, 'U')
        apply_move(marde, 'U')
    elif move == 'duoUi':
        apply_move(marde, 'U')
        apply_move(marde, 'U')
        apply_move(marde, 'U')
        apply_move(marde, 'U')
        apply_move(marde, 'U')
        apply_move(marde, 'U')
    elif move == 'D':
        temp_right = [marde['Right'][6], marde['Right'][7], marde['Right'][8]]
        temp_front = [marde['Front'][6], marde['Front'][7], marde['Front'][8]]
        temp_left = [marde['Left'][6], marde['Left'][7], marde['Left'][8]]
        temp_back = [marde['Back'][6], marde['Back'][7], marde['Back'][8]]

        marde['Right'][6], marde['Right'][7], marde['Right'][8] = temp_front
        marde['Front'][6], marde['Front'][7], marde['Front'][8] = temp_left
        marde['Left'][6], marde['Left'][7], marde['Left'][8] = temp_back
        marde['Back'][6], marde['Back'][7], marde['Back'][8] = temp_right

        # # Rotation de la face droite dans le sens horaire
        marde['Bottom'][0], marde['Bottom'][1], marde['Bottom'][2], \
            marde['Bottom'][3], marde['Bottom'][4], marde['Bottom'][5], \
            marde['Bottom'][6], marde['Bottom'][7], marde['Bottom'][8] = \
            marde['Bottom'][6], marde['Bottom'][3], marde['Bottom'][0], \
                marde['Bottom'][7], marde['Bottom'][4], marde['Bottom'][1], \
                marde['Bottom'][8], marde['Bottom'][5], marde['Bottom'][2]
    elif move == "Di":
        apply_move(marde, 'D')
        apply_move(marde, 'D')
        apply_move(marde, 'D')
    elif move == 'duoD':
        apply_move(marde, 'D')
        apply_move(marde, 'D')
    elif move == 'duoDi':
        apply_move(marde, 'D')
        apply_move(marde, 'D')
        apply_move(marde, 'D')
        apply_move(marde, 'D')
        apply_move(marde, 'D')
        apply_move(marde, 'D')
    elif move == 'F':
        temp_right = [marde['Right'][0], marde['Right'][3], marde['Right'][6]]
        temp_top = [marde['Top'][6], marde['Top'][7], marde['Top'][8]]
        temp_bottom = [marde['Bottom'][0], marde['Bottom'][1], marde['Bottom'][2]]
        temp_left = [marde['Left'][2], marde['Left'][5], marde['Left'][8]]

        marde['Right'][0], marde['Right'][3], marde['Right'][6] = temp_top
        marde['Top'][6], marde['Top'][7], marde['Top'][8] = temp_left[::-1]
        marde['Left'][2], marde['Left'][5], marde['Left'][8] = temp_bottom
        marde['Bottom'][0], marde['Bottom'][1], marde['Bottom'][2] = temp_right[
                                                                                                      ::-1]

        # # Rotation de la face droite dans le sens horaire
        marde['Front'][0], marde['Front'][1], marde['Front'][2], \
            marde['Front'][3], marde['Front'][4], marde['Front'][5], \
            marde['Front'][6], marde['Front'][7], marde['Front'][8] = \
            marde['Front'][6], marde['Front'][3], marde['Front'][0], \
                marde['Front'][7], marde['Front'][4], marde['Front'][1], \
                marde['Front'][8], marde['Front'][5], marde['Front'][2]
    elif move == "Fi":
        apply_move(marde, 'F')
        apply_move(marde, 'F')
        apply_move(marde, 'F')
    elif move == 'duoF':
        apply_move(marde, 'F')
        apply_move(marde, 'F')
    elif move == 'duoFi':
        apply_move(marde, 'F')
        apply_move(marde, 'F')
        apply_move(marde, 'F')
        apply_move(marde, 'F')
        apply_move(marde, 'F')
        apply_move(marde, 'F')
    elif move == 'B':
        temp_right = [marde['Right'][2], marde['Right'][5], marde['Right'][8]]
        temp_top = [marde['Top'][0], marde['Top'][1], marde['Top'][2]]
        temp_bottom = [marde['Bottom'][6], marde['Bottom'][7], marde['Bottom'][8]]
        temp_left = [marde['Left'][0], marde['Left'][3], marde['Left'][6]]

        marde['Right'][2], marde['Right'][5], marde['Right'][8] = temp_bottom[::-1]
        marde['Top'][0], marde['Top'][1], marde['Top'][2] = temp_right
        marde['Left'][0], marde['Left'][3], marde['Left'][6] = temp_top[::-1]
        marde['Bottom'][6], marde['Bottom'][7], marde['Bottom'][8] = temp_left

        # # Rotation de la face droite dans le sens horaire
        marde['Back'][0], marde['Back'][1], marde['Back'][2], \
            marde['Back'][3], marde['Back'][4], marde['Back'][5], \
            marde['Back'][6], marde['Back'][7], marde['Back'][8] = \
            marde['Back'][6], marde['Back'][3], marde['Back'][0], \
                marde['Back'][7], marde['Back'][4], marde['Back'][1], \
                marde['Back'][8], marde['Back'][5], marde['Back'][2]
    elif move == "B'":
        apply_move(marde, 'B')
        apply_move(marde, 'B')
        apply_move(marde, 'B')
    elif move == 'duoB':
        apply_move(marde, 'B')
        apply_move(marde, 'B')
    elif move == 'duoBi':
        apply_move(marde, 'B')
        apply_move(marde, 'B')
        apply_move(marde, 'B')
        apply_move(marde, 'B')
        apply_move(marde, 'B')
        apply_move(marde, 'B')
    elif move == 'M':
        # Implémentez la logique pour le mouvement M (rotation du cube dans le sens de la colonne centrale droite)
        temp_top = [marde['Top'][1], marde['Top'][4], marde['Top'][7]]
        temp_front = [marde['Front'][1], marde['Front'][4],
                      marde['Front'][7]]
        temp_bottom = [marde['Bottom'][1], marde['Bottom'][4],
                       marde['Bottom'][7]]
        temp_back = [marde['Back'][1], marde['Back'][4], marde['Back'][7]]

        marde['Top'][1], marde['Top'][4], marde['Top'][7] = temp_back[::-1]
        marde['Front'][1], marde['Front'][4], marde['Front'][7] = temp_top
        marde['Bottom'][1], marde['Bottom'][4], marde['Bottom'][
            7] = temp_front
        marde['Back'][1], marde['Back'][4], marde['Back'][7] = temp_bottom[::-1]

    elif move == "Mi":
        # Mouvement M inverse (dans le sens antihoraire)
        apply_move(marde, 'M')
        apply_move(marde, 'M')
        apply_move(marde, 'M')
    elif move == 'duoM':
        apply_move(marde, 'M')
        apply_move(marde, 'M')
    elif move == 'duoMi':
        apply_move(marde, 'M')
        apply_move(marde, 'M')
        apply_move(marde, 'M')
        apply_move(marde, 'M')
        apply_move(marde, 'M')
        apply_move(marde, 'M')
    elif move == 'E':
        # Implémentez la logique pour le mouvement E (rotation du cube dans le sens de la ligne centrale du haut)
        temp_front = marde['Front'][3:6]
        temp_right = marde['Right'][3:6]
        temp_back = marde['Back'][3:6]
        temp_left = marde['Left'][3:6]

        marde['Front'][3:6] = temp_left
        marde['Right'][3:6] = temp_front
        marde['Back'][3:6] = temp_right
        marde['Left'][3:6] = temp_back

    elif move == "Ei":
        # Mouvement E inverse (dans le sens antihoraire)
        apply_move(marde, 'E')
        apply_move(marde, 'E')
        apply_move(marde, 'E')
    elif move == 'duoE':
        apply_move(marde, 'E')
        apply_move(marde, 'E')
    elif move == 'duoEi':
        apply_move(marde, 'E')
        apply_move(marde, 'E')
        apply_move(marde, 'E')
        apply_move(marde, 'E')
        apply_move(marde, 'E')
        apply_move(marde, 'E')
    elif move == 'S':
        # Implémentez la logique pour le mouvement S (rotation du cube dans le sens de la ligne centrale de droite)
        temp_top = [marde['Top'][3], marde['Top'][4], marde['Top'][5]]
        temp_right = [marde['Right'][1], marde['Right'][4],
                      marde['Right'][7]]
        temp_bottom = [marde['Bottom'][3], marde['Bottom'][4],
                       marde['Bottom'][5]]
        temp_left = [marde['Left'][1], marde['Left'][4], marde['Left'][7]]

        marde['Top'][3], marde['Top'][4], marde['Top'][5] = temp_left[::-1]
        marde['Right'][1], marde['Right'][4], marde['Right'][
            7] = temp_top
        marde['Bottom'][3], marde['Bottom'][4], marde['Bottom'][
            5] = temp_right[::-1]
        marde['Left'][1], marde['Left'][4], marde['Left'][7] = temp_bottom

    elif move == "Si":
        # Mouvement S inverse (dans le sens antihoraire)
        apply_move(marde, 'S')
        apply_move(marde, 'S')
        apply_move(marde, 'S')
    elif move == 'duoS':
        apply_move(marde, 'S')
        apply_move(marde, 'S')
    elif move == 'duoSi':
        apply_move(marde, 'S')
        apply_move(marde, 'S')
        apply_move(marde, 'S')
        apply_move(marde, 'S')
        apply_move(marde, 'S')
        apply_move(marde, 'S')

    elif move in ['X', 'Xi', "Y", 'Yi', 'Z', "Zi"]:
        rotate_cube(marde, move)

    else:
        print("Mouvement non reconnu")

    return marde


# Function to rotate the entire cube around the X axis
def rotate_cube(cube, rotation):
    if rotation == 'X':
        temp_top = [cube['Top'][0], cube['Top'][1], cube['Top'][2],
                    cube['Top'][3], cube['Top'][4], cube['Top'][5],
                    cube['Top'][6], cube['Top'][7], cube['Top'][8]]
        temp_front = [cube['Front'][0], cube['Front'][1], cube['Front'][2],
                      cube['Front'][3], cube['Front'][4], cube['Front'][5],
                      cube['Front'][6], cube['Front'][7], cube['Front'][8]]
        temp_bottom = [cube['Bottom'][0], cube['Bottom'][1], cube['Bottom'][2],
                       cube['Bottom'][3], cube['Bottom'][4], cube['Bottom'][5],
                       cube['Bottom'][6], cube['Bottom'][7], cube['Bottom'][8]]
        temp_back = [cube['Back'][0], cube['Back'][1], cube['Back'][2],
                     cube['Back'][3], cube['Back'][4], cube['Back'][5],
                     cube['Back'][6], cube['Back'][7], cube['Back'][8]]

        cube['Top'][0], cube['Top'][1], cube['Top'][2], cube['Top'][3], \
        cube['Top'][4], cube['Top'][5], cube['Top'][6], cube['Top'][7], \
        cube['Top'][8] = temp_front
        cube['Front'][0], cube['Front'][1], cube['Front'][2], \
        cube['Front'][3], cube['Front'][4], cube['Front'][5], \
        cube['Front'][6], cube['Front'][7], cube['Front'][8] = temp_bottom
        cube['Bottom'][0], cube['Bottom'][1], cube['Bottom'][2], \
        cube['Bottom'][3], cube['Bottom'][4], cube['Bottom'][5], \
        cube['Bottom'][6], cube['Bottom'][7], cube['Bottom'][8] = temp_back[::-1]
        cube['Back'][0], cube['Back'][1], cube['Back'][2], cube['Back'][
            3], cube['Back'][4], cube['Back'][5], cube['Back'][6], \
        cube['Back'][7], cube['Back'][8] = temp_top[::-1]

        cube['Right'][0], cube['Right'][1], cube['Right'][2], \
            cube['Right'][3], cube['Right'][4], cube['Right'][5], \
            cube['Right'][6], cube['Right'][7], cube['Right'][8] = \
            cube['Right'][6], cube['Right'][3], cube['Right'][0], \
                cube['Right'][7], cube['Right'][4], cube['Right'][1], \
                cube['Right'][8], cube['Right'][5], cube['Right'][2]

        cube['Left'][0], cube['Left'][1], cube['Left'][2], \
            cube['Left'][3], cube['Left'][4], cube['Left'][5], \
            cube['Left'][6], cube['Left'][7], cube['Left'][8] = \
            cube['Left'][2], cube['Left'][5], cube['Left'][8], \
                cube['Left'][1], cube['Left'][4], cube['Left'][7], \
                cube['Left'][0], cube['Left'][3], cube['Left'][6]

    elif rotation == 'Xi':
        rotate_cube(cube, 'X')
        rotate_cube(cube, 'X')
        rotate_cube(cube, 'X')


    elif rotation == 'Z':
        temp_top = [cube['Top'][0], cube['Top'][1], cube['Top'][2],
                    cube['Top'][3], cube['Top'][4], cube['Top'][5],
                    cube['Top'][6], cube['Top'][7], cube['Top'][8]]
        temp_right = [cube['Right'][0], cube['Right'][1], cube['Right'][2],
                      cube['Right'][3], cube['Right'][4], cube['Right'][5],
                      cube['Right'][6], cube['Right'][7], cube['Right'][8]]
        temp_bottom = [cube['Bottom'][0], cube['Bottom'][1], cube['Bottom'][2],
                       cube['Bottom'][3], cube['Bottom'][4], cube['Bottom'][5],
                       cube['Bottom'][6], cube['Bottom'][7], cube['Bottom'][8]]
        temp_left = [cube['Left'][0], cube['Left'][1], cube['Left'][2],
                     cube['Left'][3], cube['Left'][4], cube['Left'][5],
                     cube['Left'][6], cube['Left'][7], cube['Left'][8]]

        cube['Top'][2], cube['Top'][5], cube['Top'][8], cube['Top'][1], \
        cube['Top'][4], cube['Top'][7], cube['Top'][0], cube['Top'][3], \
        cube['Top'][6] = temp_left
        cube['Right'][2], cube['Right'][5], cube['Right'][8], \
            cube['Right'][1], cube['Right'][4], cube['Right'][7], \
            cube['Right'][0], cube['Right'][3], cube['Right'][6] = temp_top
        cube['Bottom'][2], cube['Bottom'][5], cube['Bottom'][8], \
            cube['Bottom'][1], cube['Bottom'][4], cube['Bottom'][7], \
            cube['Bottom'][0], cube['Bottom'][3], cube['Bottom'][6] = temp_right
        cube['Left'][2], cube['Left'][5], cube['Left'][8], \
            cube['Left'][1], cube['Left'][4], cube['Left'][7], \
            cube['Left'][0], cube['Left'][3], cube['Left'][6] = temp_bottom

        cube['Front'][0], cube['Front'][1], cube['Front'][2], \
            cube['Front'][3], cube['Front'][4], cube['Front'][5], \
            cube['Front'][6], cube['Front'][7], cube['Front'][8] = \
            cube['Front'][6], cube['Front'][3], cube['Front'][0], \
                cube['Front'][7], cube['Front'][4], cube['Front'][1], \
                cube['Front'][8], cube['Front'][5], cube['Front'][2]

        cube['Back'][0], cube['Back'][1], cube['Back'][2], \
            cube['Back'][3], cube['Back'][4], cube['Back'][5], \
            cube['Back'][6], cube['Back'][7], cube['Back'][8] = \
            cube['Back'][2], cube['Back'][5], cube['Back'][8], \
                cube['Back'][1], cube['Back'][4], cube['Back'][7], \
                cube['Back'][0], cube['Back'][3], cube['Back'][6]
    elif rotation == 'Zi':
        rotate_cube(cube, 'Z')
        rotate_cube(cube, 'Z')
        rotate_cube(cube, 'Z')


    elif rotation == 'Y':
        temp_front = [cube['Front'][0], cube['Front'][1], cube['Front'][2],
                      cube['Front'][3], cube['Front'][4], cube['Front'][5],
                      cube['Front'][6], cube['Front'][7], cube['Front'][8]]
        temp_right = [cube['Right'][0], cube['Right'][1], cube['Right'][2],
                      cube['Right'][3], cube['Right'][4], cube['Right'][5],
                      cube['Right'][6], cube['Right'][7], cube['Right'][8]]
        temp_back = [cube['Back'][0], cube['Back'][1], cube['Back'][2],
                     cube['Back'][3], cube['Back'][4], cube['Back'][5],
                     cube['Back'][6], cube['Back'][7], cube['Back'][8]]
        temp_left = [cube['Left'][0], cube['Left'][1], cube['Left'][2],
                     cube['Left'][3], cube['Left'][4], cube['Left'][5],
                     cube['Left'][6], cube['Left'][7], cube['Left'][8]]

        cube['Front'][0], cube['Front'][1], cube['Front'][2], \
        cube['Front'][3], cube['Front'][4], cube['Front'][5], \
        cube['Front'][6], cube['Front'][7], cube['Front'][8] = temp_right
        cube['Right'][0], cube['Right'][1], cube['Right'][2], \
        cube['Right'][3], cube['Right'][4], cube['Right'][5], \
        cube['Right'][6], cube['Right'][7], cube['Right'][8] = temp_back
        cube['Back'][0], cube['Back'][1], cube['Back'][2], cube['Back'][
            3], cube['Back'][4], cube['Back'][5], cube['Back'][6], \
        cube['Back'][7], cube['Back'][8] = temp_left
        cube['Left'][0], cube['Left'][1], cube['Left'][2], cube['Left'][
            3], cube['Left'][4], cube['Left'][5], cube['Left'][6], \
        cube['Left'][7], cube['Left'][8] = temp_front

        cube['Top'][0], cube['Top'][1], cube['Top'][2], \
            cube['Top'][3], cube['Top'][4], cube['Top'][5], \
            cube['Top'][6], cube['Top'][7], cube['Top'][8] = \
            cube['Top'][6], cube['Top'][3], cube['Top'][0], \
                cube['Top'][7], cube['Top'][4], cube['Top'][1], \
                cube['Top'][8], cube['Top'][5], cube['Top'][2]

        cube['Bottom'][0], cube['Bottom'][1], cube['Bottom'][2], \
            cube['Bottom'][3], cube['Bottom'][4], cube['Bottom'][5], \
            cube['Bottom'][6], cube['Bottom'][7], cube['Bottom'][8] = \
            cube['Bottom'][2], cube['Bottom'][5], cube['Bottom'][8], \
                cube['Bottom'][1], cube['Bottom'][4], cube['Bottom'][7], \
                cube['Bottom'][0], cube['Bottom'][3], cube['Bottom'][6]
    elif rotation == 'Yi':
        rotate_cube(cube, 'Y')
        rotate_cube(cube, 'Y')
        rotate_cube(cube, 'Y')


if __name__ == '__main__':
    basic_moves = moves.keys()

    for move in basic_moves:
        initial_face_colors = {
    'Back': ['r', 'g', 'g', 'b', 'g', 'g', 'o', 'o', 'w'],
    'Left': ['w', 'g', 'w', 'r', 'o', 'b', 'r', 'w', 'o'],
    'Top': ['o', 'y', 'y', 'w', 'y', 'y', 'b', 'b', 'y'],
    'Right': ['g', 'r', 'b', 'y', 'r', 'r', 'b', 'o', 'w'],
    'Front': ['r', 'w', 'r', 'o', 'b', 'b', 'g', 'r', 'y'],
    'Bottom': ['y', 'w', 'o', 'o', 'w', 'y', 'g', 'g', 'b']
}
        input(move)
        merde = apply_move(initial_face_colors, move)
        print_marde(merde)
