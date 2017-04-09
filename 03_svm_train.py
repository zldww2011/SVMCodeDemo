import os
import os.path
from PIL import Image, ImageEnhance, ImageFilter
from svmutil import *

def GetFeature(imgCropImg, nImgHeight, nImgWidth):
    PixelCountList = []
    # transverse scan picture data
    for y in range(nImgHeight):
        CountX = 0
        for x in range(nImgWidth):
            # if the point is black
            if imgCropImg.getpixel((x, y)) == 0:
                CountX += 1
        PixelCountList.append(CountX)
    # longitudinal scan picture data
    for x in range(nImgWidth):
        CountY = 0
        for y in range(nImgHeight):
            # if the point is black
            if imgCropImg.getpixel((x, y)) == 0:
                CountY += 1
        PixelCountList.append(CountY)
    # return the verification code list
    return PixelCountList

def OutPutVectorData(strID, strMaterialDir, strOutPath):
    for ParentPath, DirNames, FileNames in os.walk(strMaterialDir):
        with open(strOutPath, 'a') as fpFea:
            for fp in FileNames:
                # picture file path info
                strFullPath = os.path.join(ParentPath, fp)
                # open picture
                imgOriImg = Image.open(strFullPath)
                # generate the signature code
                FeatureList = GetFeature(imgOriImg, 14, 13)
                strFeature = strID + ' '
                nCount = 1
                for i in FeatureList:
                    strFeature = '%s%d:%d '%(strFeature,nCount,i)
                    nCount += 1
                fpFea.write(strFeature+'\n')
                fpFea.flush()
        fpFea.close()

def TrainSvmModel(strProblemPath, strModelPath):
    Y, X = svm_read_problem(strProblemPath)
    Model = svm_train(Y, X)
    svm_save_model(strModelPath, Model)

def SvmModelTest(strProblemPath, strModelPath):
    TestY, TestX = svm_read_problem(strProblemPath)
    Model = svm_load_model(strModelPath)
    # p_label is the result of identification
    pLabel, pAcc, pVal = svm_predict(TestY, TestX, Model)
    return pLabel

for i in range(0, 10):
    strID = '%d'% i
    OutPutVectorData(strID, '***The classification of documents after processing***'+strID,
	                 '***To store the vector file after processing***')
for j in range(97, 123):
    OutPutVectorData('%d'%j, '***The classification of documents after processing***'+chr(j),
	                 '***To store the vector file after processing***')
# according to the vector file training robot
TrainSvmModel('***To store the vector file after processing***',
	              '***To store the model file through SVM-Training***')
