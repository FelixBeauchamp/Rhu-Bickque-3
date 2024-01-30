# This is a sample Python script.
import sys
sys.path.append('path/to/opencv/module')


#import cv2

# import cv2

cap = cv2.VideoCapture(0)


YellowL_limit = np.array([30, 100, 70])  # setting the yellow lower limit
YellowU_limit = np.array([50, 255, 255])  # setting the yellow upper limit

BlueL_limit = np.array([100, 100, 70])  # setting the yellow lower limit
BlueU_limit = np.array([140, 255, 255])

RedL_limit = np.array([165, 150, 160])  # setting the yellow lower limit
RedU_limit = np.array([180, 255, 255])

OrangeL_limit = np.array([10, 200, 70])  # setting the yellow lower limit
OrangeU_limit = np.array([20, 255, 255])

GreenL_limit = np.array([30, 100, 70])  # setting the yellow lower limit
GreenU_limit = np.array([50, 255, 255])

WhiteL_limit = np.array([30, 100, 70])  # setting the yellow lower limit
WhiteU_limit = np.array([50, 255, 255])

while 1:
    ret, frame = cap.read()
    width = np.size(frame,1)
    height = np.size(frame,0)

    frame_1_1 = frame.copy()
    frame_2_1 = frame.copy()
    frame_3_1 = frame.copy()

    frame_1_2 = frame.copy()
    frame_2_2 = frame.copy()
    frame_3_2 = frame.copy()

    frame_1_3 = frame.copy()
    frame_2_3 = frame.copy()
    frame_3_3 = frame.copy()


    coin_sup_gauche = [0,0]
    coin_inf_droit = [width, height]

    cote_cube = 100

    #Barre horizontales
    haut_1_x = 100
    bas_1_x = 200

    haut_2_x = haut_1_x 
    bas_2_x = 300

    haut_3_x = 300
    bas_3_x = 400

    #Barres verticales
    gauche_x_1 = 200
    droite_x_1 = 300

    gauche_x_2 = 300
    droite_x_2 = 400

    gauche_x_3 = 400
    droite_x_3 = 500



    frame_1_1 = frame[haut_1_x:bas_1_x, gauche_x_1:droite_x_1]


    # ret will return a true value if the frame exists otherwise False
    into_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    into_hsv_1_1 = cv2.cvtColor(frame_1_1, cv2.COLOR_BGR2HSV)

    Y_mask = cv2.inRange(into_hsv, YellowL_limit, YellowU_limit)
    B_mask = cv2.inRange(into_hsv, BlueL_limit, BlueU_limit)
    R_mask = cv2.inRange(into_hsv, RedL_limit, RedU_limit)
    O_mask = cv2.inRange(into_hsv_1_1, OrangeL_limit, OrangeU_limit)
    G_mask = cv2.inRange(into_hsv, GreenL_limit, GreenU_limit)
    W_mask = cv2.inRange(into_hsv, WhiteL_limit, WhiteU_limit)
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
    cv2.imshow('Original', frame)  # to display the original frame

    cv2.imshow('1_1', frame_1_1)
    '''
    cv2.imshow('1_2', frame_1_2)
    cv2.imshow('1_3', frame_1_3)

    cv2.imshow('2_1', frame_2_1)
    cv2.imshow('2_2', frame_2_2)
    cv2.imshow('2_3', frame_2_3)

    cv2.imshow('3_1', frame_3_1)
    cv2.imshow('3_2', frame_3_2)
    cv2.imshow('3_3', frame_3_3)
    '''
    cv2.imshow('Orange Detector', O_mask)  # to display the yellow object output

    white_pixel_count = cv2.countNonZero(O_mask)

    if white_pixel_count > 500:
        print('orange')
        print(white_pixel_count)
        print(np.size(frame_1_1,0))
    #
    if cv2.waitKey(1) == 27:
        break
    # this function will be triggered when the ESC key is pressed
    # and the while loop will terminate and so will the program
cap.release()

cv2.destroyAllWindows()



