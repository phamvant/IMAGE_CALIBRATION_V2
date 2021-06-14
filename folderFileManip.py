import os.path
from os import path

# os.getcwd()
# print(os.listdir())
# Test name functions
# input_name = input("Write your input name here: ")

def folder_manip(input_name): #creating project working directories
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

    # Return the folder pointer to main folder
    os.chdir(path_parent)
    ### Debug: Print current working directory
    # print(os.getcwd())

    #print(os.listdir)

def file_manip(input_name): #making log files for future access

    path_parent = os.getcwd()
    #print(pathParent)

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

# folder_manip(input_name)
# file_manip(input_name)


