# The file to analyze the colors on the cube
import numpy as np
import cv2

# Setting the lower and upper limits for each color of the rubik's cube
YellowL_limit = np.array([18, 10, 0])
YellowU_limit = np.array([35, 255, 235])

BlueL_limit = np.array([100, 0, 0])
BlueU_limit = np.array([110, 255, 230])

RedL_limit_high = np.array([160, 0, 0])
RedU_limit_high = np.array([180, 255, 230])

RedL_limit_low = np.array([0, 0, 0])
RedU_limit_low = np.array([6, 255, 230])

OrangeL_limit = np.array([8, 0, 0])
OrangeU_limit = np.array([17, 255, 230])

GreenL_limit = np.array([45, 0, 0])
GreenU_limit = np.array([95, 255, 230])

WhiteL_limit = np.array([0, 0, 90])
WhiteU_limit = np.array([180, 75, 255])

#This function finds the color of a square
def colorofsquare(leframe):

    #Checks the amount of pixels which are a certain color, for each color
    Y_mask = cv2.inRange(leframe, YellowL_limit, YellowU_limit)
    yellow_pixel_count = cv2.countNonZero(Y_mask)

    B_mask = cv2.inRange(leframe, BlueL_limit, BlueU_limit)
    blue_pixel_count = cv2.countNonZero(B_mask)

    # Red can be found on both ends of the HSV color range, hence why two color ranges are checked here
    R_mask = cv2.inRange(leframe, RedL_limit_high, RedU_limit_high)
    R_mask_2 = cv2.inRange(leframe, RedL_limit_low, RedU_limit_low)
    red_pixel_count = cv2.countNonZero(R_mask) + cv2.countNonZero(R_mask_2)

    O_mask = cv2.inRange(leframe, OrangeL_limit, OrangeU_limit)
    orange_pixel_count = cv2.countNonZero(O_mask)

    G_mask = cv2.inRange(leframe, GreenL_limit, GreenU_limit)
    green_pixel_count = cv2.countNonZero(G_mask)

    W_mask = cv2.inRange(leframe, WhiteL_limit, WhiteU_limit)
    white_pixel_count = cv2.countNonZero(W_mask)

    # Can be used to print the amount of pixels corresponding to each colors, used for debugging
    #print("Blue:", blue_pixel_count, "Red:",red_pixel_count, "Orange:",orange_pixel_count, "Green:",green_pixel_count, "Yellow:",yellow_pixel_count,
    #     "White:",white_pixel_count)


    couleur = max(blue_pixel_count, red_pixel_count, orange_pixel_count, green_pixel_count, yellow_pixel_count,
                  white_pixel_count)
    # Returns the color with the highest color count
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

# This function analyses a picture and isolates each square of the face of the cube
def faceofdacube(image):
    # Check if a picture has to be taken with the camera or if a saved image will be used, for unit testing purposes
    if image == '':
        cap = cv2.VideoCapture(0)
        ret, frame_test = cap.read()

        ret, avg_frame = cap.read()
    else:
        avg_frame = cv2.imread(image)

    # Constants used to crop each square
    cote_cube = 85
    frame_loose = 6
    length_pince = 55
    edge_width = 15

    # Variables used to crop each square, vertical
    haut_1_x = 100
    bas_1_x = haut_1_x+cote_cube

    haut_2_x = haut_1_x + cote_cube + edge_width
    bas_2_x = haut_2_x + cote_cube

    haut_3_x = haut_2_x + cote_cube + edge_width
    bas_3_x = haut_3_x + cote_cube

    # Variables used to crop each square, horizontal
    gauche_x_1 = 210
    droite_x_1 = gauche_x_1+cote_cube

    gauche_x_2 = gauche_x_1 + cote_cube +edge_width
    droite_x_2 = gauche_x_2 + cote_cube

    gauche_x_3 = gauche_x_2 + cote_cube +edge_width
    droite_x_3 = gauche_x_3 + cote_cube

    #Gaussianblur used to get rid of extremes and uniform pixels
    filtered_avg = cv2.GaussianBlur(avg_frame, (5, 5), cv2.BORDER_DEFAULT)

    #Changing color format from RGB to HSV
    into_hsv_filtered_avg = cv2.cvtColor(filtered_avg, cv2.COLOR_BGR2HSV)
    # Framing the face
    frame_cube_avg = into_hsv_filtered_avg[haut_1_x:bas_3_x, gauche_x_1:droite_x_3].copy()

    # Cropping out each square
    frame_1_1 = into_hsv_filtered_avg[haut_1_x+frame_loose:bas_1_x-frame_loose, gauche_x_1+frame_loose:droite_x_1-frame_loose].copy()
    frame_2_1 = into_hsv_filtered_avg[haut_2_x+frame_loose:bas_2_x-frame_loose, gauche_x_1+length_pince:droite_x_1-frame_loose].copy()
    frame_3_1 = into_hsv_filtered_avg[haut_3_x+frame_loose:bas_3_x-frame_loose, gauche_x_1+frame_loose:droite_x_1-frame_loose].copy()


    frame_1_2 = into_hsv_filtered_avg[haut_1_x+length_pince:bas_1_x-frame_loose, gauche_x_2+frame_loose:droite_x_2-frame_loose].copy()
    frame_2_2 = into_hsv_filtered_avg[haut_2_x+frame_loose:bas_2_x-frame_loose, gauche_x_2+frame_loose:droite_x_2-frame_loose].copy()
    frame_3_2 = into_hsv_filtered_avg[haut_3_x+frame_loose:bas_3_x-length_pince, gauche_x_2+frame_loose:droite_x_2-frame_loose].copy()


    frame_1_3 = into_hsv_filtered_avg[haut_1_x+frame_loose:bas_1_x-frame_loose, gauche_x_3+frame_loose:droite_x_3-frame_loose].copy()
    frame_2_3 = into_hsv_filtered_avg[haut_2_x+frame_loose:bas_2_x-frame_loose, gauche_x_3+frame_loose:droite_x_3-length_pince].copy()
    frame_3_3 = into_hsv_filtered_avg[haut_3_x+frame_loose:bas_3_x-frame_loose, gauche_x_3+frame_loose:droite_x_3-frame_loose].copy()

    # Detecting the color of each square
    square1_1 = colorofsquare(frame_1_1)
    square2_1 = colorofsquare(frame_2_1)
    square3_1 = colorofsquare(frame_3_1)

    square1_2 = colorofsquare(frame_1_2)
    square2_2 = colorofsquare(frame_2_2)
    square3_2 = colorofsquare(frame_3_2)

    square1_3 = colorofsquare(frame_1_3)
    square2_3 = colorofsquare(frame_2_3)
    square3_3 = colorofsquare(frame_3_3)

    # If the camera was used, close it
    if image == '':
        cap.release()

    # Returning the results
    daresults = [square1_1, square1_2, square1_3, square2_1, square2_2, square2_3, square3_1, square3_2, square3_3]

    return daresults


if __name__ == '__main__':
    while 1:
        print(faceofdacube('frame_cube.png'))
        #Press esc to close the program
        if cv2.waitKey(3000) == 27:
            break
    # this function will be triggered when the ESC key is pressed
    # and the while loop will terminate and so will the program


