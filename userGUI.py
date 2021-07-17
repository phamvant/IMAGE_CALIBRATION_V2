# This is the file containing test layout for ImageCalibration
# The layout is in development
### Import libraries/packages
# ---------------------------------------------------------------------------------------------------------------------
import os
import io
# Import required processing libraries/packages
import PySimpleGUI as sg
import cv2
from PIL import Image, ImageTk

# Import image calibration algorithm file
import myTranslation as mytrans
# Import folder & file manipulation functions
import folderFileManip as ff_manip
# Import GUI additional functions
import infoGUI as inf_gui
# ---------------------------------------------------------------------------------------------------------------------

# Initiate values
# ---------------------------------------------------------------------------------------------------------------------
# Get top working folder directory
parent_path = os.getcwd()
print(parent_path)
# print(parent_path)

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
wid, hght = inf_gui.get_scr_size(scale)
maxsize = (wid, hght)

# Define image files, which should be used in later definitions
file_types = [("JPEG (*.jpg)", ".jpg"),
              ("All files (*.*)", "*.*")]

# Define a list, emulating reading different parking lot
list_of_parking_lot, avail_flag = ff_manip.file_open_avail_parklot(parent_path)
size_of_list_parklot = len(list_of_parking_lot)

### Define layouts
# ---------------------------------------------------------------------------------------------------------------------
# Layout 1/layout_open: Opening layout of the program
layout_open = [[sg.Text('IMAGE CALIBRATION', font='Arial')],
               [sg.Button('Define new parking lot', key='-DEFNEW-')],
               [sg.Button('Run automatically', key='-RUNAUTO-')]]

# Layout 2/layout_defnew_1: Define new parking lot name layout
layout_defnew_1 = [[sg.Text('DEFINE NEW PARKING LOT')],
                   [sg.Text('Please input new parking lot name')],
                   [sg.InputText(key='-NEW_PARKLOT_NAME-')],
                   [sg.Button('Enter new name', key='-ENTER_NAME-')],
                   [sg.Text("This parking lot has been defined, select Redefine or Run auto instead",
                            key='-RET_MSG_DEFNEW1-', visible=False)],
                   [sg.Text("Parking lot name is blank, please try again", key='-NAME_BLANK-', visible=False)],
                   [sg.Button('Back', key='-BACK_2-')],
                   [sg.Button('Next', key='-DEFINE_01-', visible=False),
                    sg.Button('Redefine', key='-REDEFINE_DEF-', visible=False),
                    sg.Button('Run auto', key='-RUN_DEF-', visible=False)]
                   ]

# Layout 3/layout_runauto_1: Select defined parking lot layout
layout_runauto_1 = [[sg.Text("RUN CALIBRATING AUTOMATICALLY")],
                    [sg.Text("Select one of these defined parking lot")],
                    [sg.Listbox(values=list_of_parking_lot, select_mode='single', key='-PARKLOT-', size=(30, 6))],
                    [sg.Button('Back', key='-BACK_3-'),
                     sg.Button('Redefine', key='-REDEFINE-'), sg.Button('Run auto', key='-RUN-')]]

# Layout 4/layout_defnew_2: Select reference image layout
layout_defnew_2 = [[sg.Text('DEFINE PARKING LOT')],
                   [sg.Text('Select reference image')],
                   [sg.Text('Choose a file: '), sg.Input(size=(30, 1), key='-REFIMG-'),
                    sg.FileBrowse(file_types=file_types)],
                   [sg.Button("Load image")],
                   [sg.Image(key="-IMAGE-")],
                   [sg.Button('Back', key='-BACK_4-'), sg.Button('Next', key='-DEFINE_02-', visible=False)]]

# Layout 5/layout_defnew3: Define landmarks & parking slots layout
layout_1 = [[sg.Graph(canvas_size=(wid, hght),              # First column
                      graph_bottom_left=(0, 720),
                      graph_top_right=(1280, 0),
                      enable_events=True,
                      drag_submits=True,
                      key='-GRAPH-')],
            [sg.InputText(size=(10, 1), key='-LM_NUM-'),
             sg.Button("Save as Landmark", key='-SAVE_LM-'),
             sg.Button("Save LM file", key='-REDEF_LM-'),
             sg.InputText(size=(10, 1), key='-SLOT_NUM-'),
             sg.Button("Save as ParkSlot", key='-SAVE_SLOT-'),
             sg.Button("Save PSlot file", key='-REDEF_SLOT-')],
            [sg.Button('Back', key='-BACK_5-'), sg.Button('Finish', key='-FIN-')]]

layout_2 = [[sg.Text(key='-INFO-', size=(50, 1))],          # Second column
            [sg.Text(key='-LM_1-', size=(30, 1))],
            [sg.Text(key='-LM_2-', size=(30, 1))],
            [sg.Text(key='-LM_3-', size=(30, 1))],
            [sg.Text(key='-LM_4-', size=(30, 1))],
            [sg.Text(key='-SLOT_1-', size=(15, 1))],
            [sg.Text(key='-SLOT_2-', size=(15, 1))],
            [sg.Text(key='-SLOT_3-', size=(15, 1))],
            [sg.Text(key='-SLOT_4-', size=(15, 1))],
            [sg.Text(key='-SLOT_5-', size=(15, 1))],
            [sg.Text(key='-SLOT_6-', size=(15, 1))],
            [sg.Text(key='-SLOT_7-', size=(15, 1))],
            [sg.Text(key='-SLOT_8-', size=(15, 1))],
            [sg.Text(key='-SLOT_9-', size=(15, 1))],
            [sg.Text(key='-SLOT_10-', size=(15, 1))],
            [sg.Text(key='-SLOT_11-', size=(15, 1))],
            [sg.Text(key='-SLOT_12-', size=(15, 1))],
            [sg.Text(key='-SLOT_13-', size=(15, 1))],
            [sg.Text(key='-SLOT_14-', size=(15, 1))],
            [sg.Text(key='-SLOT_15-', size=(15, 1))],
            [sg.Text(key='-SLOT_16-', size=(15, 1))],
            [sg.Text(key='-SLOT_17-', size=(15, 1))],
            [sg.Text(key='-SLOT_18-', size=(15, 1))],
            [sg.Text(key='-SLOT_19-', size=(15, 1))],
            [sg.Text(key='-SLOT_20-', size=(15, 1))]
            ]


layout_defnew_3 = [[sg.Text('DEFINE PARKING LOT')],         # Master layout of layout 5, combine 1st and 2nd column
                   [sg.Text('Define landmarks & parking slots')],
                   [sg.Column(layout_1), sg.Column(layout_2)]]

# Layout 6/layout_select_calib_mode: Select calibration mode
layout_select_calib_mode = [[sg.Text("SELECT DATA FOLDER & CALIBRATION TYPE")],
                            [sg.Text("Input data folder"), sg.Input(size=(30, 1), key='-DATA_FOL-'),
                             sg.FolderBrowse()],
                            [sg.Button('Translation', key='-TRANS-'), sg.Button('Rotation', key='-ROL-')],
                            [sg.Button('Back', key='-BACK_6-')]]

# Layout 7/layout_wait_error: Wait screen/Error screen layout
layout_wait_error = [[sg.Text("WAIT SCREEN")],
                     [sg.Text("Parking lot has not been defined, please define before run", key='-NOT_DEF-',
                              visible=False)],
                     [sg.Text("Parking lot processing, please wait", key='-WAIT-',
                              visible=False)],
                     [sg.Text(key="-PROCESSING_FILE-", size=(60, 1), visible=False)],
                     [sg.ProgressBar(1, orientation='h', size=(80, 20), key='-PROG_BAR-')],
                     [sg.Text("Program finished monitoring", key='-FINISHED-', visible=False)],
                     [sg.Button("Show result", key='-SHOW_RES-', visible=False)]]

# Layout 8/layout_results: Result layout - Image viewer
result_col_1 = [[sg.Text("Before calibration")],        # First column
                [sg.Graph(canvas_size=(640, 360),
                          graph_bottom_left=(0, 360),
                          graph_top_right=(640, 0),
                          background_color='white',
                          enable_events=True,
                          key='-BEFORE_CALIB-')]]

result_col_2 = [[sg.Text("After calibration")],         # Second column
                [sg.Graph(canvas_size=(640, 360),
                          graph_bottom_left=(0, 360),
                          graph_top_right=(640, 0),
                          background_color='white',
                          enable_events=True,
                          key='-AFTER_CALIB-')]]

layout_result = [[sg.Text("RESULTS")],                  # Master layout of layout 8, combine 1st and 2nd column
                 [sg.Text("Before and After Calibration")],
                 [sg.Text("Image", key='-SHOWN_IMG-', size=(30, 1))],
                 [sg.Column(result_col_1), sg.Column(result_col_2)],
                 [sg.Button("Prev Image", key='-PREV_IMG-'), sg.Button("Next Image", key='-NEXT_IMG-')],
                 [sg.Button("Back to define", key='-BACK2DEF-'), sg.Button("Close the program", key='-CLOSE_PROG-')]]

# Master layout of the program: Combining above layouts & navigate buttons
layout = [[sg.Column(layout_open, key='lay_1', element_justification='center'),
           sg.Column(layout_defnew_1, visible=False, key='lay_2'),
           sg.Column(layout_runauto_1, visible=False, key='lay_3'),
           sg.Column(layout_defnew_2, visible=False, key='lay_4'),
           sg.Column(layout_defnew_3, visible=False, key='lay_5'),
           sg.Column(layout_select_calib_mode, visible=False, key='lay_6'),
           sg.Column(layout_wait_error, visible=False, key='lay_7'),
           sg.Column(layout_result, visible=False, key='lay_8')]]
# [ sg.Button('Cycle layout'), sg.Button('1'), sg.Button('2'), sg.Button('3'),
# sg.Button('4'), sg.Button('5'), sg.Button('6'), sg.Button('7'), sg.Button('8'),
# sg.Button('Exit')]]
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
        layout = 2                                      # Update define new name layout
        window[f'lay_{layout}'].update(visible=True)

    if event == '-ENTER_NAME-':                         # If enter new name button is pressed
        match = 0
        parklot_name = values['-NEW_PARKLOT_NAME-']
        ### Debug: Determine input parking lot name
        # print(parklot_name)
        if parklot_name == "":                           # Check if new name is blank. Blank name cannot be used
            window['-NAME_BLANK-'].update(visible=True)  # Blank name message, visible = True
            window['-DEFINE_01-'].update(visible=False)  # Next button, visible = False
            continue                                     # Continue receiving new name

        for i in range(0, size_of_list_parklot):         # Check if name is used, means parking lot is defined
            if parklot_name == list_of_parking_lot[i]:
                match = 1                                # Found matching result!
                temp = list_of_parking_lot[i]
        if match == 1:         # Display Redefine, RunAuto option. Not append this new name since it's already available
            window['-RET_MSG_DEFNEW1-'].update(visible=True)    # Matched name message, visible = True
            window['-REDEFINE_DEF-'].update(visible=True)       # Redefine button, visible = True
            window['-RUN_DEF-'].update(visible=True)            # RunAuto button, visible = True
            window['-DEFINE_01-'].update(visible=False)         # Next button, visible = False
            window['-NAME_BLANK-'].update(visible=False)        # Blank name message, visible = False
        else:                                             # No matching name found. This name need to be added
            window['-DEFINE_01-'].update(visible=True)          # Next button, visible = True
            window['-REDEFINE_DEF-'].update(visible=False)      # Redefine button, visible = False
            window['-RUN_DEF-'].update(visible=False)           # RunAuto button , visible = False
            window['-RET_MSG_DEFNEW1-'].update(visible=False)   # Matched name message, visble = False
            window['-NAME_BLANK-'].update(visible=False)        # Blank name message, visible = False
            ff_manip.file_append_avail_parklot(parent_path, parklot_name) # Append the new name to available parking lots

    # -----------------------------------------------------------------------------------------------------------------

    # Work with select reference image
    # -------------------------------------------------------------------------------------------------------
    if event == '-DEFINE_01-' or event == '-REDEFINE-' or event == '-REDEFINE_DEF-' or event == '-BACK2DEF-' \
            or event == '-RUN-':
        if event == '-RUN-' or event == '-REDEFINE-':
            strx = ""
            for v in values['-PARKLOT-']:
                strx = v  # Extract the string from the list parentheses
            parklot_name = strx
            ### Debug: Determine input parking lot name
            # print(parklot_name)
            if event == '-REDEFINE-':
                window[f'lay_{layout}'].update(visible=False)
                layout = 4  # Update select image layout
                window[f'lay_{layout}'].update(visible=True)
                ff_manip.folder_manip(parent_path, parklot_name)
                ff_manip.file_manip(parent_path, parklot_name)
                os.chdir(parent_path + "\\data_process\\{}".format(parklot_name))
        else:
        # If event wish to come/comeback to select reference image
            window[f'lay_{layout}'].update(visible=False)
            layout = 4                                  # Update select image layout
            window[f'lay_{layout}'].update(visible=True)
            # Get the parking lot name
            if event == '-DEFINE_01-' or event == '-REDEFINE_DEF-':
                ### Debug: Print parking lot name string
                parklot_name = values['-NEW_PARKLOT_NAME-']
                ### Debug: Determine input parking lot name
                # print(parklot_name)
            # Create required folders:
            os.chdir(parent_path + "\\data_process")
            ff_manip.folder_manip(parent_path, parklot_name)
            ff_manip.file_manip(parent_path, parklot_name)
            os.chdir(parent_path + "\\data_process\\{}".format(parklot_name))

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
    # --------------------------------------------------------------------------------------
    if event == '-DEFINE_02-':
    # If event is input image for parking lot defining
        ### Debug:
        # print("Accessing landmark & parking slot mode")
        window[f'lay_{layout}'].update(visible=False)
        layout = 5                                              # Update landmark & slot define layout
        window[f'lay_{layout}'].update(visible=True)
        grid_drawn = inf_gui.gui_draw(parent_path, filename)                         # Draw grid on selected image
        data = inf_gui.get_img_data(grid_drawn, maxsize, first=True)    # Convert reference image data to base64
        graph.draw_image(data=data, location=(0, 0))            # Draw image to grid, layout 5

    # Define actions on graph
    if event == '-GRAPH-':
        x, y = values['-GRAPH-']                                # Get coordinate from mouse on graph
        if not dragging:                                        # If drag = False
            start_point = (x, y)                                # Get starting point
            dragging = True
        else:
            end_point = (x, y)                                  # Get ending point
        if prior_rect:
            graph.delete_figure(prior_rect)                     # Delete previous selected zone
        if None not in (start_point, end_point):
            prior_rect = graph.draw_rectangle(start_point, end_point, line_color='blue')
    elif event.endswith('+UP'):                                 # If mouse is released
        info = window['-INFO-']                                 # Update information on image (rectangle)
        info.update(value=f"Selected rectangle from {start_point} to {end_point}")
        dragging = False                                        # Set drag to false, ready for an another action

    # Define actions on saving information. Calculate using grabbed coordinates, revert to original scale
    if event == '-SAVE_LM-':
        if values['-LM_NUM-'] == "":                # Save landmark information, but landmark number is not defined
            index = 0                               # Save in the first slot, as a dummy value
            ref_pos_x[index] = int((start_point[0] + end_point[0]) / 2 / scale)
            ref_pos_y[index] = int((start_point[1] + end_point[1]) / 2 / scale)
        else:
            index = int(values['-LM_NUM-'])         # Save landmark information, save to the -LM_NUM- position
            ref_pos_x[index] = int((start_point[0] + end_point[0]) / 2 / scale)
            ref_pos_y[index] = int((start_point[1] + end_point[1]) / 2 / scale)
            # Show saved data to the screen
            window['-LM_1-'].update(value=f"Landmark 01: {ref_pos_x[1]}, {ref_pos_y[1]}")
            window['-LM_2-'].update(value=f"Landmark 02: {ref_pos_x[2]}, {ref_pos_y[2]}")
            window['-LM_3-'].update(value=f"Landmark 03: {ref_pos_x[3]}, {ref_pos_y[3]}")
            window['-LM_4-'].update(value=f"Landmark 04: {ref_pos_x[4]}, {ref_pos_y[4]}")
            # print(ref_pos_x)
            # print(ref_pos_y)

    # Define actions on saving slots. Calculate using grabbed coordinates, revert to original scale
    if event == '-SAVE_SLOT-':
        if values['-SLOT_NUM-'] == "":              # Save slot information, but slot number is not defined
            index = 0                               # Save in the first slot, as a dummy value
            slot_pos_x[index] = int((start_point[0] + end_point[0]) / 2 / scale)
            slot_pos_y[index] = int((start_point[1] + end_point[1]) / 2 / scale)
        else:
            index = int(values['-SLOT_NUM-'])       # Save slot information, save to the -SLOT_NUM- position
            slot_pos_x[index] = int((start_point[0] + end_point[0]) / 2 / scale)
            slot_pos_y[index] = int((start_point[1] + end_point[1]) / 2 / scale)
            window['-SLOT_1-'].update(value=f"Slot 01: {slot_pos_x[1]}, {slot_pos_y[1]}")
            window['-SLOT_2-'].update(value=f"Slot 02: {slot_pos_x[2]}, {slot_pos_y[2]}")
            window['-SLOT_3-'].update(value=f"Slot 03: {slot_pos_x[3]}, {slot_pos_y[3]}")
            window['-SLOT_4-'].update(value=f"Slot 04: {slot_pos_x[4]}, {slot_pos_y[4]}")
            window['-SLOT_5-'].update(value=f"Slot 05: {slot_pos_x[5]}, {slot_pos_y[5]}")
            window['-SLOT_6-'].update(value=f"Slot 06: {slot_pos_x[6]}, {slot_pos_y[6]}")
            window['-SLOT_7-'].update(value=f"Slot 07: {slot_pos_x[7]}, {slot_pos_y[7]}")
            window['-SLOT_8-'].update(value=f"Slot 08: {slot_pos_x[8]}, {slot_pos_y[8]}")
            window['-SLOT_9-'].update(value=f"Slot 09: {slot_pos_x[9]}, {slot_pos_y[9]}")
            window['-SLOT_10-'].update(value=f"Slot 10: {slot_pos_x[10]}, {slot_pos_y[10]}")
            window['-SLOT_11-'].update(value=f"Slot 11: {slot_pos_x[11]}, {slot_pos_y[11]}")
            window['-SLOT_12-'].update(value=f"Slot 12: {slot_pos_x[12]}, {slot_pos_y[12]}")
            window['-SLOT_13-'].update(value=f"Slot 13: {slot_pos_x[13]}, {slot_pos_y[13]}")
            window['-SLOT_14-'].update(value=f"Slot 14: {slot_pos_x[14]}, {slot_pos_y[14]}")
            window['-SLOT_15-'].update(value=f"Slot 15: {slot_pos_x[15]}, {slot_pos_y[15]}")
            window['-SLOT_16-'].update(value=f"Slot 16: {slot_pos_x[16]}, {slot_pos_y[16]}")
            window['-SLOT_17-'].update(value=f"Slot 17: {slot_pos_x[17]}, {slot_pos_y[17]}")
            window['-SLOT_18-'].update(value=f"Slot 18: {slot_pos_x[18]}, {slot_pos_y[18]}")
            window['-SLOT_19-'].update(value=f"Slot 19: {slot_pos_x[19]}, {slot_pos_y[19]}")
            window['-SLOT_20-'].update(value=f"Slot 20: {slot_pos_x[20]}, {slot_pos_y[20]}")
            # print("{} {} {}\n".format(index, slot_pos_x[index], slot_pos_y[index]))

    # Save changes to landmark file, if redefine landmark file is pressed
    if event == '-REDEF_LM-':
        ff_manip.file_landmark_write(parent_path, ref_pos_x, ref_pos_y, parklot_name)
        
    # Save changes to slot file, if redefine slot button is pressed
    if event == '-REDEF_SLOT-':
        ff_manip.file_slot_write(parent_path, parklot_name, slot_pos_x, slot_pos_y, number_of_slot)
    # ---------------------------------------------------------------------------------------

    # Work with run automatically
    # -----------------------------------------------
    if event == '-RUNAUTO-':
        window[f'lay_{layout}'].update(visible=False)
        layout = 3                                  # Update select defined parking lot layout
        window[f'lay_{layout}'].update(visible=True)
    # -----------------------------------------------

    # Work with select calibration mode
    # ---------------------------------------------------------------------------------------------
    if event == '-RUN-' or event == '-RUN_DEF-' or event == '-FIN-':
        # print("Accessing running mode, return the results")
        window[f'lay_{layout}'].update(visible=False)
        layout = 6                                  # Update select calibration mode layout
        window[f'lay_{layout}'].update(visible=True)

        # Check if all required folders are created or not. If not, create new ones
        ff_manip.folder_manip(parent_path, parklot_name)
        ff_manip.file_manip(parent_path, parklot_name)

        # Update the destination folders after working with folder name
        folder_calibrated = parent_path + "\\data_process\\{}\\calib_image".format(parklot_name)

        # Move into the required folder
        cur_cwd = parent_path + "\\data_process\\{}".format(parklot_name)
        os.chdir(cur_cwd)
        # print(os.getcwd())

    # Switch between 2 types of calibration: Translation & Rotation
    if event == '-TRANS-' or event == '-ROL-':
        window[f'lay_{layout}'].update(visible=False)
        layout = 7                                  # Update waiting layout
        window[f'lay_{layout}'].update(visible=True)
        # Avoid using static addresses
        # Remove all files in the previous run. This function should be removed in future updates or refurbished for a
        # better experience
        folder_original = values['-DATA_FOL-']

        write_address_full = cur_cwd + "\\calib_image"
        write_address_small = cur_cwd + "\\calib_image_cut"
        ff_manip.remove_folder_content(write_address_full)
        ff_manip.remove_folder_content(write_address_small)
        # Open runtime file, check if the parking lot is actually defined
        f_runtime = open(cur_cwd + "\\runTime.txt", 'r+')
        # Actual image calibrating
        landmark_flag, ref_x, ref_y = mytrans.info_open(parklot_name)
        checkdef = f_runtime.read()
        progress_bar = window.FindElement('-PROG_BAR-')         # Define loading bar
        if checkdef == '0' or landmark_flag == 1:               # The parking lot is not defined. Redefine required!
            window['-NOT_DEF-'].update(visible=True)            # Not defined message, visible = True
            window['-WAIT-'].update(visible=False)              # Wait for processing message, visible = False
        else:
            window['-NOT_DEF-'].update(visible=False)           # Not defined message, visible = False
            window['-WAIT-'].update(visible=True)               # Wait for processing message, visible = True
            # Change to data need calibration folder
            os.chdir(folder_original)
            number_of_file = 0                                  # Initiate the number of data files need calibration
            run_var = 0                                         # Running variable for loading bar
            for base, dirs, files in os.walk(os.getcwd()):
                for Files in files:
                    number_of_file = number_of_file + 1         # Get the number of data files need calibration
            if event == '-TRANS-':
                trans_rot_mode = 1                              # Use Translation only
                for filename in os.listdir(os.getcwd()):
                    image = cv2.imread(filename)
                    # Update which file is being processed
                    window['-PROCESSING_FILE-'].update(value=f"{filename} processing")
                    window['-PROCESSING_FILE-'].update(visible=True)
                    # Image calibration
                    cur1, cur2, cur3, cur4 = mytrans.landmark_recog(filename)
                    ### Debug: Print recognized landmarks values
                    # print(cur1, cur2, cur3, cur4)
                    # print("")
                    mytrans.main(parklot_name, trans_rot_mode, filename, cur1, cur2, cur3, cur4)
                    run_var = run_var + 1
                    progress_bar.UpdateBar(run_var, number_of_file)     # Update loading bar
                window['-FINISHED-'].update(visible=True)               # Finished message, visible = True
                window['-SHOW_RES-'].update(visible=True)               # Show result button, visible = True
            elif event == '-ROL-':
                trans_rot_mode = 2                              # Use Rotation only
                for filename in os.listdir(os.getcwd()):
                    image = cv2.imread(filename)
                    window['-PROCESSING_FILE-'].update(value=f"{filename} processing")
                    window['-PROCESSING_FILE-'].update(visible=True)
                    cur1, cur2, cur3, cur4 = mytrans.landmark_recog(filename)
                    mytrans.main(parklot_name, trans_rot_mode, filename, cur1, cur2, cur3, cur4)
                    run_var = run_var + 1
                    progress_bar.UpdateBar(run_var, number_of_file)     # Update loading bar
                window['-FINISHED-'].update(visible=True)               # Finished message, visible = True
                window['-SHOW_RES-'].update(visible=True)               # Show result button, visible = True
    # ---------------------------------------------------------------------------------------------

    # Work with showing results
    # ---------------------------------------------------------------------------------------------
    if event == '-SHOW_RES-':
        result_image_index = 0                          # Reset image index to 0
        window[f'lay_{layout}'].update(visible=False)
        layout = 8                                      # Update image viewer layout
        window[f'lay_{layout}'].update(visible=True)

        # Get a list of file names available
        # Define image viewer function
        flist_o = os.listdir(folder_original)           # Get list of original images
        flist_c = os.listdir(folder_calibrated)         # Get list of calibrated images
        # Get list of names, original images
        fnames_o = [f for f in flist_o if os.path.isfile(os.path.join(folder_original, f))]
        numfiles_o = len(fnames_o)                      # Get number of original images
        # Get list of names, calibration images
        fnames_c = [g for g in flist_c if os.path.isfile(os.path.join(folder_calibrated, g))]
        numfiles_c = len(fnames_c)                      # Get number of calibrated images
        del flist_o, flist_c                            # Remove lists of names, since it's unused
        # End of getting list

        # Grab the first image
        filename_og = os.path.join(folder_original, fnames_o[result_image_index])
        filename_cab = os.path.join(folder_calibrated, fnames_c[result_image_index])
        # print(os.path.isfile(filename_og), os.path.isfile(filename_cab))

        # Print the image name:
        window['-SHOWN_IMG-'].update(value=f"{fnames_o[result_image_index]}")
        # Show the first images:
        data_og = inf_gui.get_img_data(filename_og, (640, 360), first=True)
        before_calib.draw_image(data=data_og, location=(0, 0))          # Draw image to left graph, image viewer
        data_cab = inf_gui.get_img_data(filename_cab, (640, 360), first=True)
        after_calib.draw_image(data=data_cab, location=(0, 0))          # Draw image to right graph, image viewer

    # Image scrolling
    if event in ('-PREV_IMG-', '-NEXT_IMG-'):
        if event == '-PREV_IMG-':                                       # Previous function in image viewer
            result_image_index = result_image_index - 1
            if result_image_index < 0:
                result_image_index = numfiles_o + result_image_index
            window['-SHOWN_IMG-'].update(value=f"{fnames_o[result_image_index]}")
        elif event == '-NEXT_IMG-':                                     # Next function in image viewer
            result_image_index = result_image_index + 1
            if result_image_index >= numfiles_o:
                result_image_index = result_image_index - numfiles_o
            window['-SHOWN_IMG-'].update(value=f"{fnames_o[result_image_index]}")

        # Grab the image
        filename_og = os.path.join(folder_original, fnames_o[result_image_index])
        filename_cab = os.path.join(folder_calibrated, fnames_c[result_image_index])
        # print(os.path.isfile(filename_og), os.path.isfile(filename_cab))

        # Show the images:
        data_og = inf_gui.get_img_data(filename_og, (640, 360), first=True)
        before_calib.draw_image(data=data_og, location=(0, 0))          # Draw image to left graph, image viewer
        data_cab = inf_gui.get_img_data(filename_cab, (640, 360), first=True)
        after_calib.draw_image(data=data_cab, location=(0, 0))          # Draw image to right graph, image viewer
    # ---------------------------------------------------------------------------------------------
    """
    # Test layout change & access directly to available layouts
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
    """
window.close()
