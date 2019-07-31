import json
import numpy as np
import pandas as pd
import cv2
import pickle
from smpl_np import SMPLModel
from config import model_folder

def get_points(keypoints):
    x = np.array(keypoints)[range(0, len(keypoints),3)]
    y = np.array(keypoints)[range(1, len(keypoints),3)]
    return x, y

def get_point_on_canvas(keypoints):
    #Use  5th and 6th last points for kop4ik and last point for leg (to calculate distance)
    # dist koleno-dist_noga
    x, y = get_points(keypoints)
    x_fin = (x[-5]+x[-6])/2
    y_mean = (y[-5]+y[-6])/2
    dist1 = np.power(np.power(x_fin - x[-1],2)+np.power(y_mean-y[-1],2),1/2)
    dist2 = np.power(np.power(x_fin - x[-2],2)+np.power(y_mean-y[-2],2),1/2)
    dist_mean = (dist1+dist2)/2
    y_fin = y_mean + dist_mean
    return x_fin, y_fin

def frame_to_texture_coords(x,y, homo_mat):
    return cv2.perspectiveTransform(np.array([[[x,y]]]),homo_mat)

def texture_to_blender_coords(x,y):
    y = 1920 - y
    x = (x/1920-0.5)*10
    y = (y/1920-0.5)*10
    return x,y

def generate_objects(hmmr_out):
    folder_path = model_folder
    model = SMPLModel("assets/basicmodel_m_lbs_10_207_0_v1.0.0.pkl")
    counter = 0
    for i in hmmr_out["verts"]:
        model.verts = i
        model.save_to_obj(folder_path+"/"+str(counter)+".obj")
        counter+=1

def alpha_pose_to_blender(alpha_pose_dict, homo_file, out_path = "positions.pkl"):
    points = []
    frame_names = [dic for dic in dicta]
    frame_names = np.array(frame_names)
    u, indexes = np.unique(frame_names, return_index=True)
    for i in range(len(indexes)):
        try:
            keypoints = alpha_pose_dict[i][1]
            homo = homo_file[i]["texture"]
            x_canv, y_canv = get_point_on_canvas(keypoints)
            x_text, y_text = frame_to_texture_coords(x_canv, y_canv, homo)[0][0]
            x_blend, y_blend = texture_to_blender_coords(x_text, y_text)
            points.append([x_blend, y_blend])
        except:
            points.append([np.nan, np.nan])
            continue
    points = pd.DataFrame(points).interpolate().values
    with open(out_path,"wb") as file:
        pickle.dump(points,file)
    return points

def convert_frame(frame):
    convert = {}
    for keypoint in frame:
        convert[keypoint["idx"]] = keypoint["keypoints"]
    return convert

def convert_dicta(dicta):
    frames = [convert_frame(dicta[i]) for i in dicta]
    return frames

print("1) Load Assets")

with open("assets/alphapose-results-forvis-tracked.json","r") as file:
    dicta = json.load(file)
alpha_pose_dict = convert_dicta(dicta)
    
print("AlphaPose loaded")

with open("assets/homo.pkl","rb") as file:
    homo = pickle.load(file)
    
print("Homography loaded")

with open("assets/hmmr_output.pkl","rb") as file:
    hmmr_out = pickle.load(file)
    
print("HMMR loaded")
print("2) Generate objects")
    
generate_objects(hmmr_out)
print("Models saved")
alpha_pose_to_blender(alpha_pose_dict, homo)
print("Positioning Done")
