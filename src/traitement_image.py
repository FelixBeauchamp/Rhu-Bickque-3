# The file to analyze the colors on the cube
import numpy as np
import cv2

YellowL_limit = np.array([15, 10, 0])  # setting the yellow lower limit
YellowU_limit = np.array([35, 255, 200])

BlueL_limit = np.array([100, 0, 0])  # setting the blue lower limit
BlueU_limit = np.array([110, 255, 220])

RedL_limit_high = np.array([140, 0, 0])  # setting the red lower limit
RedU_limit_high = np.array([178, 255, 220])

OrangeL_limit = np.array([2, 0, 0])  # setting the orange lower limit
OrangeU_limit = np.array([15, 255, 220])

GreenL_limit = np.array([45, 0, 0])  # setting the green lower limit
GreenU_limit = np.array([95, 255, 220])

WhiteL_limit = np.array([0, 0, 90])  # setting the white lower limit
WhiteU_limit = np.array([180, 75, 255])


# frames = np.array([[1,1,1],[1,1,1],[1,1,1]])
def colorofsquare(leframe):

    Y_mask = cv2.inRange(leframe, YellowL_limit, YellowU_limit)
    yellow_pixel_count = cv2.countNonZero(Y_mask)
    cv2.imshow('Yellow pixel count', Y_mask)

    B_mask = cv2.inRange(leframe, BlueL_limit, BlueU_limit)
    blue_pixel_count = cv2.countNonZero(B_mask)

    R_mask = cv2.inRange(leframe, RedL_limit_high, RedU_limit_high)
#   R_mask_2 = cv2.inRange(leframe, RedL_limit_low, RedU_limit_low)
    red_pixel_count = cv2.countNonZero(R_mask) #+ cv2.countNonZero(R_mask_2)

    O_mask = cv2.inRange(leframe, OrangeL_limit, OrangeU_limit)
    orange_pixel_count = cv2.countNonZero(O_mask)

    G_mask = cv2.inRange(leframe, GreenL_limit, GreenU_limit)
    green_pixel_count = cv2.countNonZero(G_mask)

    W_mask = cv2.inRange(leframe, WhiteL_limit, WhiteU_limit)
    white_pixel_count = cv2.countNonZero(W_mask)

    print("Blue:", blue_pixel_count, "Red:",red_pixel_count, "Orange:",orange_pixel_count, "Green:",green_pixel_count, "Yellow:",yellow_pixel_count,
          "White:",white_pixel_count)

    couleur = max(blue_pixel_count, red_pixel_count, orange_pixel_count, green_pixel_count, yellow_pixel_count,
                  white_pixel_count)
    if couleur == blue_pixel_count:
        return "B"
    elif couleur == red_pixel_count:
        return "R"
    elif couleur == orange_pixel_count:
        return "O"
    elif couleur == green_pixel_count:
        return "G"
    elif couleur == yellow_pixel_count:
        return "Y"
    elif couleur == white_pixel_count:
        return "W"




def faceofdacube(image):
    if image == '':
        cap = cv2.VideoCapture(0)
        print('tbnk')
        ret, frame_test = cap.read()
        # Number of frames to capture
        num_frames =1
        frames = []

        #Capture frames
        #for i in range(num_frames):
        #    ret, frame = cap.read()
        #    if not ret:
        #       break
        #    frames.append(frame)

        #Average the frames
        #avg_frame = sum(frames) // len(frames)

        ret, avg_frame = cap.read()
    else:
        avg_frame = cv2.imread(image)

    #coin_sup_gauche = [0, 0]
    #coin_inf_droit = [width, height]

    cote_cube = 85
    frame_loose = 6
    length_pince = 55
    edge_width = 15
    # Barre horizontales

    haut_1_x = 100
    bas_1_x = haut_1_x+cote_cube

    haut_2_x = haut_1_x + cote_cube + edge_width
    bas_2_x = haut_2_x + cote_cube

    haut_3_x = haut_2_x + cote_cube + edge_width
    bas_3_x = haut_3_x + cote_cube

    # Barres verticales
    gauche_x_1 = 210
    droite_x_1 = gauche_x_1+cote_cube

    gauche_x_2 = gauche_x_1 + cote_cube +edge_width
    droite_x_2 = gauche_x_2 + cote_cube

    gauche_x_3 = gauche_x_2 + cote_cube +edge_width
    droite_x_3 = gauche_x_3 + cote_cube

    cv2.imshow('Vision initiale', avg_frame)
    filtered_avg = cv2.GaussianBlur(avg_frame, (5, 5), cv2.BORDER_DEFAULT)
    cv2.imshow('Face du cube avg nor', filtered_avg)

    into_hsv_filtered_avg = cv2.cvtColor(filtered_avg, cv2.COLOR_BGR2HSV)
    frame_cube_avg = into_hsv_filtered_avg[haut_1_x:bas_3_x, gauche_x_1:droite_x_3].copy()
    cv2.imshow('Face du cube avg', frame_cube_avg)
    cv2.imwrite('frame_cube.png', avg_frame)

    frame_1_1 = into_hsv_filtered_avg[haut_1_x+frame_loose:bas_1_x-frame_loose, gauche_x_1+frame_loose:droite_x_1-frame_loose].copy()
    cv2.imshow('Face 1_1', frame_1_1)
    #cv2.imwrite('frame_11.png', frame_1_1)
    frame_2_1 = into_hsv_filtered_avg[haut_2_x+frame_loose:bas_2_x-frame_loose, gauche_x_1+length_pince:droite_x_1-frame_loose].copy()
    cv2.imshow('Face 2_1', frame_2_1)
    #cv2.imwrite('frame_21.png',frame_2_1)
    frame_3_1 = into_hsv_filtered_avg[haut_3_x+frame_loose:bas_3_x-frame_loose, gauche_x_1+frame_loose:droite_x_1-frame_loose].copy()
    cv2.imshow('Face 3_1', frame_3_1)
    #cv2.imwrite('frame_31.png',frame_3_1)

    frame_1_2 = into_hsv_filtered_avg[haut_1_x+length_pince:bas_1_x-frame_loose, gauche_x_2+frame_loose:droite_x_2-frame_loose].copy()
    cv2.imshow('Face 1_2', frame_1_2)
    #cv2.imwrite('frame_12.png',frame_1_2)
    frame_2_2 = into_hsv_filtered_avg[haut_2_x+frame_loose:bas_2_x-frame_loose, gauche_x_2+frame_loose:droite_x_2-frame_loose].copy()
    cv2.imshow('Face 2_2', frame_2_2)
    #cv2.imwrite('frame_22.png',frame_2_2)
    frame_3_2 = into_hsv_filtered_avg[haut_3_x+frame_loose:bas_3_x-length_pince, gauche_x_2+frame_loose:droite_x_2-frame_loose].copy()
    cv2.imshow('Face 3_2', frame_3_2)
    #cv2.imwrite('frame_32.png',frame_3_2)

    frame_1_3 = into_hsv_filtered_avg[haut_1_x+frame_loose:bas_1_x-frame_loose, gauche_x_3+frame_loose:droite_x_3-frame_loose].copy()
    cv2.imshow('Face 1_3', frame_1_3)
    #cv2.imwrite('frame_13.png',frame_1_3)
    frame_2_3 = into_hsv_filtered_avg[haut_2_x+frame_loose:bas_2_x-frame_loose, gauche_x_3+frame_loose:droite_x_3-length_pince].copy()
    cv2.imshow('Face 2_3', frame_2_3)
    #cv2.imwrite('frame_23.png',frame_2_3)
    frame_3_3 = into_hsv_filtered_avg[haut_3_x+frame_loose:bas_3_x-frame_loose, gauche_x_3+frame_loose:droite_x_3-frame_loose].copy()
    cv2.imshow('Face 3_3', frame_3_3)
    #cv2.imwrite('frame_33.png',frame_3_3)

    square1_1 = colorofsquare(frame_1_1)
    square2_1 = colorofsquare(frame_2_1)
    square3_1 = colorofsquare(frame_3_1)

    square1_2 = colorofsquare(frame_1_2)
    square2_2 = colorofsquare(frame_2_2)
    square3_2 = colorofsquare(frame_3_2)

    square1_3 = colorofsquare(frame_1_3)
    square2_3 = colorofsquare(frame_2_3)
    square3_3 = colorofsquare(frame_3_3)

    daresults = [square1_1, square1_2, square1_3, square2_1, square2_2, square2_3, square3_1, square3_2, square3_3]

    if image == '':
        cap.release()
    # cv2.destroyAllWindows()
    return daresults


if __name__ == '__main__':
    while 1:
        print(faceofdacube('frame_cube.png'))
        if cv2.waitKey(3000) == 27:
            break
    # this function will be triggered when the ESC key is pressed
    # and the while loop will terminate and so will the program


