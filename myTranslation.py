import os
import numpy as np
import cv2
import imutils
# import math

# Define my image calibration algorithm

# Initiate threshold values, for later image processing (contour recognition based on color)
im_lower = np.array([20, 75, 75], dtype="uint8")
im_upper = np.array([35, 255, 255], dtype="uint8")
kernel = np.ones((3, 3), np.uint8)
# Coordinates corresponding to landmarks
ref_x = []  # Reference landmark coordinates, x axis
ref_y = []  # Reference landmark coordinates, y axis
cur_x = []  # Current landmark coordinates, x axis
cur_y = []  # Current landmark coordinates, y axis
for k in range(0, 5):  # Initiate above lists
    ref_x.append(0)
    ref_y.append(0)
    cur_x.append(0)
    cur_y.append(0)

# Open parking lot information files - landmark
def info_open_slot():
    file_flag = 0
    coord = []
    f_slot = open("D:\\IC DESIGN LAB\\[LAB] PRJ.Parking Lot\\IMAGE_CALIBRATION_V2\\"
                  "data_process\\park_lot_info\\slot.txt", 'r')

    if (os.stat("D:\\IC DESIGN LAB\\[LAB] PRJ.Parking Lot\\IMAGE_CALIBRATION_V2\\"
                  "data_process\\park_lot_info\\slot.txt").st_size == 0):
        # print('Landmark file has no value, please run Define Parking Slot')
        file_flag = 1
    else:
        lis = [line.split() for line in f_slot]
        n = len(lis[0])
        fileLength = len(lis)

        for j in range(n):
            tempArray = []
            for i in range(fileLength):
                tempArray.append(int(lis[i][j]))
            coord.append(tempArray)

    return file_flag, coord

def info_open():
    global ref_x, ref_y
    file_flag = 0
    ### Bad coding practice, avoid using static addresses! Try using environment variables instead to prevent machine
    ### specific errors!
    path_parent = os.getcwd()
    f_landmark = open("D:\\IC DESIGN LAB\\[LAB] PRJ.Parking Lot\\IMAGE_CALIBRATION_V2"
                      "\\data_process\\park_lot_info\\landmark.txt", 'r+')
    if os.stat("D:\\IC DESIGN LAB\\[LAB] PRJ.Parking Lot\\IMAGE_CALIBRATION_V2"
                      "\\data_process\\park_lot_info\\landmark.txt").st_size == 0:
        # print('Landmark file has no value, please run Define Parking Slot')
        file_flag = 1
    else:
        # Appending values from file to a list, then add to above ref list
        lis = [line.split() for line in f_landmark]
        coord = []
        n = len(lis[0])
        file_length = len(lis)

        for j in range(n):
            temp_array = []
            for i in range(file_length):
                temp_array.append(int(lis[i][j]))
            coord.append(temp_array)
        ### Debug code:
        # print(coord)
        ref_x[1] = coord[1][0]
        ref_y[1] = coord[2][0]
        ref_x[2] = coord[1][1]
        ref_y[2] = coord[2][1]
        ref_x[3] = coord[1][2]
        ref_y[3] = coord[2][2]
        ref_x[4] = coord[1][3]
        ref_y[4] = coord[2][3]
    return file_flag, ref_x, ref_y

# Recognize landmarks available on the input image!
def landmark_recog(filename):
    # Value indicates how many contour available at desired landmark positions. Best value = 1
    # Initiate values
    cur_1 = 0   # Landmark 1
    cur_2 = 0   # Landmark 2
    cur_3 = 0   # Landmark 3
    cur_4 = 0   # Landmark 4

    # Input image, create binary mask for contour recognition
    img = cv2.imread(filename)
    ### Debug code:
    # print(img)
    # cv2.imshow("Check image", img)
    # cv2.waitKey()
    img_copy = img.copy()
    im_hsv = cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV)
    im_mask = cv2.inRange(im_hsv, im_lower, im_upper)
    im_mask = cv2.morphologyEx(im_mask, cv2.MORPH_OPEN, kernel)
    ### Debug code:
    # cv2.imshow("Test landmark_recog", im_mask)
    # cv2.waitKey(1000)

    # Finding contours available on image
    cur_cnt, _ = cv2.findContours(im_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Mapping contours found with desired landmarks, comparing parameters
    for c in cur_cnt:
        # Define contour bounding box
        x, y, w, h = cv2.boundingRect(c)
        # Defined range for landmark 1
        if (210 < (x + (w // 2)) < 770) and (250 < (y + (h // 2)) < 720) and (15 < w < 70) and (7 < h < 60):
            cur_x[1] = x + (w // 2)
            cur_y[1] = y + (h // 2)
            cur_1 = cur_1 + 1
        # Defined range for landmarks 2
        elif (880 < (x + (w // 2)) < 1430) and (260 < (y + (h // 2)) < 750) and (15 < w < 70) and (7 < h < 60):
            cur_x[2] = x + (w // 2)
            cur_y[2] = y + (h // 2)
            cur_2 = cur_2 + 1
        # Defined range for landmarks 3
        elif (30 < (x + (w // 2)) < 580) and (500 < (y + (h // 2)) < 960) and (20 < w < 80) and (10 < h < 60):
            cur_x[3] = x + (w // 2)
            cur_y[3] = y + (h // 2)
            cur_3 = cur_3 + 1
        # Defined range for landmarks 4
        elif (950 < (x + (w // 2)) < 1510) and (540 < (y + (h // 2)) < 1010) and (20 < w < 90) and (10 < h < 90):
            cur_x[4] = x + (w // 2)
            cur_y[4] = y + (h // 2)
            cur_4 = cur_4 + 1
    ### Debug code:
    # print(cur_1, cur_2, cur_3, cur_4)

    return cur_1, cur_2, cur_3, cur_4   # Return available contour values

# Translation & Rotation calibration function
def main(trans_rot_mode, filename, cur_1, cur_2, cur_3, cur_4):

    # Switch case for translation/rotation properties, based on the number of landmarks found & check availability
    def case_switch_mode():
        run_flag = 0        # Initiate run_flag, determine if the program could execute or not
        run_mode = 0        # Initiate run_mode, determine if the program run in 4 landmarks mode or 3 landmarks mode
        # run_mode = 1: 4 landmarks mode, run_mode = 0: 3 landmark mode
        cur_toggle = []     # List, determine which landmark could be used

        for i in range(0, 5):   # Initiate cur_toggle list, cur_toggle[0]:cur_toggle[5]
            cur_toggle.append(0)

        # sum_cur variable, quick check if the landmarks could be used or not
        sum_cur = cur_1 + cur_2 + cur_3 + cur_4

        # Case: 4 landmarks found, usable!
        if sum_cur == 4:
            if cur_1 == 1 and cur_2 == 1 and cur_3 == 1 and cur_4 == 1:
                run_flag = 1
                run_mode = 1
            else:   # sum_cur is not correct, check the individuals
                if cur_1 != 1:
                    print("cur_1 = ", cur_1, ", <> 1, eliminate")
                    cur_toggle[1] = 1
                if cur_2 != 1:
                    print("cur_2 = ", cur_2, ", <> 1, eliminate")
                    cur_toggle[2] = 1
                if cur_3 != 1:
                    print("cur_3 = ", cur_3, ", <> 1, eliminate")
                    cur_toggle[3] = 1
                if cur_4 != 1:
                    print("cur_4 = ", cur_4, ", <> 1, eliminate")
                    cur_toggle[4] = 1
                print("Landmarks mismatch!")

        # Case: 3 landmarks found!
        elif sum_cur == 3:
            sum_toggle = 0  # sum_toggle variable, check if sum_cur actually returns 3 usable landmarks
            if cur_1 != 1:
                cur_toggle[1] = 1
            if cur_2 != 1:
                cur_toggle[2] = 1
            if cur_3 != 1:
                cur_toggle[3] = 1
            if cur_4 != 1:
                cur_toggle[4] = 1
            for i in range(0, 5):
                # Taking the sum of cur_toggle, if the value > 1 means there is more than 1 wrong landmark
                sum_toggle = sum_toggle + cur_toggle[i]
            if sum_toggle > 1:
                print("Landmark mismatch")
            else:
                # 3 valid landmarks, proceed to run!
                run_flag = 1
        else:
            print("Missing required landmarks!")

        return run_flag, run_mode, cur_toggle

    # Calculate the center (midpoint of ROI), used as a base for later transformation/rotation
    def midpoint_cal(run_flag, run_mode, cur_toggle):
        global ref_x, ref_y, cur_x, cur_y
        ref_midpoint_x = 0
        ref_midpoint_y = 0
        cur_midpoint_x = 0
        cur_midpoint_y = 0
        if run_flag == 1 and run_mode == 1:     # Calculate using all 4 landmarks
            for i in range(1, 5):
                ref_midpoint_x = ref_midpoint_x + ref_x[i]
                ref_midpoint_y = ref_midpoint_y + ref_y[i]
                cur_midpoint_x = cur_midpoint_x + cur_x[i]
                cur_midpoint_y = cur_midpoint_y + cur_y[i]
            ref_midpoint_x = int(ref_midpoint_x / 4)
            ref_midpoint_y = int(ref_midpoint_y / 4)
            cur_midpoint_x = int(cur_midpoint_x / 4)
            cur_midpoint_y = int(cur_midpoint_y / 4)
        elif run_flag == 1 and run_mode == 0:   # Calculate using 3 available landmarks only
            for i in range(1, 5):
                if cur_toggle[i] == 0:
                    ref_midpoint_x = ref_midpoint_x + ref_x[i]
                    ref_midpoint_y = ref_midpoint_y + ref_y[i]
                    cur_midpoint_x = cur_midpoint_x + cur_x[i]
                    cur_midpoint_y = cur_midpoint_y + cur_y[i]
            ref_midpoint_x = int(ref_midpoint_x / 3)
            ref_midpoint_y = int(ref_midpoint_y / 3)
            cur_midpoint_x = int(cur_midpoint_x / 3)
            cur_midpoint_y = int(cur_midpoint_y / 3)
            ### Debug code":
            # print("This function has been run")
            # print(ref_midpoint_x, ref_midpoint_y, cur_midpoint_x, cur_midpoint_y)

        else:   # run_flag
            print("Landmark mismatch, program cannot execute!")

        return ref_midpoint_x, ref_midpoint_y, cur_midpoint_x, cur_midpoint_y

    # Calculate rotation angle using vector-based calculations
    def rotate_angle(ref_midpoint_x, ref_midpoint_y, cur_midpoint_x, cur_midpoint_y, ref_xx, ref_yy, cur_xx, cur_yy):

        # Determine the reference vector & current vector
        ref_vector = [ref_midpoint_x - ref_xx, ref_midpoint_y - ref_yy]
        cur_vector = [cur_midpoint_x - cur_xx, cur_midpoint_y - cur_yy]

        unit_ref_vector = ref_vector/np.linalg.norm(ref_vector)
        unit_cur_vector = cur_vector/np.linalg.norm(cur_vector)
        dot_prod = np.dot(unit_ref_vector, unit_cur_vector)

        angle = np.arccos(dot_prod) * 180 / 3.1415

        ### Debug code:
        # print(angle)

        return angle

    # Define final rotation calibration case, based on the number of landmark available:
    def run_case(run_flag, run_mode, cur_toggle):
        # case variable for defining cases:
        # case = -1: Program error, not enough information for processing
        # case = 0: 4 landmarks mode
        # case = 1: 3 landmarks mode, landmark 01 eliminated from calculation due to error
        # case = 2: 3 landmarks mode, landmark 02 eliminated from calculation due to error
        # case = 3: 3 landmarks mode, landmark 03 eliminated from calculation due to error
        # case = 4: 3 landmarks mode, landmark 04 eliminated from calculation due to error
        case = -1    # Initiate case, default = -1 to prevent unwanted processing
        if run_flag == 1 and run_mode == 1:
            case = 0
        elif run_flag == 1 and run_mode == 0:
            if cur_toggle[1] == 1:
                case = 1
            if cur_toggle[2] == 1:
                case = 2
            if cur_toggle[3] == 1:
                case = 3
            if cur_toggle[4] == 1:
                case = 4
        else:   # Cannot process image, return error warning!
            case = -1
            print("Not enough landmark information, please check the camera")

        return case

    # Zoom image function, process image before translation & rotation
    def zoom_image(img):
        # Initiate roi list/matrix, we only calculate on 2D plane
        roi = np.float32([[1, 0, 0], [0, 1, 0]])
        # Zoom out image
        # Expand the image to 3000 x 3000 px
        zoom = cv2.warpAffine(img, roi, (3000, 3000))
        # Matching the center point of the original image to the new center point of 3000 x 3000 px image
        shift_image = imutils.translate(zoom, (1500 - 1920/2), (1500 - 1080/2))
        ### Debug code: Show enlarged & shifted image
        # cv2.imshow("Test image", shift_image)
        # cv2.waitKey()

        return shift_image

    # Translation calibration main function
    def translation(shift_image, case, ref_midpoint_x, ref_midpoint_y, cur_midpoint_x, cur_midpoint_y):
        if case != -1:
            # Initiate values
            trans_x = ref_midpoint_x - cur_midpoint_x
            trans_y = ref_midpoint_y - cur_midpoint_y

            # If the shift is around 5 px, the translation is ignored
            # Landmark recognition might have small errors in calculating positions
            if trans_x in range(-5, 6):
                trans_x = 0
            if trans_y in range(-5, 6):
                trans_y = 0
            ### Debug code: Return value to check
            # print(trans_x, trans_y)

            # Return the original position
            shift_copy = shift_image
            shift_revert = imutils.translate(shift_copy, trans_x, trans_y)

        else:
            trans_x = 0
            trans_y = 0
            # Zoom out image
            shift = zoom_image(image)
            # Do nothing, return the original image
            shift_revert = shift

        return shift_revert, trans_x, trans_y

    def rotation(shift_image, case, ref_midpoint_x, ref_midpoint_y, cur_midpoint_x, cur_midpoint_y):

        # Initiate the values
        angle = []              # Rotation angle properties, angle[1]:angle[4] correspond to angle calculations
                                # based on landmark01:landmark04
        angle_final = 0         # Average rotation angle
        for i in range(0, 5):   # Initiate angle list
            angle.append(0)

        ### Debug code:
        # print("Process case = ", case)
        # case = 0, 4 landmarks mode, calculation based on angle[1] and angle[4]
        if case == 0:
            angle[1] = rotate_angle(ref_midpoint_x, ref_midpoint_y, cur_midpoint_x, cur_midpoint_y,
                                    ref_x[1], ref_y[1], cur_x[1], cur_y[1])
            angle[4] = rotate_angle(ref_midpoint_x, ref_midpoint_y, cur_midpoint_x, cur_midpoint_y,
                                    ref_x[4], ref_y[4], cur_x[4], cur_y[4])
            angle_final = round((angle[1] + angle[4])/2)
            # If the current x[1] coordinate > reference x[1] coordinate, image has rotated clockwise, need to revert
            # with a negative angle
            if cur_x[1] > ref_x[1]:
                angle_final = -angle_final
            ### Debug code: Print angle[1], angle[4] & angle_final
            # print(angle[1], angle[4])
            # print(angle_final)
        # case = 2 or case = 3, 3 landmarks mode, calculation based on angle[1] and angle[4]
        if case == 2 or case == 3:
            angle[1] = rotate_angle(ref_midpoint_x, ref_midpoint_y, cur_midpoint_x, cur_midpoint_y,
                                    ref_x[1], ref_y[1], cur_x[1], cur_y[1])
            angle[4] = rotate_angle(ref_midpoint_x, ref_midpoint_y, cur_midpoint_x, cur_midpoint_y,
                                    ref_x[4], ref_y[4], cur_x[4], cur_y[4])
            angle_final = round((angle[1] + angle[4])/2)
            # If the current x[1] coordinate > reference x[1] coordinate, image has rotated clockwise, need to revert
            # with a negative angle
            if cur_x[1] > ref_x[1]:
                angle_final = -angle_final
            ### Debug code: Print angle[1], angle[4] & angle_final
            # print(angle[1], angle[4])
            # print(angle_final)
        if case == 1 or case == 4:
            angle[2] = rotate_angle(ref_midpoint_x, ref_midpoint_y, cur_midpoint_x, cur_midpoint_y,
                                    ref_x[2], ref_y[2], cur_x[2], cur_y[2])
            angle[3] = rotate_angle(ref_midpoint_x, ref_midpoint_y, cur_midpoint_x, cur_midpoint_y,
                                    ref_x[3], ref_y[3], cur_x[3], cur_y[3])
            angle_final = round((angle[2] + angle[3])/2)
            if cur_x[2] > ref_x[2]:
                angle_final = -angle_final
            ### Debug code: Print angle[2], angle[3] & angle_final
            # print(angle[2], angle[3])
            # print(angle_final)
        if case == -1:
            # Do nothing, return the original image. Print out a warning to the user
            print("Landmarks mismatched or misconstructed, image not processed, please check the camera/input")

            rotate_image = shift_image
            return rotate_image, 0
        ### Debug code:
        # print(angle_final)

        # Check if the angle is too large
        if angle_final in range(-12, 13):
            # Rotate the image
            shift_copy = shift_image
            ### Debug code:
            # cv2.imwrite(os.path.join("D:\\21_05_08_result\\debug", "debug.jpg"), shift_copy)
            rotate_mat = cv2.getRotationMatrix2D((3000 // 2, 3000 // 2), angle_final, 1.0)
            ### Debug code: Print debug value
            # cv2.imshow("Image", shift_copy)
            # cv2.waitKey()
            # print(rotate_mat)
            # Rotation calibration
            rotate_image = cv2.warpAffine(shift_copy, rotate_mat, (3000, 3000))
        else:
            print("Image is tilted too much, please check the camera")
            print("The image will not be rotated")

            rotate_image = shift_image

        return rotate_image, angle_final

    # Crop out the original image & save image function
    def save_image(img, case, trans_x, trans_y, angle):

        # Initiate height, width values. Avoid using constant, try using
        height = 1080
        width = 1920
        # Cut the desired image
        cut = img[960:960 + height, 540:540 + width]

        # Drawing cutting slot
        image_out = drawRectangle(cut, slot_coord)

        # Write down the desired image
        # Avoid using static addresses, try using environment variable instead!
        result_path = "D:\\IC DESIGN LAB\\[LAB] PRJ.Parking Lot\\IMAGE_CALIBRATION_V2\\data_process\\calib_image"     # Image save path
        name = os.path.splitext(filename)[0]    # Separate filename, remove the extension
        cv2.imwrite(os.path.join(result_path, 'recov_{}_({}_{}_{}).jpg'.format(name, trans_x, trans_y, angle)), image_out)
        if case != -1:
            print(filename, " recovered")
        else:
            # cv2.imwrite(os.path.join(result_path, 'not_recov_{}.jpg'.format(name)), cut)
            print(filename, " not recovered, please check the camera/input")


    def drawRectangle(image, cd):
        image_out = image
        for i in range(0, 20):
            if i in range(0, 8):
                cv2.rectangle(image_out, (cd[1][i] - 75, cd[2][i] - 75), (cd[1][i] + 75, cd[2][i] + 75), (0, 255, 0), 2)
            elif i in range(8, 14):
                cv2.rectangle(image_out, (cd[1][i] - 45, cd[2][i] - 45), (cd[1][i] + 45, cd[2][i] + 45), (0, 255, 0), 2)
            else:
                cv2.rectangle(image_out, (cd[1][i] - 35, cd[2][i] - 35), (cd[1][i] + 35, cd[2][i] + 35), (0, 255, 0), 2)
        return image_out

    # Connect functions
    image = cv2.imread(filename)
    run_fl, run_md, cur_togg = case_switch_mode()
    ref_mid_x, ref_mid_y, cur_mid_x, cur_mid_y = midpoint_cal(run_fl, run_md, cur_togg)
    r_case = run_case(run_fl, run_md, cur_togg)
    slot_fileflag, slot_coord = info_open_slot()
    ### Debug code:
    print("Working case: ", r_case)
    # print(ref_x)
    # print(ref_y)
    # print(cur_x)
    # print(cur_y)
    # Zoom out image
    process_image = zoom_image(image)
    ### Both image translation and rotation calibration
    # rot_image, rotAngle = rotation(process_image, r_case, ref_mid_x, ref_mid_y, cur_mid_x, cur_mid_y)
    # trans_image, transX, transY = translation(rot_image, r_case, ref_mid_x, ref_mid_y, cur_mid_x, cur_mid_y)
    ### In case of running image translation calibration only:
    if trans_rot_mode == 1:
        trans_image, transX, transY = translation(process_image, r_case, ref_mid_x, ref_mid_y, cur_mid_x, cur_mid_y)
        rotAngle = 0

        save_image(trans_image, r_case, transX, transY, rotAngle)
    ### In case of running image rotation calibration only:
    if trans_rot_mode == 2:
        transX = 0
        transY = 0
        rot_image, rotAngle = rotation(process_image, r_case, ref_mid_x, ref_mid_y, cur_mid_x, cur_mid_y)
        save_image(rot_image, r_case, transX, transY, rotAngle)

