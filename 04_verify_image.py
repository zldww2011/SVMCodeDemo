import os
import os.path
from PIL import Image, ImageEnhance, ImageFilter
from svmutil import *

# binary image data
def BinarizationImg(strImgPath):
    # open the image
    imgOriImg = Image.open(strImgPath)
    # enhance contrast to 200%    
    pocEnhance = ImageEnhance.Contrast(imgOriImg)
    imgOriImg = pocEnhance.enhance(2.0)
    # enhance sharpness to 200%
    pocEnhance = ImageEnhance.Sharpness(imgOriImg)
    imgOriImg = pocEnhance.enhance(2.0)
    # enhance brightness to 200%
    pocEnhance = ImageEnhance.Brightness(imgOriImg)
    imgOriImg = pocEnhance.enhance(2.0)
    # filter the image
    imgGryImg = imgOriImg.convert('L').filter(ImageFilter.DETAIL)
    # convert to bin file
    imgBinImg = imgGryImg.convert('1')
    return imgBinImg

# clear noise point
def ClearNoise(imgBinImg):
    for x in range(1, (imgBinImg.size[0]-1)):
        for y in range(1, (imgBinImg.size[1]-1)):
            # if central point is black and all around point is white
            # set the point to white
            if imgBinImg.getpixel((x,y))==0 \
               and imgBinImg.getpixel(((x-1),(y+1)))==255 \
               and imgBinImg.getpixel(((x-1), y   ))==255 \
               and imgBinImg.getpixel(((x-1),(y-1)))==255 \
               and imgBinImg.getpixel(((x+1),(y+1)))==255 \
               and imgBinImg.getpixel(((x+1), y   ))==255 \
               and imgBinImg.getpixel(((x+1),(y-1)))==255 \
               and imgBinImg.getpixel(( x   ,(y+1)))==255 \
               and imgBinImg.getpixel(( x   ,(y-1)))==255:
                imgBinImg.putpixel([x,y],255)
    return imgBinImg

# cut images for four pieces
def GetCropImgs(imgClrImg):
    ImgList = []
    for i in range(4):
        x = 6 + i*13
        y = 3
        SubImg = imgClrImg.crop((x, y, x+13, y+17))
        ImgList.append(SubImg)
    return ImgList

# analysis of the data characteristics of a single picture
def GetFeature(imgCropImg):
    nWidth = 13
    nHeight = 14
    PixelCountList = []
    # horizontal traverse
    for y in range(nHeight):
        CountX = 0
        for x in range(nWidth):
            # determine whether the point is black
            if imgCropImg.getpixel((x, y))==0:
                CountX += 1
        PixelCountList.append(CountX)
    # longitudinal traverse
    for x in range(nWidth):
        CountY = 0
        for y in range(nHeight):
            # determine whether the point is black
            if imgCropImg.getpixel((x, y))==0:
                CountY += 1
        PixelCountList.append(CountY)
    return PixelCountList
    
# with the most similar character signature query
def SvmModelTest(strProblemPath, strModelPath):
    TestY, TestX = svm_read_problem(strProblemPath)
    Model = svm_load_model(strModelPath)
    # pLabel is the result of the identification
    pLabel, pAcc, pVal = svm_predict(TestY, TestX, Model)
    return pLabel

# get the file and analysis process
# set the source and destination path
picDir = '***The local file catalog to store the image***'
modelDir = '***The local file catalog to store model file and tmp-data file***'
for ParentPath, DirNames, FileNames in os.walk(picDir):
    # lterate through all the file
    for fp in FileNames:
        # picture file path info
        strFullPath = os.path.join(ParentPath, fp)
        # binarization the image
        imgBinImg = BinarizationImg(strFullPath)
        # clear the noise point
        imgClrImg = ClearNoise(imgBinImg)
        # show the picture (for test)
        #imgClrImg.show()
        # cut images for four pieces
        imgList = GetCropImgs(imgClrImg)
        # open tmp file to store the vector data
        fpFea = open(modelDir+'tmp.txt','w')
        # every picture processing
        for img in imgList:
            # get the feature code 
            FeatureList = GetFeature(img)
            # generate the standard svm-file 
            # store default vector test label y
            strFeature = '2 '
            nCount = 1
            for i in FeatureList:
                strFeature = '%s%d:%d '%(strFeature, nCount, i)
                nCount += 1
            fpFea.write(strFeature+'\n')
            fpFea.flush()
        fpFea.close()
        # use model file recognize the verification code
        Label = SvmModelTest(modelDir+'tmp.txt',modelDir+'Model.txt')
        # the floating point number into a string
        strName = ''
        for i in Label:
            if int(i) > 9:
                strName += chr(int(i))
            else:
                strName += str(int(i))
        # rename the source file
        # print the predict name (for test)
        # print(strName)
        os.rename(strFullPath,os.path.join(ParentPath, strName+'.png'))
      






            
           
            
            
