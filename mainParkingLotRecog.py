import os
import cv2

# import folderFileManip    # Unused
import userDefine as usrDef
import myTranslation as myTrans

# folderFileManip.folderManip()
# folderFileManip.fileManip()

while True:
    os.system('cls')
    print("_Welcome to Parking Lot recognition_")
    print("_To continue, please select one of these functions_")
    print("___0. Exit the program___")
    print("___1. Define new parking slot___")
    print("___2. Run parking lot recognition automatically___")
    print("____Select function: ")
    path_parent = os.getcwd()
    key = input()
    if int(key) == 1:
        print("_You have selected Define new parking slot_")
        os.chdir(path_parent)
        image_ref = cv2.imread(".\\data_process\\ref_image\\imageplaceholder.jpg")
        usrDef.user_define(image_ref)
        print(os.getcwd())
    elif int(key) == 2:
        os.chdir(path_parent)
        f_runTime = open(path_parent+"\\data_process\\runTime.txt", 'r')
        checkDef = f_runTime.read()
        if checkDef == '0':
            print('_Parking lot has not been defined. Please define before running this mode_')
        else:
            print("_System now supervising parking lot automatically_")
            # Main program calls & execution
            # Avoid using static address! Use environment variable for this instead!
            os.chdir("D:\\IC DESIGN LAB\\[LAB] PRJ.Parking Lot\\IMAGE_CALIBRATION_V2\\data_process\\data")
            # Open landmarks information
            flag, ref_x, ref_y = myTrans.infoOpen()
            ### Debug code:
            # print(flag)
            # print(ref_x)
            # print(ref_y)
            if flag == 1:
                print("Parking lot is yet to be defined, exit")
            else:
                ### Debug code:
                # print(path_parent+"\\data_process\\data")

                for filename in os.listdir(os.getcwd()):
                    image = cv2.imread(filename)

                    ### Debug code:
                    # print(filename)
                    # print(os.stat(filename).st_size)
                    # cv2.imshow("Read image", image)
                    # cv2.waitKey()

                    cur1, cur2, cur3, cur4 = myTrans.landmark_recog(filename)
                    myTrans.main(filename, cur1, cur2, cur3, cur4)
                    print("")

            print("_System has finished monitoring. Now exit_")
            break
    if int(key) == 0:
        print("_Program terminated")
        break
    print("___Press Enter to continue___")
    cont = input()
