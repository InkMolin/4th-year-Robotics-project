## Semi-Autonomous Mobile Robot Controlling A Lift Using Real-Time Image Recognition And Robotic Arm Manipulator Repository
This repository contains the different files employed during our 4th year project. The repository is split into 3 different sections.

### Arduino
This part contains the arduino files that were employed for both the [up/down movement of the arm](/arduino/movement/arm_control_isolated_v3.ino) and the [robot's localization and movement](/arduino/movement/base_robot_code_clean_ver.ino).

### Raspberry Pi
This section is comprised of the python files used for the integration of the robot and the arm's movements. Additionally, a [testing file](raspberry_pi/controller/functionTestPanel.py) 
was created to ensure that the different actions that the robot needed to perform
could be carried out successfully.

### Computer Vision
This section is focused on the different computer vision algorithms utilized. It is comprised of a series of python files:
- The [intrinsic parameter extraction file](/computer_vision/intrinsic_parameter_extraction.py) was used to obtain the intrinsic parameters of the webcam used. The
[calibration pictures used](/computer_vision/calibration_pictures/) can also be found.
- The [person recognition file](/computer_vision/person_recognition.py) contains the code employed for the detection of people before the robot entered the lift.
The [MobileNet SSD model files](/computer_vision/coco_ssd_mobilenet_v1/) required for running the object detection model are also included in the repository.
- The [camera calibration and button recognition file](/computer_vision/button_recon_and_camera_calibration.py) is responsible for detecting the lift button that 
is wanted and determining how much the arm and the robot need to move in order to press it. The [model instance used](/computer_vision/trained_efficientdet_version/trained_instance/),
the [training notebook employed](/computer_vision/Roboflow_EfficientDet_v2_Training_Modified.ipynb) to train that model and the 
[infer class](/computer_vision/Monk_Object_Detection/efficientdet/lib/infer_detector.py) used for running the button recognition algorithm can all be found in the
repository.
