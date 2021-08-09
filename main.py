import cv2

from noparkingsigndetection import noparkingsigndetection
from numberplatedetection import numberplatedetection
from savenumberplateindatabase import savenumberplateindatabase
#from sendsms import sendsms

img=cv2.imread('signandnumber/0.jpg')

cv2.namedWindow('Original Image',cv2.WINDOW_NORMAL)
cv2.resizeWindow('Original Image',800,700)
cv2.imshow('Original Image',img)
cv2.waitKey(0)
cv2.destroyWindow('Original Image')


sign=noparkingsigndetection(img)

if(sign==True):
    
    print("NO PARKING sign detected")

else:
    
    print("NO PARKING sign not detected")

number=numberplatedetection(img)

if(number==''):
    
    print("Number plate not detected")

else:
    
    print("Number plate detected")

if(sign==True and number!=''):
    
    fine=savenumberplateindatabase(number)
    
    if(fine==True):
        print("Fine generated")
        print("Sending SMS..")
        #sendsms()
cv2.namedWindow('Original Image',cv2.WINDOW_NORMAL)
cv2.resizeWindow('Original Image',800,700)        
cv2.imshow('Original Image',img)       
cv2.waitKey(0)
cv2.destroyAllWindows()