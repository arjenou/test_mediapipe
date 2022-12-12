import cv2
import os
import mediapipe as mp
import matplotlib.pyplot as plt
import time as ti
from torch import NoneType
import argparse

from zmq import NULL
# %matplotlib inlinew

ap = argparse.ArgumentParser()
DEFAULT_FILEPATH = "exp"
ap.add_argument('-filepath', type=str, default=DEFAULT_FILEPATH,
                    help='set file')
args = ap.parse_args()

DEFAULT_FILEPATH = args.filepath
print(DEFAULT_FILEPATH)
extt="t.jpg"
while True:
  Filelist=[]
  org_img_folder=f'/content/drive/MyDrive/Yolov5_DeepSort/runs/track/{DEFAULT_FILEPATH}'
  
  def getFileList(dir,ext=None):
    newDir = dir
    if os.path.isfile(dir):
      if ext is None:
          pass
      else:
        if ext in dir[-3:] and extt not in dir[-5:]:
          return Filelist.append(dir)
    
    elif os.path.isdir(dir):

      for s in os.listdir(dir):
          newDir=os.path.join(dir,s)
          getFileList(newDir, ext)


  imglist = getFileList(org_img_folder,'jpg')
  if Filelist is None:
    continue

  mp_pose = mp.solutions.pose


  mp_drawing = mp.solutions.drawing_utils 

  pose = mp_pose.Pose(static_image_mode=True,        
                      model_complexity=2,           
                      smooth_landmarks=True,        
                      enable_segmentation=True,     
                      min_detection_confidence=0.5,  
                      min_tracking_confidence=0.5)  

  
  for imgpath in Filelist:
    imgname= os.path.splitext(os.path.basename(imgpath))[0]
    img = cv2.imread(imgpath)
    img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(img_RGB)
    debug_image = mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    base_name=os.path.splitext(imgpath)[0]
    h = img.shape[0]
    w = img.shape[1]
    if results.pose_landmarks:
      for i in range(33): 

        cx = int(results.pose_landmarks.landmark[i].x * w)
        cy = int(results.pose_landmarks.landmark[i].y * h)
        cz = results.pose_landmarks.landmark[i].z
        with open(f"{base_name}_test.txt","a") as f:
          f.write(f"({cx},{cy})\n")
        radius = 1

        if i == 0: 
            img = cv2.circle(img,(cx,cy), radius, (0,0,255), -1)
        elif i in [11,12]: 
            img = cv2.circle(img,(cx,cy), radius, (223,155,6), -1)
        elif i in [23,24]: 
            img = cv2.circle(img,(cx,cy), radius, (1,240,255), -1)
        elif i in [13,14]: 
            img = cv2.circle(img,(cx,cy), radius, (140,47,240), -1)
        elif i in [25,26]: 
            img = cv2.circle(img,(cx,cy), radius, (0,0,255), -1)
        elif i in [15,16,27,28]: 
            img = cv2.circle(img,(cx,cy), radius, (223,155,60), -1)
        elif i in [17,19,21]: 
            img = cv2.circle(img,(cx,cy), radius, (94,218,121), -1)
        elif i in [18,20,22]: 
            img = cv2.circle(img,(cx,cy), radius, (16,144,247), -1)
        elif i in [27,29,31]: 
            img = cv2.circle(img,(cx,cy), radius, (29,123,243), -1)
        elif i in [28,30,32]: 
            img = cv2.circle(img,(cx,cy), radius, (193,182,255), -1)
        elif i in [9,10]: 
            img = cv2.circle(img,(cx,cy), radius, (205,235,255), -1)
        elif i in [1,2,3,4,5,6,7,8]: 
            img = cv2.circle(img,(cx,cy), radius, (94,218,121), -1)
        else: 
            img = cv2.circle(img,(cx,cy), radius, (0,255,0), -1)
    else:
      print("no kindpoint",imgpath)
      for i in range(33): 
        with open(f"{base_name}_test.txt","a") as f:
          f.write(f"(NULL,NULL)\n")
      print("fail_test.txt make")
      cv2.imwrite(f"{base_name}_fail_test.jpg",img)
      os.system(f"rm -f {imgpath}")
      continue
    cv2.imwrite(f"{base_name}_test.jpg",img)
    os.system(f"rm -f {imgpath}")
    # cv2.imwrite(f"{base_name}.jepg",img)
    print(f"Sucess get {imgpath} is {base_name}")
  # ti.sleep(10)