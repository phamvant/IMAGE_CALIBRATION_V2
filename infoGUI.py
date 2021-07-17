# Import required libraries
import os
import ctypes
import cv2
import io

from PIL import Image, ImageTk

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
def gui_draw(parent_path, file_name):
    # Draw a guidance grid onto the image
    img = cv2.imread(file_name)
    # Avoid using static addresses
    # Use this instead, but be cautious :
    # grid_img = cv2.imread(os.getcwd() + "\\data_process\\ref_image\\imGrid.png")
    # Make sure the working files are in the right positions before use
    grid_img = cv2.imread(parent_path + "\\data_process\\grid_img\\imGrid.png")
    ### Debug: show Grid image
    # cv2.imshow("Image", grid_img)
    # cv2.waitKey()

    rows, cols, channel = grid_img.shape
    roi = img[0:rows, 0:cols]

    # Add grid to the selected reference image
    img2gray = cv2.cvtColor(grid_img, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 200, 255, cv2.THRESH_BINARY_INV)
    mask_inv = cv2.bitwise_not(mask)
    img = cv2.bitwise_and(roi, roi, mask=mask_inv)
    grid_img_fg = cv2.bitwise_and(grid_img, grid_img, mask=mask)
    img = cv2.add(img, grid_img_fg)

    # Get file name, write the image with grid. This will be used in later processing
    name = os.path.splitext(file_name)[0]+"_grid.jpg"
    # Avoid using static addresses
    # Use this instead, but be cautious:
    # file_path = os.path.join(os.getcwd()+"\\data_process\\ref_image", name)
    file_path = os.path.join(os.getcwd() + "\\data_process\\ref_image", name)
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
