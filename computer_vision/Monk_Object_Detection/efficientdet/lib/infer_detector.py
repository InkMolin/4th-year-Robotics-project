import os
import argparse
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import transforms
from Monk_Object_Detection.efficientdet.lib.src.dataset import CocoDataset, Resizer, Normalizer, Augmenter, collater
from Monk_Object_Detection.efficientdet.lib.src.model import EfficientDet
from tensorboardX import SummaryWriter
import shutil
import numpy as np
from tqdm.autonotebook import tqdm
from Monk_Object_Detection.efficientdet.lib.src.config import colors
import cv2
import time as time

class Infer():
    def __init__(self, verbose=1):
        self.system_dict = {};
        self.system_dict["verbose"] = verbose;
        self.system_dict["local"] = {};
        self.system_dict["local"]["common_size"] = 512;
        self.system_dict["local"]["mean"] = np.array([[[0.485, 0.456, 0.406]]])
        self.system_dict["local"]["std"] = np.array([[[0.229, 0.224, 0.225]]])

    def Model(self, model_dir="trained_efficientdet_version/trained_instance/"):
        self.system_dict["local"]["model"] = torch.load(model_dir + "signatrix_efficientdet_coco.pth", map_location=torch.device('cpu')).module
        if torch.cuda.is_available():
            self.system_dict["local"]["model"] = self.system_dict["local"]["model"].cuda();

    def Predict(self, frame, class_list, desired_button, vis_threshold = 0.4):
        # Get the frame and perform pre-processing
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB);
        frame_resized = cv2.resize(frame_rgb, (512, 512))
        image = frame_resized.astype(np.float32) / 255.;
        image = (image.astype(np.float32) - self.system_dict["local"]["mean"]) / self.system_dict["local"]["std"]
        new_image = np.zeros((self.system_dict["local"]["common_size"], self.system_dict["local"]["common_size"], 3))
        new_image[0:512, 0:512] = image
        img = torch.from_numpy(new_image)
        
        # Predict buttons inside the image (scores, labels and their prediction "box")
        with torch.no_grad():
            scores, labels, boxes = self.system_dict["local"]["model"](img.permute(2, 0, 1).float().unsqueeze(dim=0))
            boxes /= 1;

        try:
            # If more than one button was predicted
            if boxes.shape[0] > 0:
                # Go through all the predicted buttons
                for box_id in range(boxes.shape[0]):
                    # If the predicted button is not the desired one, go to the next
                    pred_label = int(labels[box_id])
                    if class_list[pred_label] != desired_button:
                        continue
                    
                    # If the prediction probability is less than the threshold
                    pred_prob = float(scores[box_id])
                    if pred_prob < vis_threshold:
                        break
                    
                    # If the desired button was found add it to the frame and save the image
                    xmin, ymin, xmax, ymax = boxes[box_id, :]
                    xmin, ymin, xmax, ymax = int(xmin), int(ymin), int(xmax), int(ymax)
                    color = colors[pred_label]
                    cv2.rectangle(frame_resized, (xmin, ymin), (xmax, ymax), color, 2)
                    text_size = cv2.getTextSize(class_list[pred_label] + ' : %.2f' % pred_prob, cv2.FONT_HERSHEY_PLAIN, 1, 1)[0]
                    cv2.rectangle(frame_resized, (xmin, ymin), (xmin + text_size[0] + 3, ymin + text_size[1] + 4), color, -1)
                    cv2.putText(
                        frame_resized, class_list[pred_label] + ' : %.2f' % pred_prob,
                        (xmin, ymin + text_size[1] + 4), cv2.FONT_HERSHEY_PLAIN, 1,
                        (255, 255, 255), 1)
                    cv2.circle(frame_resized, (int((xmin+xmax)/2), int((ymin+ymax)/2)), radius=2, color=(0, 0, 255), thickness=-1)
                    cv2.imwrite('localized_button.png', frame_resized)

                    # Return the centre point of the predicted button
                    return (int((xmin+xmax)/2), int((ymin+ymax)/2))
                
                return None  # Return none if no buttons were found
            
        # Return None if there is an error when going through the predicted buttons
        except: 
            print("NO Object Detected")
            return None

    def predict_batch_of_images(self, img_folder, class_list, vis_threshold = 0.4, output_folder='Inference'):
        
        all_filenames = os.listdir(img_folder)
        all_filenames.sort()
        generated_count = 0
        for filename in all_filenames:
            img_path = "{}/{}".format(img_folder, filename)
            try:
                self.Predict(img_path , class_list, vis_threshold ,output_folder)
                generated_count += 1
            except:
                continue
        print("Objects detected  for {} images".format(generated_count))

        
