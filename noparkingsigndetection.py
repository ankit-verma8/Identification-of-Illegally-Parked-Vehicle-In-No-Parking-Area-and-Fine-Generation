def noparkingsigndetection(testImgBGR):
    import cv2

    MIN_MATCH_COUNT = 30

    detector = cv2.xfeatures2d.SIFT_create()
    FLANN_INDEX_KDTREE = 0
    flannParam = dict(algorithm=FLANN_INDEX_KDTREE, tree=5)
    flann = cv2.FlannBasedMatcher(flannParam, {})

    trainImg = cv2.imread('trainimage.jpg')
    cv2.imshow("Training Image",trainImg)
    cv2.waitKey(0)
    cv2.destroyWindow("Training Image")
    trainKP, trainDesc = detector.detectAndCompute(trainImg, None)

    #cv2.imshow("original image", testImgBGR)
    testImg = cv2.cvtColor(testImgBGR, cv2.COLOR_BGR2GRAY)
    testKP, testDesc = detector.detectAndCompute(testImg, None)
    matches = flann.knnMatch(testDesc, trainDesc, k=2)

    goodMatch = []
    for m, n in matches:
        if (m.distance < 0.66 * n.distance):
            goodMatch.append(m)

    if (len(goodMatch) > MIN_MATCH_COUNT):
        # print("NO PARKING sign detected")
        return True

    else:
        # print("Not Enough Matches : %d/%d"%(len(goodMatch),MIN_MATCH_COUNT))
        return False

    #cv2.waitKey(0)
    #cv2.destroyAllWindows()










