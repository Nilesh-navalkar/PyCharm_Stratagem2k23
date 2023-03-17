from django.shortcuts import render,redirect
from .models import profile,token
from django.contrib import messages
import cv2
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login as log_in,authenticate,logout
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
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        aadhar=request.POST.get("aadhar")
        pp=request.FILES.get("pp")
        psw1=request.POST.get("psw1")
        psw2=request.POST.get("psw2")
        #print(aadhar,pp,psw1,psw2)
        if User.objects.filter(username=aadhar).exists():
            messages.error(request,"User already exists ")
            return redirect("register")
        elif User.objects.filter(email=email).exists():
            messages.error(request,"Email taken ")
            return redirect("register")
        elif psw1!=psw2:
            messages.error(request,"passwords dont match ")
            return redirect("register")
        else:
            u=User.objects.create_user(username=aadhar,email=email,password=psw1)
            u.save()
            ap=profile.objects.create(u=u,name=name,aadhar=aadhar,email=email,pp=pp)
            ap.save()
            image="media/"+ap.pp.name
            detections = embedder.extract(image, threshold=0.95)
            #print(detections[0]['embedding'])
            pencoding=detections[0]['embedding']
            s=str(pencoding)
            ap.pencoding=s[1:-1]
            ap.save()
            #x=np.fromstring(s[1:-1], sep=' ').reshape(512, )
            messages.error(request,"user registeration complete ")
            return redirect("register")
                
    return render(request,"register.html")

def login(request):
    if request.method=='POST':
        un=request.POST.get('un')
        pss=request.POST.get('psw')
        user=authenticate(username=un,password=pss)
        if user is not None:
            if user.is_superuser:
                log_in(request,user)
                return redirect("mark")
            else:
                messages.error(request,"invalid credentials")
                return redirect("login")
        else:
            messages.error(request,"invalid credentials")
            return redirect("login")
    return render(request,'login.html')

@staff_member_required
@login_required(login_url="login")
def log_out(request):
    logout(request) 
    return redirect("login")
 

def gen(camera):
	while True:
		frame,img,bloo= camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed(request):
	return StreamingHttpResponse(gen(VideoCamera()),
                    #video type
					content_type='multipart/x-mixed-replace; boundary=frame')


@staff_member_required
@login_required(login_url="login")
def mark(request):
    result=False
    min_dist = 9999
    identity = ""
    if request.method=="POST":
        vc=VideoCamera()
        bytes,image,result = vc.get_frame()
        #print(image)
        cv2.imshow('img',image)
    if result:
        detections = embedder.extract(image, threshold=0.95)
        print(detections)
        if len(detections)<1 or len(detections)>1:
             messages.info(request,"face not detected")
             return redirect("mark")
        encoding=detections[0]['embedding']
        all=profile.objects.values_list("aadhar","pencoding")
        #print(all)
        for i in all:
            x=np.fromstring(i[1], sep=' ').reshape(512, )
            #print(encoding,x)
            dist=np.linalg.norm(encoding - x)
            print("d=",dist)
            if(dist < min_dist):
                min_dist = dist
                identity = i[0]
        threshold=0.95
        if min_dist < threshold:
            entry=token.objects.create(aadhar=identity,date=datetime.today().strftime('%Y-%m-%d'))
            messages.error(request,"token for "+str(identity)+' is : '+str(entry.tken))
            return redirect("mark")
        else:
            messages.error(request,"no matching faces")
            return redirect("mark")
    #print(identity,min_dist) 
    return render(request,"mark.html") 
