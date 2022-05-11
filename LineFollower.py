import cv2
import numpy as np

# Put Tello Stuff here
# add take off here also

cap=cv2.VideoCapture(0)
# hsvVals=[0, 0, 117, 179, 22, 219]
hsvVals=[0, 0, 117, 179, 22, 219]
sensors=3
threshold=0.2
width, height = 480, 360 # match cam width and height in pixels
sensitivity = 3 # higher number means less sensitive
weights = [-25, -15, 0, 15, 25] # how much to turn based on sensor
curve = 0
forward_speed = 15

def thresholding(img):
  hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
  lower=np.array([hsvVals[0],hsvVals[1],hsvVals[2]])
  upper=np.array([hsvVals[3],hsvVals[4],hsvVals[5]])
  mask=cv2.inRange(hsv,lower,upper)
  return mask

def getContours(imgThres,img):
  cx = 0
  contours, hierarchy = cv2.findContours(imgThres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
  if not contours:
    # print("Contours is empty")
    return cx
  biggest=max(contours, key=cv2.contourArea)
  x,y,w,h=cv2.boundingRect(biggest)
  cx=x+ w//2
  cy=y+ h//2
  cv2.drawContours(img,biggest,-1,(255,0,255),7)
  cv2.circle(img,(cx,cy),10,(0,255,0),cv2.FILLED)
  return cx

def getSensorOutput(imgThres, sensors):
  imgs=np.hsplit(imgThres,sensors)
  totalPixels=(img.shape[1]//sensors)*img.shape[0]
  senOut=[]
  for x,im in enumerate(imgs):
    pixelCount = cv2.countNonZero(im)
    if pixelCount > threshold*totalPixels:
      senOut.append(1)
    else:
      senOut.append(0)
    # cv2.imshow(str(x),im)
  # print(senOut)
  return senOut

def sendCommands(senOut, cx):
  global curve
  ## TRANSLATION
  lr = (cx - width//2) // sensitivity # left right
  lr = int(np.clip(lr, -10, 10)) # limit movement speed
  if lr < 2 and lr > -2: lr = 0 # set as zero for insignificant lr values

  ## ROTATION
  if senOut == [1,0,0]: curve = weights[0]
  elif senOut == [1,1,0]: curve = weights[1]
  elif senOut == [0,1,0]: curve = weights[2]
  elif senOut == [0,1,1]: curve = weights[3]
  elif senOut == [0,0,1]: curve = weights[4]
  elif senOut == [0,0,0]: curve = weights[2] # lost
  elif senOut == [1,1,1]: curve = weights[2] # illegal
  elif senOut == [1,0,1]: curve = weights[2] # illegal

  # me.send_rc_control(lr, forward_speed, 0, curve)

while True:
  _, img=cap.read()
  # use drone image capture
  img=cv2.resize(img,(width, height))
  #img=cv2.flip(img,0)

  imgThres = thresholding(img)
  cx = getContours(imgThres,img) ## Translation
  senOut = getSensorOutput(imgThres,sensors)
  sendCommands(senOut, cx) # translation, rotation
  cv2.imshow('Output', img)
  cv2.imshow('Path', imgThres)
  # add quit later
  cv2.waitKey(1)