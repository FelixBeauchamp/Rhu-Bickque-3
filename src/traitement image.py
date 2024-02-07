# The file to analyze the colors on the cube
import numpy as np
import cv2
cap = cv2.VideoCapture(0)

YellowL_limit = np.array([30, 100, 70])  # setting the yellow lower limit
YellowU_limit = np.array([40, 255, 255])  # setting the yellow upper limit

BlueL_limit = np.array([100, 100, 70])  # setting the yellow lower limit
BlueU_limit = np.array([140, 255, 255])

RedL_limit = np.array([165, 150, 160])  # setting the yellow lower limit
RedU_limit = np.array([180, 255, 255])

OrangeL_limit = np.array([10, 200, 70])  # setting the yellow lower limit
OrangeU_limit = np.array([25, 255, 255])

GreenL_limit = np.array([30, 30, 30])  # setting the yellow lower limit
GreenU_limit = np.array([70, 255, 255])

WhiteL_limit = np.array([30, 100, 70])  # setting the yellow lower limit
WhiteU_limit = np.array([50, 255, 255])


# frames = np.array([[1,1,1],[1,1,1],[1,1,1]])
def colorofsquare(leframe):
    Y_mask = cv2.inRange(leframe, YellowL_limit, YellowU_limit)
    yellow_pixel_count = cv2.countNonZero(Y_mask)
    if yellow_pixel_count > 500:
        return 1
    else:
        B_mask = cv2.inRange(leframe, BlueL_limit, BlueU_limit)
        blue_pixel_count = cv2.countNonZero(B_mask)
        if blue_pixel_count > 1000:
            return 2
        R_mask = cv2.inRange(leframe, RedL_limit, RedU_limit)
        red_pixel_count = cv2.countNonZero(B_mask)
        if red_pixel_count > 1000:
            return 3
        O_mask = cv2.inRange(leframe, OrangeL_limit, OrangeU_limit)
        orange_pixel_count = cv2.countNonZero(O_mask)
        if orange_pixel_count > 1000:
            return 4
        G_mask = cv2.inRange(leframe, GreenL_limit, GreenU_limit)
        green_pixel_count = cv2.countNonZero(G_mask)
        if green_pixel_count > 1000:
            return 5
        W_mask = cv2.inRange(leframe, WhiteL_limit, WhiteU_limit)
        white_pixel_count = cv2.countNonZero(W_mask)
        if white_pixel_count > 1000:
            return 6


while 1:
    ret, frame = cap.read()
    width = np.size(frame, 1)
    height = np.size(frame, 0)

    coin_sup_gauche = [0, 0]
    coin_inf_droit = [width, height]

    cote_cube = 100

    # Barre horizontales
    haut_1_x = 100
    bas_1_x = 200

    haut_2_x = haut_1_x + cote_cube
    bas_2_x = bas_1_x + cote_cube

    haut_3_x = haut_2_x + cote_cube
    bas_3_x = bas_2_x + cote_cube

    # Barres verticales
    gauche_x_1 = 200
    droite_x_1 = 300

    gauche_x_2 = gauche_x_1 + cote_cube
    droite_x_2 = droite_x_1 + cote_cube

    gauche_x_3 = gauche_x_2 + cote_cube
    droite_x_3 = droite_x_2 + cote_cube

    filtered = cv2.GaussianBlur(frame, (5, 5), cv2.BORDER_DEFAULT)

    into_hsv = cv2.cvtColor(filtered, cv2.COLOR_BGR2HSV)
    into_hsv_filtered = cv2.cvtColor(filtered, cv2.COLOR_BGR2HSV)

    frame_1_1 = into_hsv[haut_1_x:bas_1_x, gauche_x_1:droite_x_1].copy()
    frame_2_1 = into_hsv[haut_2_x:bas_2_x, gauche_x_1:droite_x_1].copy()
    frame_3_1 = into_hsv[haut_3_x:bas_3_x, gauche_x_1:droite_x_1].copy()

    frame_1_2 = into_hsv[haut_1_x:bas_1_x, gauche_x_2:droite_x_2].copy()
    frame_2_2 = into_hsv[haut_2_x:bas_2_x, gauche_x_2:droite_x_2].copy()
    frame_3_2 = into_hsv[haut_3_x:bas_3_x, gauche_x_2:droite_x_2].copy()

    frame_1_3 = into_hsv[haut_1_x:bas_1_x, gauche_x_3:droite_x_3].copy()
    frame_2_3 = into_hsv[haut_2_x:bas_2_x, gauche_x_3:droite_x_3].copy()
    frame_3_3 = into_hsv[haut_3_x:bas_3_x, gauche_x_3:droite_x_3].copy()

    # ret will return a true value if the frame exists otherwise False
    into_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # creating the mask using inRange() function
    # this will produce an image where the color of the objects
    # falling in the range will turn white and rest will be black
    '''
    yellow = cv2.bitwise_and(frame, frame, mask=Y_mask)
    blue = cv2.bitwise_and(frame, frame, mask=B_mask)
    red = cv2.bitwise_and(frame, frame, mask=R_mask)
    orange = cv2.bitwise_or(frame, frame, mask=O_mask)
    green = cv2.bitwise_and(frame, frame, mask=G_mask)
    white = cv2.bitwise_and(frame, frame, mask=W_mask)
    '''
    # this will give the color to mask.
    cv2.imshow('frame1_1', frame_1_1)
    '''
    cv2.imshow('Original', frame)  # to display the original frame
    cv2.imshow('Filtered', filtered)  # to display the original frame
    cv2.imshow('hsv', into_hsv)  # to display the original frame
    cv2.imshow('hsv_filtered', into_hsv_filtered)  # to display the original frame
    cv2.imshow('frame1_1', frame_1_1)

    cv2.imshow('1_1', frame_1_1)
    cv2.imshow('2_1', frame_2_1)
    cv2.imshow('3_1', frame_3_1)

    cv2.imshow('1_2', frame_1_2)
    cv2.imshow('2_2', frame_2_2)
    cv2.imshow('3_2', frame_3_2)

    cv2.imshow('1_3', frame_1_3)
    cv2.imshow('2_3', frame_2_3)
    cv2.imshow('3_3', frame_3_3)

    cv2.imshow('Orange Detector', O_mask)  # to display the yellow object output
    cv2.imshow('White Detector', W_mask)
    cv2.imshow('Yellow Detector', Y_mask)
    cv2.imshow('Blue Detector', B_mask)
    cv2.imshow('Red Detector', R_mask)
    cv2.imshow('Green Detector', G_mask)
    '''

    square1_1 = colorofsquare(frame_1_1)
    square2_1 = colorofsquare(frame_2_1)
    square3_1 = colorofsquare(frame_3_1)

    square1_2 = colorofsquare(frame_1_2)
    square2_2 = colorofsquare(frame_2_2)
    square3_2 = colorofsquare(frame_3_2)

    square1_3 = colorofsquare(frame_1_3)
    square2_3 = colorofsquare(frame_2_3)
    square3_3 = colorofsquare(frame_3_3)

    print(square1_1, square1_2, square1_3)
    print("\n")
    print(square2_1, square2_2, square2_3)
    print("\n")
    print(square3_1, square3_2, square3_3)

    #
    if cv2.waitKey(3000) == 27:
        break
    # this function will be triggered when the ESC key is pressed
    # and the while loop will terminate and so will the program

cap.release()

cv2.destroyAllWindows()



