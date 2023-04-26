import cv2
import numpy as np

# General Settings
NUM_IMAGES = 11
SQUARE_SIZE = 22  # (mm)
CALIBRATION_IMAGES = [f'calibration_pictures/calibration_{i}.png' for i in range(NUM_IMAGES)]

# Construct the v matrix, from which the intrinsic parameters are computed
def v_T_ij(H, i, j, image):
    v = np.zeros((1, 6))
    v[0, 0] = H[0, i-1, image] * H[0, j-1, image]
    v[0, 1] = H[1, i-1, image] * H[0, j-1, image] + H[0, i-1, image] * H[1, j-1, image]
    v[0, 2] = H[1, i-1, image] * H[1, j-1, image]
    v[0, 3] = H[2, i-1, image] * H[0, j-1, image] + H[0, i-1, image] * H[2, j-1, image]
    v[0, 4] = H[2, i-1, image] * H[1, j-1, image] + H[1, i-1, image] * H[2, j-1, image]
    v[0, 5] = H[2, i-1, image] * H[2, j-1, image]

    return v

# Rearrange image-frame corner points so that they match the order of the equivalent 
# world-frame points  
def rearrange_corner_points(corner_points_image):
    elements_list = [element for element in corner_points_image]
    elements_copy = elements_list.copy()
    for i in range(9):
        for j in range(6):
            elements_list[i*6+j] = elements_copy[i*6+5-j]
    
    return np.array(elements_list)


def main():
    
    # Detect the checkerboard corners on the images
    imagePoints = []
    boardSize = None
    for file in CALIBRATION_IMAGES:
        img = cv2.imread(file)
        img = cv2.resize(img, (512, 512))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (6, 9), None)
        if ret:
            boardSize = (6, 9)
            imagePoints.append(corners)

    # Generate the world coordinates of the checkerboard corners ((0,0), (0,22), (0, 44), ...)
    worldPoints = np.zeros((boardSize[0]*boardSize[1], 2), np.float32)
    worldPoints[:, :2] = np.mgrid[0:boardSize[0], 0:boardSize[1]].T.reshape(-1, 2) * SQUARE_SIZE
    worldPoints = np.fliplr(worldPoints)

    # Rearrange image points to match the equivalent world-frame ones 
    rearranged_image_points = [rearrange_corner_points(imagePoints[i]) for i in range(len(imagePoints))]

    n_rows = rearranged_image_points[0].shape[0]

    # Generate matrix phi
    phi = np.zeros((2*n_rows, 9, NUM_IMAGES))
    for image in range(NUM_IMAGES):
        row_counter = 0
        for row in range(n_rows):
            x_i, y_i = rearranged_image_points[image][row][0]
            X_i, Y_i = worldPoints[row]
            phi[row_counter, :, image] = [0, 0, 0, X_i, Y_i, 1, -y_i*X_i, -y_i*Y_i, -y_i]
            phi[row_counter+1, :, image] = [X_i, Y_i, 1, 0, 0, 0, -x_i*X_i, -x_i*Y_i, -x_i]
            row_counter += 2

    # Obtain camera matrix by performing SVD on phi
    H = np.zeros((3, 3, NUM_IMAGES))
    for i in range(NUM_IMAGES):
        U, S, V = np.linalg.svd(phi[:, :, i])
        H[:, :, i] = np.reshape(V.T[:, -1], (3, 3))

    # Generate v matrix
    v = np.zeros((2*NUM_IMAGES, 6))
    r_counter = 0
    for image in range(NUM_IMAGES):
        v_T_11 = v_T_ij(H, 1, 1, image)
        v_T_12 = v_T_ij(H, 1, 2, image)
        v_T_22 = v_T_ij(H, 2, 2, image)
        v[r_counter,:] = v_T_12
        v[r_counter+1,:] = (v_T_11 - v_T_22) 
        r_counter += 2

    # Perform SVD on v
    U, S, V = np.linalg.svd(v)
    V = V.T

    # Get the last column of V and create B_matrix
    B_vector = V[:,-1]
    B_matrix = np.array([[B_vector[0], B_vector[1], B_vector[3]],
    [B_vector[1], B_vector[2], B_vector[4]],
    [B_vector[3], B_vector[4], B_vector[5]]])

    # Calculate the values of the intrinsic parameters from B
    y0 = (B_matrix[0,1]*B_matrix[0,2]-B_matrix[0,0]*B_matrix[1,2])/(B_matrix[0,0]*B_matrix[1,1]-(B_matrix[0,1])**2)
    lambda_ = B_matrix[2,2]-((B_matrix[0,2])**2+y0*(B_matrix[0,1]*B_matrix[0,2]-B_matrix[0,0]*B_matrix[1,2]))/B_matrix[0,0]
    alpha = np.sqrt(lambda_/B_matrix[0,0])
    beta = np.sqrt(lambda_*B_matrix[0,0]/(B_matrix[0,0]*B_matrix[1,1]-(B_matrix[0,1])**2))
    gamma = -B_matrix[0,1]*alpha**2*beta/lambda_
    x0 = gamma*y0/alpha-B_matrix[0,2]*alpha**2/lambda_

    # Construct the intrinsic parameter matrix
    K = np.array([[alpha, gamma, x0], [0, beta, y0], [0, 0, 1]])
    print(K)

if __name__ == "__main__":
    main()