from django.shortcuts import render,redirect
from .models import profile,attendence
from django.contrib import messages
import cv2
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User

from django.http.response import StreamingHttpResponse
from .camera import VideoCamera,IPWebCam

from cv2 import VideoCapture 
cam = VideoCapture(0)

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import numpy as np
from keras_facenet import FaceNet
embedder = FaceNet()

# Create your views here.
def register(request):
    return render(request,'register.html')

def login(request):
    return render(request,'login.html')

def mark(request):
    return render(request,'mark.html')

def logout(request):
    return 

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed(request):
	return StreamingHttpResponse(gen(VideoCamera()),
                    #video type
					content_type='multipart/x-mixed-replace; boundary=frame')
