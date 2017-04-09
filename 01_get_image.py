import requests

def Download_Pic(strPath, strName):
        # choose the appointed site to get verification code picture
	"""url = '*********************************************'"""
	# send a get request in the form of binary stream
	# set stream=True , before read the data continuously
	rReq = requests.get(url, stream=True)
	# save the picture data
	with open(strPath+strName+'.png','wb') as fpPIC:
		# a 1024 byte read content to byChunk
		# before read the data cycle
		for byChunk in rReq.iter_content(chunk_size=1024):
			if byChunk:
				fpPIC.write(byChunk)
				fpPIC.flush()
		# close the pic-file
		fpPIC.close()

for i in range(1, 100+1):
	strFileName = '%03d'%i
	# set the local file catalog to store the picture
	Download_Pic('***The local file catalog to store the image***',strFileName)
