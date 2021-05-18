import os.path
from os import path

#os.getcwd()
#print(os.listdir())
def folderManip(): #creating project working directories
    pathParent = os.getcwd()
    print(pathParent)
    #Define folderMake command:
    def folderMake(folder_name):
        if (path.exists(folder_name) == False):
            os.mkdir(folder_name)
            print(folder_name + ' created!')
        else:
            print(folder_name + ' existed!')
    #DataProcess Folder, parent folder for all files:
    folderMake('DataProcess')
    os.chdir('.\DataProcess')
    #Reference image folder:
    folderMake('RefImg')
    #Calibrated image folder:
    folderMake('CalibImg')
    #Recognized image folder:
    folderMake('RecogImg')
    #ParkingLotInfo folder:
    folderMake('PkLotInfo')
    #Background image set folder:
    folderMake('BgImgSet')
    #Slot masks folder:
    folderMake('SlotMsk')
    #Background subtraction weights folder:
    folderMake('BgSub')
    #Data storage/Test data storage folder:
    folderMake('Data')

    #Debug properties:
    folderMake('Debug')
    os.chdir(pathParent+'\DataProcess\Debug')
    folderMake('OriginalImg')
    folderMake('CalibImg')
    folderMake('CutImg')

    os.chdir(pathParent)
    #print(os.getcwd())

    #print(os.listdir)

def fileManip(): #making log files for future access

    pathParent = os.getcwd()
    #print(pathParent)

    def fileMake(filename):
        if (path.isfile(filename) == False):
            f = open(filename, "w")
            f.close()
            print(filename+' created!')
        else:
            print(filename+ ' existed!')

    #print(os.getcwd())
    os.chdir('.\DataProcess')

    #print(os.getcwd())

    #ParkingLotInfo log file create:
    os.chdir('.\PkLotInfo')
    fileMake("landmark.txt")
    fileMake("slot.txt")
    #BG Subtract log file create:
    os.chdir(pathParent+'\DataProcess\BgSub')
    #print(os.getcwd())
    fileMake("weights.txt")
    #Create run file to check run number
    os.chdir(pathParent+'\DataProcess')
    fileMake("runTime.txt")
    f_runTime = open("runTime.txt", 'w+')
    f_runTime.write('0')                    #Clear the definition to force running
    f_runTime.close()

    #Debug properties
    os.chdir(pathParent+'\DataProcess\Debug')
    fileMake("MarkRecogDebug.csv")

#folderManip()
#fileManip()



