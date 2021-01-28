import os
from pypylon import pylon
import cv2
from base_camera import BaseCamera


class Camera(BaseCamera):
    
    def __init__(self):
        Camera.set_video_source('basler')
        super(Camera, self).__init__()
    
    @staticmethod
    def set_video_source(source):
        Camera.video_source = source
        
    @staticmethod
    def frames():
        
        # conecting to the first available camera
        camera=pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        camera.Open()
        camera.GainAuto.SetValue("Once") 
        
        camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
        converter = pylon.ImageFormatConverter()


        # converting to opencv bgr format
        converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
        
        while camera.IsGrabbing():
            grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)            
            

            if grabResult.GrabSucceeded():
                image = converter.Convert(grabResult)
                img = image.GetArray()
                
                img = img[:-1, :-1, :]
                
                # aca5472-17uc
                width = 5472//1
                height = 3648//1
                dim = (width,height)
                img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)                
                
                # img_width = img.shape[1]
                # img_height = img.shape[0]
                
                # width = int(img_width*.75)
                # height = int(img_height*.7)        

                # start_point = ((img_width-width)//2, (img_height-height)//2)
                # end_point = ((img_width-width)//2+width, (img_height-height)//2+height)               
                # color = (0, 0, 255)                
                # thickness = 1
               
                # img = cv2.rectangle(img, start_point, end_point, color, thickness)
                
                # template match algorithm
                
                
                #yield cv2.imencode('.jpg', img)[1].tobytes()
                yield img












