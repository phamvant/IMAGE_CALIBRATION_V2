# This is the file containing test layout for ImageCalibration
# The layout is in development
### Import libraries/packages
# ---------------------------------------------------------------------------------------------------------------------
import os
import io
# Import required processing libraries/packages
import PySimpleGUI as sg
import ctypes
import cv2

from PIL import Image, ImageTk
# Import image calibration algorithm file
import myTranslation as mytrans
# ---------------------------------------------------------------------------------------------------------------------


### Define additional functions:
# ---------------------------------------------------------------------------------------------------------------------
# Get native screen resolution, times the ratio for native compatible resolution, avoid bleeding edges
def get_scr_size(ratio):
    user32 = ctypes.windll.user32                                       # ctypes function
    scr_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)   # ctypes function, returns a list of parameters
    scr_width = scr_size[0]
    scr_height = scr_size[1]
    width = int(scr_width * ratio)                                      # get width*ratio, for later GUI scaling
    height = int(scr_height * ratio)                                    # get height*ratio, for later GUI scaling

    return width, height

# Draw a grid on to the image, using an overlay image of grid
# Could use an another approach, using PySimpleGUI graphing functions since images are shown on graph-based canvas
def gui_draw(file_name):
    # Draw a guidance grid onto the image
    img = cv2.imread(file_name)
    # Avoid using static addresses
    # Use this instead, but be cautious :
    # gridImg = cv2.imread(os.getcwd() + "\\data_process\\ref_image\\imGrid.png")
    # Make sure the working files are in the right positions before use
    gridImg = cv2.imread("D:\\IC DESIGN LAB\\[LAB] PRJ.Parking Lot"
                         "\\IMAGE_CALIBRATION_V2\\data_process\\ref_image\\imGrid.png")
    ### Debug: show Grid image
    # cv2.imshow("Image", gridImg)
    # cv2.waitKey()

    rows, cols, channel = gridImg.shape
    roi = img[0:rows, 0:cols]

    # Add grid to the selected reference image
    img2gray = cv2.cvtColor(gridImg, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 200, 255, cv2.THRESH_BINARY_INV)
    mask_inv = cv2.bitwise_not(mask)
    img = cv2.bitwise_and(roi, roi, mask=mask_inv)
    gridImg_fg = cv2.bitwise_and(gridImg, gridImg, mask=mask)
    img = cv2.add(img, gridImg_fg)

    # Get file name, write the image with grid. This will be used in later processing
    name = os.path.splitext(filename)[0]+"_grid.jpg"
    # Avoid using static addresses
    # Use this instead, but be cautious:
    # file_path = os.path.join(os.getcwd()+"\\data_process\\ref_image", name)
    file_path = os.path.join("D:\\IC DESIGN LAB\\[LAB] PRJ.Parking Lot"
                             "\\IMAGE_CALIBRATION_V2\\data_process\\ref_image", name)
    cv2.imwrite(file_path, img)
    return file_path

# Convert image data to base64 values, for later drawing on graph canvas
def get_img_data(f, max_size, first=False):
    img = Image.open(f)
    img.thumbnail(max_size, resample=Image.BICUBIC)
    if first:
        b_io = io.BytesIO()
        img.save(b_io, format="PNG")
        del img
        return b_io.getvalue()
    return ImageTk.PhotoImage(img)

# Open available parking lot file, append positions to a list
def file_open_avail_parklot():
    # Initiate values
    file_flag = 0
    avail_parklot = []

    # Open file contains defined parking lot name
    # Avoid using static addresses
    f_avail_parklot = open("D:\\IC DESIGN LAB\\[LAB] PRJ.Parking Lot\\IMAGE_CALIBRATION_V2\\data_process"
                           "\\avail_parklot.txt", 'r+')
    if os.stat("D:\\IC DESIGN LAB\\[LAB] PRJ.Parking Lot\\IMAGE_CALIBRATION_V2"
               "\\data_process\\avail_parklot.txt").st_size == 0:
        # Indicates if the parking lot is defined or not. If not, halt the processing program
        file_flag = 1                               # Not defined value
        avail_parklot = None
        return avail_parklot, file_flag
    else:
        strx = ""
        # Initiate new list, get the value from the list
        lis = [line.split() for line in f_avail_parklot]
        file_length = len(lis)

        for i in range(file_length):
            for val in lis[i]:
                strx = val
            avail_parklot.append(strx)
    f_avail_parklot.close()

    return avail_parklot, file_flag

# Add new parking lot name to available parking lot, if that parking lot is yet to be defined
# This function is sensitive to the text file's structure & last written position
# Modify if needed
def file_append_avail_parklot(new_parklot_name):
    # Initiate values:
    # Avoid using static addresses
    f_avail_parklot = open("D:\\IC DESIGN LAB\\[LAB] PRJ.Parking Lot\\IMAGE_CALIBRATION_V2\\data_process"
                           "\\avail_parklot.txt", 'a+')
    f_avail_parklot.write("\n")
    f_avail_parklot.write(new_parklot_name)
    f_avail_parklot.close()

    return 0

# Rewrite the parking lot's parking slots' positions
def file_slot_write(slot_x, slot_y, num_of_slot):
    # Initiate values:
    slot_index = 0
    f_slot = open("D:\\IC DESIGN LAB\\[LAB] PRJ.Parking Lot\\IMAGE_CALIBRATION_V2"
                  "\\data_process\\park_lot_info\\slot.txt", 'w+')
    # Write slot coordinates to the file
    for slot_index in range(1, num_of_slot+1):
        f_slot.write('%d ' % slot_index)
        f_slot.write('%d ' % slot_x[slot_index])
        f_slot.write('%d\n' % slot_y[slot_index])

    f_slot.close()

    return 0

# Rewrite the landmarks' positions
def file_landmark_write(ref_x, ref_y):
    # Initiate values:
    # Avoid using static addresses
    landmark_index = 0
    f_landmark = open("D:\\IC DESIGN LAB\\[LAB] PRJ.Parking Lot\\IMAGE_CALIBRATION_V2"
                      "\\data_process\\park_lot_info\\landmark.txt", 'w+')
    f_runtime = open("D:\\IC DESIGN LAB\\[LAB] PRJ.Parking Lot\\IMAGE_CALIBRATION_V2"
                     "\\data_process\\runTime.txt", 'w+')
    # Write value to the file
    f_runtime.write('1')
    # Write landmark coordinates to the file
    for landmark_index in range(1, 5):
        f_landmark.write('%d ' % landmark_index)
        f_landmark.write('%d ' % ref_x[landmark_index])
        f_landmark.write('%d\n' % ref_y[landmark_index])

    f_landmark.close()
    f_runtime.close()

    return 0

# Remove all folder content before an another run, to avoid image show errors
def remove_folder_content(address):
    for filename in os.listdir(address):
        if os.path.exists(os.path.join(address, filename)):
            os.remove(os.path.join(address, filename))
# ---------------------------------------------------------------------------------------------------------------------


# Initiate values
# ---------------------------------------------------------------------------------------------------------------------
index = 0  # index for below lists - Reference landmark position list & Slot position list
ref_pos_x = []  # Reference landmark coordinate, x-axis
ref_pos_y = []  # Reference landmark coordinate, y-axis
slot_pos_x = []  # Slot coordinate, x-axis
slot_pos_y = []  # Slot coordinate, y-axis

# Avoid using static values, try using an input to get this value
number_of_slot = 20  # Define number of slots

# Initiate above lists
for i in range(0, 5):
    ref_pos_x.append(0)
    ref_pos_y.append(0)
for j in range(0, number_of_slot + 1):
    slot_pos_x.append(0)
    slot_pos_y.append(0)

# Screen scaling ratio. This value must < 1 to get a fullscreen GUI without bleeding edges
scale = 2 / 3

# Initiate screen size, get max GUI resolution
wid, hght = get_scr_size(scale)
maxsize = (wid, hght)

# Define image files, which should be used in later definitions
file_types = [("JPEG (*.jpg)", ".jpg"),
              ("All files (*.*)", "*.*")]

# Define a list, emulating reading different parking lot
list_of_parking_lot, avail_flag = file_open_avail_parklot()
size_of_list_parklot = len(list_of_parking_lot)

### Debug: Available parking lots
# for i in range(0, size_of_list_parklot):
#    print(list_of_parking_lot[i])
# ---------------------------------------------------------------------------------------------------------------------


### Define layouts
# ---------------------------------------------------------------------------------------------------------------------
# Layout 1/layout_open
layout_open = [[sg.Text('IMAGE CALIBRATION', font='Arial')],
               [sg.Button('Define new parking lot', key='-DEFNEW-')],
               [sg.Button('Run automatically', key='-RUNAUTO-')]]

# Layout 2/layout_defnew_1
layout_defnew_1 = [[sg.Text('DEFINE NEW PARKING LOT')],
                   [sg.Text('Please input new parking lot name')],
                   [sg.InputText(key='-NEW_PARKLOT_NAME-')],
                   [sg.Button('Enter new name', key='-ENTER_NAME-')],
                   [sg.Text("This parking lot has been defined, select Redefine or Run auto instead",
                            key='-RET_MSG_DEFNEW1-', visible=False)],
                   [sg.Text("Parking lot name is blank, please try again", key='-NAME_BLANK-', visible=False)],
                   [sg.Button('Back', key ='-BACK_2-')],
                   [sg.Button('Next', key='-DEFINE_01-', visible=False),
                    sg.Button('Redefine', key='-REDEFINE_DEF-', visible=False),
                    sg.Button('Run auto', key='-RUN_DEF-', visible=False)]
                   ]

# Layout 3/layout_runauto_1
layout_runauto_1 = [[sg.Text("RUN CALIBRATING AUTOMATICALLY")],
                    [sg.Text("Select one of these defined parking lot")],
                    [sg.Listbox(values=list_of_parking_lot, select_mode='single', key='-PARKLOT-', size=(30, 6))],
                    [sg.Button('Back', key='-BACK_3-'),
                     sg.Button('Redefine', key='-REDEFINE-'), sg.Button('Run auto', key='-RUN-')]]

# Layout 4/layout_defnew_2
layout_defnew_2 = [[sg.Text('DEFINE PARKING LOT')],
                   [sg.Text('Select reference image')],
                   [sg.Text('Choose a file: '), sg.Input(size=(30, 1), key='-REFIMG-'),
                    sg.FileBrowse(file_types=file_types)],
                   [sg.Button("Load image")],
                   [sg.Image(key="-IMAGE-")],
                   [sg.Button('Back', key='-BACK_4-'), sg.Button('Next', key='-DEFINE_02-', visible=False)]]

# Layout 5/layout_defnew3:
layout_1 = [[sg.Graph(canvas_size=(wid, hght),
                      graph_bottom_left=(0, 720),
                      graph_top_right=(1280, 0),
                      enable_events=True,
                      drag_submits=True,
                      key='-GRAPH-')],
            [sg.InputText(size=(10, 1), key='-LM_NUM-'),
             sg.Button("Save as Landmark", key='-SAVE_LM-'),
             sg.InputText(size=(10, 1), key='-SLOT_NUM-'),
             sg.Button("Save as ParkSlot", key='-SAVE_SLOT-'),
             sg.Button("Save PSlot file", key='-REDEF_SLOT-', visible=False)],
            [sg.Button('Back', key='-BACK_5-'), sg.Button('Finish', key='-FIN-')]]

layout_2 = [[sg.Text(key='-INFO-', size=(50, 1))],
            [sg.Text(key='-LM_1-', size=(30, 1))],
            [sg.Text(key='-LM_2-', size=(30, 1))],
            [sg.Text(key='-LM_3-', size=(30, 1))],
            [sg.Text(key='-LM_4-', size=(30, 1))]]

layout_defnew_3 = [[sg.Text('DEFINE PARKING LOT')],
                   [sg.Text('Define landmarks & parking slots')],
                   [sg.Column(layout_1), sg.Column(layout_2)]]

# Layout 6/layout_select_calib_mode
layout_select_calib_mode = [[sg.Text("SELECT CALIBRATION TYPE")],
                 [sg.Button('Translation', key='-TRANS-'), sg.Button('Rotation', key='-ROL-')],
                 [sg.Button('Back', key='-BACK_6-')]]

# Layout 7/layout_wait_error
layout_wait_error = [[sg.Text("WAIT SCREEN")],
                     [sg.Text("Parking lot has not been defined, please define before run", key='-NOT_DEF-',
                              visible=False)],
                     [sg.Text("Parking lot processing, please wait", key='-WAIT-',
                              visible=False)],
                     [sg.Text(key="-PROCESSING_FILE-", size=(60, 1), visible=False)],
                     [sg.ProgressBar(1, orientation='h', size=(80, 20), key='-PROG_BAR-')],
                     [sg.Text("Program finished monitoring", key='-FINISHED-', visible=False)],
                     [sg.Button("Show result", key='-SHOW_RES-', visible=False)]]

# Layout 8/layout_results
result_col_1 = [[sg.Text("Before calibration")],
                [sg.Graph(canvas_size=(640, 360),
                          graph_bottom_left=(0, 360),
                          graph_top_right=(640, 0),
                          background_color='white',
                          enable_events=True,
                          key='-BEFORE_CALIB-')]]

result_col_2 = [[sg.Text("After calibration")],
                [sg.Graph(canvas_size=(640, 360),
                          graph_bottom_left=(0, 360),
                          graph_top_right=(640, 0),
                          background_color='white',
                          enable_events=True,
                          key='-AFTER_CALIB-')]]

layout_result = [[sg.Text("RESULTS")],
                 [sg.Text("Before and After Calibration")],
                 [sg.Column(result_col_1), sg.Column(result_col_2)],
                 [sg.Button("Prev Image", key='-PREV_IMG-'), sg.Button("Next Image", key='-NEXT_IMG-')],
                 [sg.Button("Back to define", key='-BACK2DEF-'), sg.Button("Close the program", key='-CLOSE_PROG-')]]

# Total layout to main program
layout = [[sg.Column(layout_open, key='lay_1', element_justification='center'),
           sg.Column(layout_defnew_1, visible=False, key='lay_2'),
           sg.Column(layout_runauto_1, visible=False, key='lay_3'),
           sg.Column(layout_defnew_2, visible=False, key='lay_4'),
           sg.Column(layout_defnew_3, visible=False, key='lay_5'),
           sg.Column(layout_select_calib_mode, visible=False, key='lay_6'),
           sg.Column(layout_wait_error, visible=False, key='lay_7'),
           sg.Column(layout_result, visible=False, key='lay_8')],
          [sg.Button('Cycle layout'), sg.Button('1'), sg.Button('2'), sg.Button('3'),
           sg.Button('4'), sg.Button('5'), sg.Button('6'), sg.Button('7'), sg.Button('8'),
           sg.Button('Exit')]]
# ---------------------------------------------------------------------------------------------------------------------


# GUI initiate values:
# ---------------------------------------------------------------------------------------------------------------------
# Initiate main window
window = sg.Window('Image Calibration', layout, element_justification='center',
                   resizable=True, finalize=True)
# Initiate layout
layout = 1
# Initiate additional graph value, for layout 6 & layout 8
graph = window['-GRAPH-']
before_calib = window['-BEFORE_CALIB-']
after_calib = window['-AFTER_CALIB-']
# Initiate index for image viewer, layout 8
result_image_index = 0
# Enable/Disable dragging variables, for drawing on graph
dragging = False
start_point = end_point = prior_rect = None
# ---------------------------------------------------------------------------------------------------------------------


# GUI switching functions
# ---------------------------------------------------------------------------------------------------------------------
while True:
    # Terminate program
    # ----------------------------------------------------------------------
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit' or event == '-CLOSE_PROG-':
        break
    # ----------------------------------------------------------------------

    # Work with Back function
    # -----------------------------------------------------------------------------------------------------------------
    if event == '-BACK_2-' or event == '-BACK_3-' or event == '-BACK_4-' or event == '-BACK_5-' or event == '-BACK_6-':
        if layout == 2 or layout == 3 or layout == 4:
            window[f'lay_{layout}'].update(visible=False)       # Toggle current layout off
            layout = 1                                          # Update desired layout value
            window[f'lay_{layout}'].update(visible=True)        # Toggle new layout on
        elif layout == 5:
            window[f'lay_{layout}'].update(visible=False)
            layout = 4
            window[f'lay_{layout}'].update(visible=True)
        elif layout == 6:
            window[f'lay_{layout}'].update(visible=False)
            layout = 5
            window[f'lay_{layout}'].update(visible=True)
    # -----------------------------------------------------------------------------------------------------------------

    # Work with define new parking lot
    # -----------------------------------------------------------------------------------------------------------------
    if event == '-DEFNEW-':                             # Change to enter new name layout
        window[f'lay_{layout}'].update(visible=False)
        layout = 2
        window[f'lay_{layout}'].update(visible=True)

    if event == '-ENTER_NAME-':                         # If enter new name button is pressed
        match = 0
        parklot_name = values['-NEW_PARKLOT_NAME-']
        print(parklot_name)
        if parklot_name == "":                          # Check if new name is blank. Blank name cannot be used
            window['-NAME_BLANK-'].update(visible=True) # Blank name message, visible = True
            window['-DEFINE_01-'].update(visible=False) # Next button, visible = False
            continue                                    # Continue receiving new name

        for i in range(0, size_of_list_parklot):        # Check if name is used, means parking lot is defined
            if parklot_name == list_of_parking_lot[i]:
                match = 1                               # Found matching result!
        if match == 1:         # Display Redefine, RunAuto option. Not append this new name since it's already available
            window['-RET_MSG_DEFNEW1-'].update(visible=True)    # Matched name message, visible = True
            parklot_name = list_of_parking_lot[i]               # Take the available name instead (Redundant?)
            window['-REDEFINE_DEF-'].update(visible=True)       # Redefine button, visible = True
            window['-RUN_DEF-'].update(visible=True)            # RunAuto button, visible = True
            window['-DEFINE_01-'].update(visible=False)         # Next button, visible = False
            window['-NAME_BLANK-'].update(visible=False)        # Blank name message, visible = False
        else:                                            # No matching name found. This name need to be added
            window['-DEFINE_01-'].update(visible=True)          # Next button, visible = True
            window['-REDEFINE_DEF-'].update(visible=False)      # Redefine button, visible = False
            window['-RUN_DEF-'].update(visible=False)           # RunAuto button , visible = False
            window['-RET_MSG_DEFNEW1-'].update(visible=False)   # Matched name message, visble = False
            window['-NAME_BLANK-'].update(visible=False)        # Blank name message, visible = False
            file_append_avail_parklot(parklot_name)             # Append the new name to available parking lots
    # -----------------------------------------------------------------------------------------------------------------

    # Work with select reference image
    # -------------------------------------------------------------------------------------------------------
    if event == '-DEFINE_01-' or event == '-REDEFINE-' or event == '-REDEFINE_DEF-' or event == '-BACK2DEF-':
    # If event wish to come/comeback to select reference image
        window[f'lay_{layout}'].update(visible=False)
        layout = 4
        window[f'lay_{layout}'].update(visible=True)
        # Get the parking lot name
        if event == '-DEFINE_01-' or event == '-REDEFINE_DEF-':
            ### Debug: Print parking lot name string
            # print(parklot_name)
            print("")
        else:
            strx = ""
            for v in values['-PARKLOT-']:
                strx = v                                # Extract the string from the list parentheses
            parklot_name = strx
            print(parklot_name)

    # If event is load image, after selecting an available image
    if event == "Load image":
        filename = values['-REFIMG-']   # Update image value
        # print(filename)
        # print(filename)
        if os.path.exists(filename):    # Open image & show thumbnail before proceed to process
            image = Image.open(values['-REFIMG-'])
            image.thumbnail((500, 500))
            bio = io.BytesIO()
            image.save(bio, format="PNG")
            window["-IMAGE-"].update(data=bio.getvalue())   # Show image
            window['-DEFINE_02-'].update(visible=True)      # Next button, visible = True
    # -----------------------------------------------------------------------------------------------------

    # Work with define landmark and parking slot
    # -----------------------------------------------------------------------------------------------------
    if event == '-DEFINE_02-':
        print("Accessing landmark & parking slot mode")
        window[f'lay_{layout}'].update(visible=False)
        layout = 5
        window[f'lay_{layout}'].update(visible=True)
        grid_drawn = gui_draw(filename)
        data = get_img_data(grid_drawn, maxsize, first=True)
        graph.draw_image(data=data, location=(0, 0))

    if event == '-GRAPH-':
        x, y = values['-GRAPH-']
        if not dragging:
            start_point = (x, y)
            dragging = True
        else:
            end_point = (x, y)
        if prior_rect:
            graph.delete_figure(prior_rect)
        if None not in (start_point, end_point):
            prior_rect = graph.draw_rectangle(start_point, end_point, line_color='blue')
    elif event.endswith('+UP'):
        info = window['-INFO-']
        info.update(value=f"Selected rectangle from {start_point} to {end_point}")
        dragging = False

    if event == '-SAVE_LM-':
        if values['-LM_NUM-'] == "":
            index = 0
            ref_pos_x[index] = int((start_point[0] + end_point[0]) / 2 / scale)
            ref_pos_y[index] = int((start_point[1] + end_point[1]) / 2 / scale)
        else:
            index = int(values['-LM_NUM-'])
            ref_pos_x[index] = int((start_point[0] + end_point[0]) / 2 / scale)
            ref_pos_y[index] = int((start_point[1] + end_point[1]) / 2 / scale)
            window['-LM_1-'].update(value=f"Landmark 01: {ref_pos_x[1]}, {ref_pos_y[1]}")
            window['-LM_2-'].update(value=f"Landmark 02: {ref_pos_x[2]}, {ref_pos_y[2]}")
            window['-LM_3-'].update(value=f"Landmark 03: {ref_pos_x[3]}, {ref_pos_y[3]}")
            window['-LM_4-'].update(value=f"Landmark 04: {ref_pos_x[4]}, {ref_pos_y[4]}")
            # print(ref_pos_x)
            # print(ref_pos_y)

    if event == '-SAVE_SLOT-':
        if values['-SLOT_NUM-'] == "":
            index = 0
            slot_pos_x[index] = int((start_point[0] + end_point[0]) / 2 / scale)
            slot_pos_y[index] = int((start_point[1] + end_point[1]) / 2 / scale)
        else:
            index = int(values['-SLOT_NUM-'])
            slot_pos_x[index] = int((start_point[0] + end_point[0]) / 2 / scale)
            slot_pos_y[index] = int((start_point[1] + end_point[1]) / 2 / scale)
            # print(slot_pos_x)
            # print(slot_pos_y)

    # Save changes to slot file
    if event == '-REDEF_SLOT-':
        file_slot_write(slot_pos_x, slot_pos_y, number_of_slot)
    # ------------------------------------------------------------------------------------------------------

    # -----------------------------------------------
    # Working with run automatically
    if event == '-RUNAUTO-':
        window[f'lay_{layout}'].update(visible=False)
        layout = 3
        window[f'lay_{layout}'].update(visible=True)
    # -----------------------------------------------

    # ---------------------------------------------------------------------------------------------
    # Working with select calibration mode
    if event == '-RUN-' or event == '-RUN_DEF-' or event == '-FIN-':
        if event == '-FIN-':
            file_landmark_write(ref_pos_x, ref_pos_y)
        print("Accessing running mode, return the results")
        window[f'lay_{layout}'].update(visible=False)
        layout = 6
        window[f'lay_{layout}'].update(visible=True)

    if event == '-TRANS-' or event == '-ROL-':
        window[f'lay_{layout}'].update(visible=False)
        layout = 7
        window[f'lay_{layout}'].update(visible=True)
        write_address = "D:\\IC DESIGN LAB\\[LAB] PRJ.Parking Lot\\IMAGE_CALIBRATION_V2" \
                        "\\data_process\\calib_image"
        remove_folder_content(write_address)
        f_runtime = open("D:\\IC DESIGN LAB\\[LAB] PRJ.Parking Lot\\IMAGE_CALIBRATION_V2\\"
                         "\\data_process\\runTime.txt", 'r+')
        landmark_flag, ref_x, ref_y = mytrans.info_open()
        checkdef = f_runtime.read()
        progress_bar = window.FindElement('-PROG_BAR-')
        if checkdef == '0' or landmark_flag == 1:
            window['-NOT_DEF-'].update(visible=True)
            window['-WAIT-'].update(visible=False)
        else:
            window['-NOT_DEF-'].update(visible=False)
            window['-WAIT-'].update(visible=True)
            os.chdir("D:\\IC DESIGN LAB\\[LAB] PRJ.Parking Lot\\IMAGE_CALIBRATION_V2\\data_process\\data")
            number_of_file = 0
            run_var = 0
            for base, dirs, files in os.walk(os.getcwd()):
                for Files in files:
                    number_of_file = number_of_file + 1
            if event == '-TRANS-':
                trans_rot_mode = 1
                for filename in os.listdir(os.getcwd()):
                    image = cv2.imread(filename)
                    window['-PROCESSING_FILE-'].update(value=f"{filename} processing")
                    window['-PROCESSING_FILE-'].update(visible=True)
                    cur1, cur2, cur3, cur4 = mytrans.landmark_recog(filename)
                    print(cur1, cur2, cur3, cur4)
                    print("")
                    mytrans.main(trans_rot_mode, filename, cur1, cur2, cur3, cur4)
                    run_var = run_var + 1
                    progress_bar.UpdateBar(run_var, number_of_file)
                window['-FINISHED-'].update(visible=True)
                window['-SHOW_RES-'].update(visible=True)
            elif event == '-ROL-':
                trans_rot_mode = 2
                for filename in os.listdir(os.getcwd()):
                    image = cv2.imread(filename)
                    window['-PROCESSING_FILE-'].update(value=f"{filename} processing")
                    window['-PROCESSING_FILE-'].update(visible=True)
                    cur1, cur2, cur3, cur4 = mytrans.landmark_recog(filename)
                    mytrans.main(trans_rot_mode, filename, cur1, cur2, cur3, cur4)
                    run_var = run_var + 1
                    progress_bar.UpdateBar(run_var, number_of_file)
                window['-FINISHED-'].update(visible=True)
                window['-SHOW_RES-'].update(visible=True)
    # ---------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------
    # Working with showing results
    if event == '-SHOW_RES-':
        window[f'lay_{layout}'].update(visible=False)
        layout = 8
        window[f'lay_{layout}'].update(visible=True)

        # Get a list of file names available
        folder_original = "D:\\IC DESIGN LAB\\[LAB] PRJ.Parking Lot\\IMAGE_CALIBRATION_V2" \
                          "\\data_process\\data"
        folder_calibrated = "D:\\IC DESIGN LAB\\[LAB] PRJ.Parking Lot\\IMAGE_CALIBRATION_V2" \
                            "\\data_process\\calib_image"
        flist_o = os.listdir(folder_original)
        flist_c = os.listdir(folder_calibrated)
        fnames_o = [f for f in flist_o if os.path.isfile(
            os.path.join(folder_original, f))]
        numfiles_o = len(fnames_o)
        fnames_c = [g for g in flist_c if os.path.isfile(
            os.path.join(folder_calibrated, g))]
        numfiles_c = len(fnames_c)
        del flist_o, flist_c
        # End of getting list

        # Grab the first image
        filename_og = os.path.join(folder_original, fnames_o[result_image_index])
        filename_cab = os.path.join(folder_calibrated, fnames_c[result_image_index])
        # print(os.path.isfile(filename_og), os.path.isfile(filename_cab))

        # Show the first images:
        data_og = get_img_data(filename_og, (640, 360), first=True)
        before_calib.draw_image(data=data_og, location=(0, 0))
        data_cab = get_img_data(filename_cab, (640, 360), first=True)
        after_calib.draw_image(data=data_cab, location=(0, 0))

    # Image scrolling
    if event in ('-PREV_IMG-', '-NEXT_IMG-'):
        if event == '-PREV_IMG-':
            result_image_index = result_image_index - 1
            if result_image_index < 0:
                result_image_index = numfiles_o + result_image_index
        elif event == '-NEXT_IMG-':
            result_image_index = result_image_index + 1
            if result_image_index >= numfiles_o:
                result_image_index = result_image_index - numfiles_o

        # Grab the image
        filename_og = os.path.join(folder_original, fnames_o[result_image_index])
        filename_cab = os.path.join(folder_calibrated, fnames_c[result_image_index])
        # print(os.path.isfile(filename_og), os.path.isfile(filename_cab))

        # Show the images:
        data_og = get_img_data(filename_og, (640, 360), first=True)
        before_calib.draw_image(data=data_og, location=(0, 0))
        data_cab = get_img_data(filename_cab, (640, 360), first=True)
        after_calib.draw_image(data=data_cab, location=(0, 0))
    # ---------------------------------------------------------------------------------------------

    # Test layout change & direct accessing to available layouts
    # ----------------------------------------------------------
    if event == 'Cycle layout':
        window[f'lay_{layout}'].update(visible=False)
        layout = layout + 1 if layout < 8 else 1
        window[f'lay_{layout}'].update(visible=True)
    elif event in '12345678':
        window[f'lay_{layout}'].update(visible=False)
        layout = int(event)
        window[f'lay_{layout}'].update(visible=True)
    # -----------------------------------------------------------
window.close()