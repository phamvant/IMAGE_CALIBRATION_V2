import os

def file_open_avail_parklot():
    # Initiate values
    file_flag = 0
    avail_parklot = []

    # Open file contains defined parking lot name
    f_avail_parklot = open("D:\\IC DESIGN LAB\\[LAB] PRJ.Parking Lot\\IMAGE_CALIBRATION_V2\\data_process"
                           "\\avail_parklot.txt", 'r+')

    if os.stat("D:\\IC DESIGN LAB\\[LAB] PRJ.Parking Lot\\IMAGE_CALIBRATION_V2"
               "\\data_process\\avail_parklot.txt").st_size == 0:
        file_flag = 1
        avail_parklot = None
        return avail_parklot, file_flag
    else:
        lis = [line.split() for line in f_avail_parklot]
        file_length = len(lis)

        for i in range (file_length):
            for val in lis[i]:
                strx = val
            avail_parklot.append(strx)

    return avail_parklot, file_flag

list_of_parking_lot, avail_flag = file_open_avail_parklot()
size_of_list_parklot = len(list_of_parking_lot)
for i in range(0, size_of_list_parklot):
    print(list_of_parking_lot[i])
print(size_of_list_parklot)

