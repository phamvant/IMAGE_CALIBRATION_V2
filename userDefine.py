import os
import cv2
import ctypes

def user_define(image):
    min_point = ()
    max_point = ()

    # Function: click and crop, use to add functions to mouse
    def click_and_crop(event, x, y, flags, param):
        nonlocal min_point, max_point
        # Mouse-click activate
        if event == cv2.EVENT_LBUTTONDOWN:
            min_point = (x, y)
        # Mouse-release activate
        elif event == cv2.EVENT_LBUTTONUP:
            max_point = (x, y)
            # Draw a rectangle around the region of interest
            cv2.rectangle(image_gui, min_point, max_point, (0, 255, 0), 2)
            cv2.imshow('User define on Image', image_gui)

    def getSysScr_Windows(ratio):
        user32 = ctypes.windll.user32
        scr_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        scr_width_in = int(scr_size[0] * ratio)
        scr_height_in = int(scr_size[1] * ratio)
        return scr_width_in, scr_height_in

    def image_read(imgR):  # This will be replaced in the future
        height_in, width_in = imgR.shape[:2]
        return imgR, height_in, width_in

    def gui_draw(image):
        # Draw a guidance grid onto the image
        grid_img = cv2.imread(os.getcwd()+"\\data_process\\ref_image\\imGrid.png")
        # cv2.imshow("Image", grid_img)
        # cv2.waitKey()

        rows, cols, channel = grid_img.shape
        roi = image[0:rows, 0:cols]

        img2gray = cv2.cvtColor(grid_img, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(img2gray, 200, 255, cv2.THRESH_BINARY_INV)
        mask_inv = cv2.bitwise_not(mask)
        img = cv2.bitwise_and(roi, roi, mask=mask_inv)
        grid_img_fg = cv2.bitwise_and(grid_img, grid_img, mask=mask)
        img = cv2.add(img, grid_img_fg)

        # Draw instruction box to the image
        cv2.rectangle(img, (1480, 940), (1910, 1070), (255, 255, 255), -1)
        cv2.rectangle(img, (1480, 940), (1910, 1070), (0, 127, 0), 3)

        text_01 = "Drag mouse over region of interest"
        text_02 = "Press M to save to Landmarks"
        text_03 = "Press S to save to Parking Slots"
        text_04 = "Press B to end the program"
        font = cv2.FONT_HERSHEY_SIMPLEX

        cv2.putText(img, text_01, (1495, 965), font, 0.7, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(img, text_02, (1515, 995), font, 0.7, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.putText(img, text_03, (1515, 1025), font, 0.7, (255, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(img, text_04, (1515, 1055), font, 0.7, (0, 0, 0), 1, cv2.LINE_AA)

        return img

    # Initiate files & values
    f_landmark = open(os.getcwd() + "\\data_process\\park_lot_info\\landmark.txt", 'w+')
    f_slot = open(os.getcwd() + "\\data_process\\park_lot_info\\slot.txt", 'w+')
    f_runTime = open(os.getcwd() + "\\data_process\\runTime.txt", 'w+')
    f_runTime.write('1')
    imageR, height, width = image_read(image)
    scr_scale = 5 / 6
    scr_width, scr_height = getSysScr_Windows(scr_scale)
    image_gui = gui_draw(imageR)

    # Check image_gui - image with gridlines & guidebox
    """ 
    cv2.imshow("Image", image_gui)
    cv2.waitKey()
    cv2.destroyWindow("Image")
    """

    # Initiate GUI, set click and crop as main function
    cv2.namedWindow("User define on Image", cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback("User define on Image", click_and_crop)
    slotNumber = 0
    lmNumber = 0
    while True:
        # Display the image for selection purpose only (used for PyCharm)
        image_gui = cv2.resize(image_gui, (scr_width, scr_height))
        cv2.imshow("User define on Image", image_gui)
        key = cv2.waitKey(1000) & 0xFF
        # print(min_point) print(max_point) # Check min_point, max_point value to see if mouse is functional
        # If the 'b' key is pressed, break from the program
        if key == ord("b"):
            break
        # If the 's' key is pressed, write the coordinates of SLOTS' vertices to txt file
        elif key == ord("s"):
            print(min_point[0], ' ', min_point[1], ' to ', max_point[0], ' ', max_point[1])
            slotNumber = slotNumber + 1
            f_slot.write('%d ' % slotNumber)
            f_slot.write('%d %d ' % (int(min_point[0] * width / scr_width), int(min_point[1] * height / scr_height)))
            f_slot.write('%d %d\n' % (int(max_point[0] * width / scr_width), int(max_point[1] * height / scr_height)))
        # If the 'm' key is pressed, write the coordinates of LANDMARKS' centroids to txt file
        elif key == ord("m"):
            print(min_point[0], ' ', min_point[1], ' to ', max_point[0], ' ', max_point[1])
            lmNumber = lmNumber + 1
            f_landmark.write('%d ' % lmNumber)
            # x-axis coordinate
            f_landmark.write('%d ' % (int((min_point[0] + max_point[0]) * width / (scr_width * 2))))
            # y-axis coordinate
            f_landmark.write('%d\n' % (int((min_point[1] + max_point[1]) * width / (scr_width * 2))))

    # Close files, kill GUI
    f_runTime.close()
    f_slot.close()
    f_landmark.close()
    cv2.destroyAllWindows()

