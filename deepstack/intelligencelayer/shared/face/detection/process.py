import cv2
from detection.networks import s3fd, detect
from .bbox import nms
import torch
import time

def load_model(model,path):
    checkpoint = torch.load(path, map_location=lambda storage, loc: storage)

    try:
        model.load_state_dict(checkpoint)
        
    except:
        copy = dict()
        for x, y in zip(model.state_dict(), checkpoint):
            new_name = y[y.index(x):]
            copy[new_name] = checkpoint[y]

class FaceModel(object):
    def __init__(self,model_path,cuda=False):

        self.cuda_mode = False

        self.model = s3fd()

        load_model(self.model,model_path)
        if torch.cuda.is_available() and cuda:
            self.model.cuda()
            self.cuda_mode = True

        self.model.eval()
        
    def predict(self, image,img_size=416,threshold=0.8,skip=0):

        bboxs = detect(self.model,image,img_size,threshold,self.cuda_mode,skip=skip)

        return bboxs