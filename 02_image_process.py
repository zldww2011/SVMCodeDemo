import os
import os.path
import random
from PIL import Image, ImageEnhance, ImageFilter

def BinaryzationImg(strImgPath):
	imgOriImg = Image.open(strImgPath)
	pocEnhance = ImageEnhance.Contrast(imgOriImg)	# Enhance contrast
	imgOriImg = pocEnhance.enhance(2.0)		# enhance contrast 200%
	pocEnhance = ImageEnhance.Sharpness(imgOriImg)	# Enhance Sharpness
	imgOriImg = pocEnhance.enhance(2.0)		# enhance sharpness 200%
	pocEnhance = ImageEnhance.Brightness(imgOriImg)	# Enhance Brightness
	imgOriImg = pocEnhance.enhance(2.0)		# enhance brightness 200%
	# filter image effect
	imgGryImg = imgOriImg.convert('L').filter(ImageFilter.DETAIL) 
	imgBinImg = imgGryImg.convert('1')	# convert to bin file
	return imgBinImg

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
				    and imgBinImg.getpixel(( x	 ,(y+1)))==255 \
				    and imgBinImg.getpixel(( x	 ,(y-1)))==255:
				imgBinImg.putpixel([x,y],255)
	return imgBinImg

def GetCropImgs(imgClrImg):
	ImgList = []
	for i in range(4):
		x = 6 + i*13
		y = 3
		SubImg = imgClrImg.crop((x, y, x+13, y+17))
		ImgList.append(SubImg)
	return ImgList

g_Count = 0
# this file catalog use to store the source verification code Image
strStep1Dir = '*****************************************************'
# this file catalog use to store image after processing
strStep2Dir = '****************************************'
for ParentPath, DirNames, FileNames in os.walk(strStep1Dir):
	# travesal all the picture file
	for i in FileNames:
		strFullPath = os.path.join(ParentPath,i)	# picture file path info
		imgBinImg = BinaryzationImg(strFullPath)	# binarization processing
		imgClrImg = ClearNoise(imgBinImg)			# remove grain
		ImgList = GetCropImgs(imgClrImg)			# image segmentation
		for img in ImgList:
			strImgName = '%04d%04d.png'%(g_Count, random.randint(0,9999))
			strImgPath = os.path.join(strStep2Dir,strImgName)
			img.save(strImgPath)
			g_Count += 1
	
