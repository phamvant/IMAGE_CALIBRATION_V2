# Import required libraries
import cv2
import os

# Initiate camera's default values
### This could be changed in future updates
rtsp_user = "admin"
rtsp_pass = "bk123456"
ip = "192.168.1.115"
port = "554"
device_number = "1"

# Define functions
def create_camera(rtsp_username, rtsp_password, ip_val, port_val, device_no):
    # Set up camera rtsp hyperlink
    rtsp = "rtsp://" + rtsp_username + ":" + rtsp_password + "@" + ip_val + ":" + port_val + "/Streaming/channels/" \
           + device_no
    # Capture video frames
    cap = cv2.VideoCapture()
    cap.open(rtsp)
    # Define additional values
    # cap.set(10, 1920)
    # cap.set(10, 1080)
    # cap.set(10, 100)
    return cap

def main_camera_func(parent_path, parking_lot_name, runtime_value):
    # Define image save path
    image_save_path = "{}\\data_process\\{}\\image_take_from_camera".format(parent_path, parking_lot_name)

    ### Debug:
    # print(image_save_path)

    # Define image dimensions
    width = 1920
    height = 1080
    image_dimension = (width, height)

    # Capture image
    camera_capture = create_camera(rtsp_user, rtsp_pass, ip, port, device_number)
    read_status, image_from_camera = camera_capture.read()

    # Save image data, if capture succeed
    if read_status:
        # Resize the image to the desired dimensions
        image_data = cv2.resize(image_from_camera, image_dimension)

        # Get image path & save captured image data
        image_name = "{}_{}_ref.jpg".format(parking_lot_name, runtime_value)
        image_path = os.path.join(image_save_path, image_name)
        # Write the image
        cv2.imwrite(image_path, image_data)

        ### Debug:
        # print(image_path)
        # cv2.imshow("Captured image", image_data)

    else:
        print("Get image data failed, check the camera & connection to the camera")
        image_path = image_save_path

    return read_status, image_path
