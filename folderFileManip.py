# Import required libraries
import os.path
from os import path

# os.getcwd()
# print(os.listdir())
# Test name functions
# input_name = input("Write your input name here: ")

# Create required working directory if needed
def folder_manip(input_name):
    path_parent = os.getcwd()
    ### Debug: Print the parent folder name
    # print(path_parent)

    # Define folder_make command:
    def folder_make(folder_name):
        if not path.exists(folder_name):
            os.mkdir(folder_name)
            print(folder_name + ' created!')
        else:
            print(folder_name + ' existed!')
        return

    # Create folder with name
    folder_make(input_name)
    os.chdir("./{}".format(input_name))
    # Create sub-directories
    folder_make("calib_image")
    folder_make("data")
    folder_make("park_lot_info")
    folder_make("ref_image")
    folder_make("calib_image_cut")

    # Return the folder pointer to main folder
    os.chdir(path_parent)
    ### Debug: Print current working directory
    # print(os.getcwd())

    # print(os.listdir)

# Create required working files
def file_manip(input_name):  # Making log files for future access
    path_parent = os.getcwd()
    ### Debug: Print working directory
    # print(pathParent)

    def file_make(filename):
        if not path.isfile(filename):
            f = open(filename, "w")
            f.close()
            print(filename + ' created!')
        else:
            print(filename + ' existed!')

    # Move inside requested folder
    os.chdir(".\\{}".format(input_name))

    # Create files to store debug data
    file_make("debug.txt")
    file_make("runTime.txt")

    # Create files to store parking lot data
    os.chdir(".\\park_lot_info")
    file_make("slot.txt")
    file_make("landmark.txt")

    os.chdir(path_parent)

# Open available parking lot file, append positions to a list
def file_open_avail_parklot(parent_path):
    # Initiate values
    file_flag = 0
    avail_parklot = []

    # Open file contains defined parking lot name
    # Avoid using static addresses
    f_avail_parklot = open(parent_path + "\\data_process\\avail_parklot.txt", 'r+')
    if os.stat(os.getcwd() + "\\data_process\\avail_parklot.txt").st_size == 0:
        # Indicates if the parking lot is defined or not. If not, halt the processing program
        file_flag = 1                               # Not defined value
        avail_parklot = None
        return avail_parklot, file_flag
    else:
        string_x = ""
        # Initiate new list, get the value from the list
        lis = [line.split() for line in f_avail_parklot]
        file_length = len(lis)

        for ii in range(file_length):
            for val in lis[ii]:
                string_x = val
            avail_parklot.append(string_x)
    f_avail_parklot.close()

    return avail_parklot, file_flag

# Add new parking lot to the monitoring file
def file_append_avail_parklot(parent_path, new_parklot_name):
    # Initiate values:
    # Avoid using static addresses
    f_avail_parklot = open(parent_path + "\\data_process\\avail_parklot.txt", 'a+')
    f_avail_parklot.write("\n")
    f_avail_parklot.write(new_parklot_name)
    f_avail_parklot.close()

    return 0

# Rewrite the parking lot's parking slots' positions
def file_slot_write(parent_path, park_lot_name, slot_x, slot_y, num_of_slot):
    # Initiate values:
    f_slot = open(parent_path + "\\data_process\\{}\\park_lot_info\\slot.txt".format(park_lot_name), 'w+')
    # Write slot coordinates to the file
    for slot_index in range(1, num_of_slot+1):
        f_slot.write('%d ' % slot_index)
        f_slot.write('%d ' % slot_x[slot_index])
        f_slot.write('%d\n' % slot_y[slot_index])

    f_slot.close()

    return 0

# Rewrite the landmarks' positions
def file_landmark_write(parent_path, ref_xx, ref_yy, park_lot_name):
    # Initiate values:
    # Avoid using static addresses
    f_landmark = open(parent_path + "\\data_process\\{}\\park_lot_info\\landmark.txt".format(park_lot_name), 'w+')
    f_runt = open(parent_path + "\\data_process\\{}\\runTime.txt".format(park_lot_name), 'w+')
    # Write value to the file
    f_runt.write('1')
    # Write landmark coordinates to the file
    for landmark_index in range(1, 5):
        f_landmark.write('%d ' % landmark_index)
        f_landmark.write('%d ' % ref_xx[landmark_index])
        f_landmark.write('%d\n' % ref_yy[landmark_index])

    f_landmark.close()
    f_runt.close()

    return 0

# Remove all folder content before an another run, to avoid image show errors
# A better approach to file management is recommended. Deleting files is not recommended.
def remove_folder_content(address):
    for file_name in os.listdir(address):
        if os.path.exists(os.path.join(address, file_name)):
            os.remove(os.path.join(address, file_name))