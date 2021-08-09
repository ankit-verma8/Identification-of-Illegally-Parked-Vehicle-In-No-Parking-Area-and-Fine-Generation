def numberplatedetection(img):
    import cv2
    import numpy as np
    import pytesseract as tess
    from PIL import Image
    
         
    # Creating a Named window to display image
    height,width,channels=img.shape
    
    img=cv2.resize(img,(799, int((height*799)/width)))
    #cv2.namedWindow('Original Image',cv2.WINDOW_NORMAL)
    #cv2.resizeWindow('Original Image',799,700)
    #cv2.imshow('Original Image',img)
    # Display image
    #cv2.waitKey(0)
    # RGB to Gray scale conversion
    img_gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    
    v=np.median(img_gray)
    
    cv2.namedWindow('Gray Converted Image',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Gray Converted Image',800,700)
    cv2.imshow("Gray Converted Image",img_gray)
    cv2.waitKey(0)
    cv2.destroyWindow('Gray Converted Image')
    # Display Image
    #cv2.waitKey(0)
    # Noise removal with iterative bilateral filter(removes noise while preserving edges)
   
    
    
    
    
    
    
    
    
    
    noise_removal = cv2.bilateralFilter(img_gray,9,75,75)
    cv2.namedWindow('Noise Removed Image',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Noise Removed Image',800,700)
    cv2.imshow("Noise Removed Image",noise_removal)
    cv2.waitKey(0)
    cv2.destroyWindow('Noise Removed Image')
    # Display Image
    #cv2.waitKey(0)
    # Histogram equalisation for better results
    equal_histogram = cv2.equalizeHist(noise_removal)
    #cv2.imshow("After Histogram equalisation",equal_histogram)
    # Display Image0
    
    #cv2.waitKey(0)
    # Morphological opening with a rectangular structure element
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
    morph_image = cv2.morphologyEx(equal_histogram,cv2.MORPH_OPEN,kernel,iterations=15)
    #cv2.imshow("Morphological opening",morph_image)
    # Display Image
    #cv2.waitKey(0)
    # Image subtraction(Subtracting the Morphed image from the histogram equalised Image)
    sub_morp_image = cv2.subtract(equal_histogram,morph_image)
    #cv2.imshow("Subtraction image", sub_morp_image)
    # Display Image
    #cv2.waitKey(0)
    
    # Thresholding the image
    ret,thresh_image = cv2.threshold(sub_morp_image,0,255,cv2.THRESH_OTSU)
    #cv2.imwrite("binary.jpg",thresh_image)
    cv2.namedWindow('Image after Thresholding',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Image after Thresholding',800,700)
    cv2.imshow("Image after Thresholding",thresh_image)
    cv2.waitKey(0)
    cv2.destroyWindow('Image after Thresholding')
    # Display Image
    #cv2.waitKey(0)
    # Applying Canny Edge detection
    sigma=0.33
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    canny_image= cv2.Canny(thresh_image, lower, upper)
    #canny_image = cv2.Canny(thresh_image,200,255)
    cv2.namedWindow('Image after applying Canny edge detection',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Image after applying Canny edge detection',800,700)
    cv2.imshow('Image after applying Canny edge detection',canny_image)
    cv2.waitKey(0)
    cv2.destroyWindow('Image after applying Canny edge detection')
    # Display Image
    #cv2.waitKey(0)
    canny_image = cv2.convertScaleAbs(canny_image)
    
    # dilation to strengthen the edges
    kernel = np.ones((3,3), np.uint8)
    # Creating the kernel for dilation
    dilated_image = cv2.dilate(canny_image,kernel,iterations=1)
    #cv2.imshow("Dilation", dilated_image)
    # Displaying Image
    #cv2.waitKey(0)
    # Finding Contours in the image based on edges
    new,contours, hierarchy = cv2.findContours(dilated_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.namedWindow('All contours',cv2.WINDOW_NORMAL)
    #cv2.resizeWindow('All contours',800,700)
    #cv2.imshow("All contours",new)
    #cv2.waitKey(0)
    #cv2.destroyWindow('All contours')
    contours= sorted(contours, key = cv2.contourArea, reverse = True)[:8]
    # Sort the contours based on area ,so that the number plate will be in top 8 contours
    allcontours=cv2.drawContours(img,contours,-1,(0,255,0),3)
    cv2.namedWindow('Selected Contours',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Selected Contours',800,700)
    cv2.imshow("Selected Contours",allcontours)
    cv2.waitKey(0)
    cv2.destroyWindow('Selected Contours')
    #cv2.waitKey(0)
    screenCnt = None
    # loop over our contours
    count=0;
    returntext = ''
    for c in contours:
     # approximate the contour
     peri = cv2.arcLength(c, True)
     approx = cv2.approxPolyDP(c, 0.01 * peri, True)  # Approximating with 1% error
     # if our approximated contour has four points, then
     # we can assume that we have found our screen  # Select the contour with 4 corners
     if(len(approx)>=4 and len(approx<=13)):
         count=count+1
         screenCnt = approx
         final = cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 1)
      # Drawing the selected contour on the original image
        # cv2.imshow("Image with Selected Contour",final)
         #cv2.imwrite("contour.jpg",final)
         #cv2.waitKey(0)
         x,y,w,h=cv2.boundingRect(c)
         new_img=img[y:y+h,x:x+w]
         #cv2.imshow("New image",new_img)
         #cv2.waitKey(0)
         newimg_gray = cv2.cvtColor(new_img,cv2.COLOR_RGB2GRAY)
         #cv2.imshow("Gray Converted Image",newimg_gray)
         # Display Image
         #cv2.waitKey(0)
         ret,newimgthresh_image = cv2.threshold(newimg_gray,0,255,cv2.THRESH_OTSU)
        
         #cv2.imshow("Image after Thresholding",newimgthresh_image)
         # Display Image
         #cv2.waitKey(0)
         plate_im = Image.fromarray(newimgthresh_image)
         text = tess.image_to_string(plate_im, lang='eng')
         if(text):
             text1=''
             text1=text1.join(e for e in text if e.isalnum())
             if(len(text1)>4):
               
                 cv2.imshow("Number plate",newimgthresh_image)
                 #cv2.waitKey(0)
                 #cv2.destroyWindow('Number plate')
                 if(text1[:1]=="M"):
                     print("Detected number plate: ",text1[:10])
                     returntext=text1[:10]
                 else:
                    print("Detected number plate: ",text1[:8])
                    returntext=text1[:8]
                 
                 #print(count)
    #print(count)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    return returntext

#import cv2
#text=numberplatedetection(img)