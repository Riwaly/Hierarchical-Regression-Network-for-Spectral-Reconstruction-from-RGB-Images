import argparse
import os
import cv2
import numpy as np
import hdf5storage as hdf5
from scipy.io import loadmat
from matplotlib import pyplot as plt

from EvalMetrics import *

BIT_8 = 256

# read path
def get_files(path):
    # read a folder, return the complete path
    ret = []
    for root, dirs, files in os.walk(path):
        for filespath in files:
            if filespath[-4:] == '.mat':
                ret.append(os.path.join(root, filespath))
    return ret

def get_jpgs(path):
    # read a folder, return the image name
    ret = []
    for root, dirs, files in os.walk(path):
        for filespath in files:
            if filespath[-4:] == '.mat':
                ret.append(filespath)
    return ret

def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

def single_img_mrae(generated_mat_path, groundtruth_mat_path):
    generated_mat = hdf5.loadmat(generated_mat_path)['cube'] # shape: (482, 512, 31)
    groundtruth_mat = hdf5.loadmat(groundtruth_mat_path)['cube'] # shape: (482, 512, 31)
    mrae = computeMRAE(generated_mat, groundtruth_mat)
    print(mrae)
    return mrae

def single_img_bpmrae(generated_mat_path, groundtruth_mat_path):
    generated_mat = hdf5.loadmat(generated_mat_path)['cube'] # shape: (482, 512, 31)
    groundtruth_mat = hdf5.loadmat(groundtruth_mat_path)['cube'] # shape: (482, 512, 31)
    filters = np.load("./resources/cie_1964_w_gain.npz")['filters']
    mrae = evalBackProjection(generated_mat, groundtruth_mat, filters)
    print(mrae)
    return mrae

def single_img_rmse(generated_mat_path, groundtruth_mat_path):
    generated_mat = hdf5.loadmat(generated_mat_path)['cube'] # shape: (482, 512, 31)
    groundtruth_mat = hdf5.loadmat(groundtruth_mat_path)['cube'] # shape: (482, 512, 31)
    rmse = computeRMSE(generated_mat, groundtruth_mat)
    print(rmse)
    return rmse

def folder_img_mrae(generated_folder_path, groundtruth_folder_path):
    matlist = get_jpgs(generated_folder_path)
    avg_mrae = 0
    for i, matname in enumerate(matlist):
        generated_mat_path = os.path.join(generated_folder_path, matname)
        groundtruth_mat_path = os.path.join(groundtruth_folder_path, matname)
        generated_mat = hdf5.loadmat(generated_mat_path)['cube'] # shape: (482, 512, 31)
        groundtruth_mat = hdf5.loadmat(groundtruth_mat_path)['cube'] # shape: (482, 512, 31)
        mrae = computeMRAE(generated_mat, groundtruth_mat)
        avg_mrae = avg_mrae + mrae
        print('The %d-th mat\'s mrae:' % (i + 1), mrae)
    avg_mrae = avg_mrae / len(matlist)
    print('The average mrae is:', avg_mrae)
    return avg_mrae

def folder_img_bpmrae(generated_folder_path, groundtruth_folder_path):
    matlist = get_jpgs(generated_folder_path)
    avg_mrae = 0
    for i, matname in enumerate(matlist):
        generated_mat_path = os.path.join(generated_folder_path, matname)
        groundtruth_mat_path = os.path.join(groundtruth_folder_path, matname)
        generated_mat = hdf5.loadmat(generated_mat_path)['cube'] # shape: (482, 512, 31)
        groundtruth_mat = hdf5.loadmat(groundtruth_mat_path)['cube'] # shape: (482, 512, 31)
        filters = np.load("./resources/cie_1964_w_gain.npz")['filters']
        mrae = evalBackProjection(generated_mat, groundtruth_mat, filters)
        avg_mrae = avg_mrae + mrae
        print('The %d-th mat\'s mrae:' % (i + 1), mrae)
    avg_mrae = avg_mrae / len(matlist)
    print('The average mrae is:', avg_mrae)
    return avg_mrae

def folder_img_rmse(generated_folder_path, groundtruth_folder_path):
    matlist = get_jpgs(generated_folder_path)
    avg_rmse = 0
    for i, matname in enumerate(matlist):
        generated_mat_path = os.path.join(generated_folder_path, matname)
        groundtruth_mat_path = os.path.join(groundtruth_folder_path, matname)
        generated_mat = hdf5.loadmat(generated_mat_path)['cube'] # shape: (482, 512, 31)
        groundtruth_mat = hdf5.loadmat(groundtruth_mat_path)['cube'] # shape: (482, 512, 31)
        rmse = computeRMSE(generated_mat, groundtruth_mat)
        avg_rmse = avg_rmse + rmse
        print('The %d-th mat\'s rmse:' % (i + 1), rmse)
    avg_rmse = avg_rmse / len(matlist)
    print('The average rmse is:', avg_rmse)
    return avg_rmse

### Validation data !!!

generated_folder_path = "F:\\NTIRE 2020\\spectral reconstruction\\ensemble\\ensemble\\track2"
#generated_folder_path = "F:\\NTIRE 2020\\spectral reconstruction\\compare\\Pix2Pix\\validation\\track1"
#generated_folder_path = "F:\\NTIRE 2020\\spectral reconstruction\\compare\\UResNet\\validation\\track1"

groundtruth_folder_path = "F:\\NTIRE 2020\\spectral reconstruction\\NTIRE2020_Validation_Spectral"
avg_mrae = folder_img_mrae(generated_folder_path, groundtruth_folder_path)
avg_bpmrae = folder_img_bpmrae(generated_folder_path, groundtruth_folder_path)
avg_rmse = folder_img_rmse(generated_folder_path, groundtruth_folder_path)
