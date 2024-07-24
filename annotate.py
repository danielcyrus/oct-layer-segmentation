import cv2 as cv
import numpy as np
from os import listdir
from os.path import isfile, join
from scipy.interpolate import interp1d
import pandas as pd
import os.path

imgArr = np.load("archive/AllImgs.npy")
print(imgArr.shape)
#onlyfiles = [f for f in listdir("images/") if isfile(join("images/", f))]
#onlyfiles.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
index = 0
colours = [(0,0,255),(158, 50, 168),(224, 195, 29),(49, 207, 222),(224, 166, 40),(79, 227, 30),(255,0,0),(222, 51, 193),(0, 255, 255)]
#img = cv.imread("images/" + onlyfiles[index])
width = imgArr.shape[2]

img = imgArr[index].copy()
lines = []
points = []
def draw_circle(event,x,y,flags,param):
 global img,points
 if event == cv.EVENT_LBUTTONDOWN:
    cv.circle(img,(x,y),2,(255,0,0),-1)
    points.append([x,y])

cv.namedWindow('image')
cv.setMouseCallback('image',draw_circle)


def fitLine():
    (xp,yp) = zip(*points)
    fun = interp1d(xp,yp,kind='cubic', fill_value="extrapolate")
    xc = np.linspace(0,width,21)
    pts = np.stack([xc.astype(np.int32),fun(xc).astype(np.int32)],axis=1)
    lines.append(pts.tolist())
    cv.polylines(img,[pts],False,colours[lines.__len__()-1],1) 


while(True):
 cv.imshow('image',img)
 cv.putText(img,str(index),(10,20),cv.QT_FONT_NORMAL,.5,(0,0,255))
 key = cv.waitKey(10)
 if key & 0xFF == 27:
     break
 elif key== ord('n'):
    if len(lines)==9:
        df = pd.DataFrame(columns=["ILMx","ILMy","RNFL-CGLx","RNFL-CGLy","IPL-INLx","IPL-INLy","INL-OPLx","INL-OPLy","OPL-ONLx","OPL-ONLy","ELMx","ELMy","IS-OSx","IS-OSy","OS-RPEx","OS-RPEy","BMx","BMy"])
        df[["ILMx","ILMy"]] = lines[0]
        df[["RNFL-CGLx","RNFL-CGLy"]] = lines[1]
        df[["IPL-INLx","IPL-INLy"]] = lines[2]
        df[["INL-OPLx","INL-OPLy"]] = lines[3]
        df[["OPL-ONLx","OPL-ONLy"]] = lines[4]
        df[["ELMx","ELMy"]] = lines[5]
        df[["IS-OSx","IS-OSy"]] = lines[6]
        df[["OS-RPEx","OS-RPEy"]] = lines[7]
        df[["BMx","BMy"]] = lines[8]
        df.to_csv("archive/labels/"+str(index)+".csv")
        points = []
        lines = []
        #np.savetxt(onlyfiles[index].replace("png","")+"csv", lines, delimiter=",")
    index+=1
    while(os.path.isfile("archive/labels/"+str(index)+".csv")):
            index+=1
        
    img = imgArr[index].copy()
   
    

 elif key== ord('d'):
    fitLine() 
    points = [] 
 elif key== ord('r'):
    points = []
    lines = []
    
    img = imgArr[index].copy()
    

cv.destroyAllWindows()

