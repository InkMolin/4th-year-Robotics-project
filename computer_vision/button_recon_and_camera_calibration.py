# Import packages
import os
import cv2
import numpy as np
import time
from threading import Thread
from Monk_Object_Detection.efficientdet.lib.infer_detector import Infer

# Define VideoStream class to handle streaming of video from webcam in separate processing thread
# Source - Adrian Rosebrock, PyImageSearch: https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/
class VideoStream:
    """Camera object that controls video streaming from the Picamera"""
    def __init__(self,resolution=(512,512),framerate=30):
        # Initialize the PiCamera and the camera image stream
        self.stream = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.stream.set(3,resolution[0])
        ret = self.stream.set(4,resolution[1])
            
        # Read first frame from the stream
        (self.grabbed, self.frame) = self.stream.read()

	# Variable to control when the camera is stopped
        self.stopped = False

    def start(self):
	# Start the thread that reads frames from the video stream
        Thread(target=self.update,args=()).start()
        return self

    def update(self):
        # Keep looping indefinitely until the thread is stopped
        while True:
            # If the camera is stopped, stop the thread
            if self.stopped:
                # Close camera resources
                self.stream.release()
                return

            # Otherwise, grab the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
	# Return the most recent frame
        return self.frame

    def stop(self):
	# Indicate that the camera and thread should be stopped
        self.stopped = True

# Initialize frame rate calculation
frame_rate_calc = 1
freq = cv2.getTickFrequency()

# Create window
cv2.namedWindow('Object detector', cv2.WINDOW_NORMAL)

# Initialize the model
model = Infer()
model.Model(model_dir="trained_efficientdet_version/trained_instance/")

# Define the board size
BOARD_SIZE = (6, 9)
SQUARE_SIZE = 22

# Generate the world points coordinates ((0, 0), (0, 22), (0, 44)...)
WORLD_POINTS = np.zeros((BOARD_SIZE[0]*BOARD_SIZE[1], 2), np.float32)
WORLD_POINTS[:, :2] = np.mgrid[0:BOARD_SIZE[0], 0:BOARD_SIZE[1]].T.reshape(-1, 2) * SQUARE_SIZE
WORLD_POINTS = np.fliplr(WORLD_POINTS)

# Video capture source camera 
VIDEO_CAPTURE = cv2.VideoCapture(1, cv2.CAP_DSHOW)
VIDEO_CAPTURE.set(cv2.CAP_PROP_FRAME_WIDTH, 512)
VIDEO_CAPTURE.set(cv2.CAP_PROP_FRAME_HEIGHT, 512)

# Initialize video stream
VIDEO_STREAM = VideoStream(resolution=(512, 512),framerate=30).start()
time.sleep(1)

# Initialize the initial horizontal and vertical arm positions
# These values depend on the specific experiment setup. They must be added before
# the script is able to run
INITIAL_HORIZONTAL_ARM_POS = 0
INITIAL_VERTICAL_ARM_POS = 0

# Initialize the list containing the different button labels
CLASS_LIST = [
    'elevator-buttons',
    '1',
    '2',
    '3',
    '4',
    'alarm',
    'down',
    'g',
    'key',
    'open',
    'up'
]

# Construct intrinsic parameter matrix with the values obtained using the extraction code
INT_PARAM = { 
    'alpha': 446.8883496875562,
    'gamma': 1.887597052700515,
    'beta': 790.5375172631137,
    'x0': 248.88180621330662,
    'y0': 205.8232296694697,
}
K = np.array([[INT_PARAM['alpha'], INT_PARAM['gamma'], INT_PARAM['x0']], [0, INT_PARAM['beta'], INT_PARAM['y0']], [0, 0, 1]])

# Function to rearrange image-frame corner points so that they match the order of the equivalent 
# world-frame points
def rearrange_corner_points(corner_points_image):
    elements_list = [element for element in corner_points_image]
    elements_copy = elements_list.copy()
    for i in range(9):
        for j in range(6):
            elements_list[i*6+j] = elements_copy[i*6+5-j]
    return np.array(elements_list)

# Function to get the camera matrix of the working image of the robot
def get_h_value_for_working_image(frame):
    # Frame pre-processing
    frame = cv2.resize(frame, (512, 512))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Find corner points and rearrange them to match the world-frame points
    ret, corners = cv2.findChessboardCorners(gray, (6, 9), None)
    if ret:
        imagePoints = corners
    rearranged_image_points = rearrange_corner_points(imagePoints)

    n_rows = rearranged_image_points.shape[0]

    # Generate matrix phi
    phi = np.zeros((2*n_rows, 9))
    row_counter = 0
    for row in range(n_rows):
        x_i, y_i = rearranged_image_points[row][0]
        X_i, Y_i = WORLD_POINTS[row]
        phi[row_counter, :] = [0, 0, 0, X_i, Y_i, 1, -y_i*X_i, -y_i*Y_i, -y_i]
        phi[row_counter+1, :] = [X_i, Y_i, 1, 0, 0, 0, -x_i*X_i, -x_i*Y_i, -x_i]
        row_counter += 2

    # Obtain camera matrix by performing SVD on phi
    H = np.zeros((3, 3))
    _, _, V = np.linalg.svd(phi)
    H = np.reshape(V.T[:, -1], (3, 3))
    return H

# Function to run button recognition algorithm
def run_button_recognition(floor_number, n_seconds, frame_stopper):
    time.sleep(n_seconds)

    # Variable to check if the desired lift button has been found
    retrieved_button = False
    frame_counter = 0
    while not retrieved_button:
        # Exit out of the loop if more than a certain number of frames have been analyzed
        # without finding the button 
        if frame_counter >= frame_stopper:
            break

        # Grab frame from video stream
        frame = VIDEO_STREAM.read()
        frame_c = frame.copy()
        
        # Predict position of the desired button
        pixel_positions = model.Predict(frame_c, CLASS_LIST, floor_number, 0.6)
    
        # Set retrieved_button to True if the desired button was found
        if pixel_positions != None:
            retrieved_button = True
        
        frame_counter += 1  # Increase frame counter

        # Press 'q' to exit the loop
        if cv2.waitKey(1) == ord('q'):
            break
    
    return pixel_positions

# Function to run the camera calibration and tell the robot how much it needs to move
# up/down left_right
def run_calibration(pixel_pos):
    # Get a frame from the video capture
    ret, frame = VIDEO_CAPTURE.read()

    if ret:  # If a frame was read

        # Get the extrinsic parameters and generate Tcw to relate between image and world frames
        R = np.zeros((3, 3))
        C_P_Worg  = np.zeros((3, 1))
        H = get_h_value_for_working_image(frame)
        sigma = 1/np.linalg.norm(np.matmul(np.linalg.inv(K), H[:, 0]))
        R[:, 0] = sigma*np.matmul(np.linalg.inv(K), H[:, 0])
        R[:, 1] = sigma*np.matmul(np.linalg.inv(K), H[:, 1])
        R[:, 2] = np.cross(R[:, 0], R[:, 1])
        C_P_Worg[:, :] = (sigma*np.matmul(np.linalg.inv(K), H[:, 2])).reshape((3,1))
        Tcw = np.concatenate((R, C_P_Worg), axis=1)
        Tcw = np.delete(Tcw, 2, 1)


        # Get the world coordinates of the desired button
        pixels = np.array([[pixel_pos[0]], [pixel_pos[1]], [1]])
        H_ = np.matmul(K, Tcw)
        reconstructed_world_points = np.matmul(np.linalg.inv(H_), pixels)
        reconstructed_world_points = reconstructed_world_points/reconstructed_world_points[2]

        # Calculate how much to move the arm up
        up_movement = INITIAL_VERTICAL_ARM_POS - reconstructed_world_points[1]

        # Calculate how much to move the arm left/right
        l_r_movement = INITIAL_HORIZONTAL_ARM_POS - reconstructed_world_points[0]
        return up_movement, l_r_movement

# Function to run camera_calibration + button recognition
def obtain_x_and_y_movements():
    pixel_pos = run_button_recognition('down', 5, 20)
    return run_calibration(pixel_pos)

obtain_x_and_y_movements()

cv2.destroyAllWindows()
VIDEO_STREAM.stop()