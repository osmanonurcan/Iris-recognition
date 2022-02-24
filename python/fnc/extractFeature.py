##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
from cv2 import imread
import cv2
from fnc.segment import segment
from fnc.normalize import normalize
from fnc.encode import encode
from PIL import Image

##-----------------------------------------------------------------------------
##  Parameters for extracting feature
##	(The following parameters are default for CASIA1 dataset)
##-----------------------------------------------------------------------------
# Segmentation parameters
eyelashes_thres = 80

# Normalisation parameters
radial_res = 20
angular_res = 240

# Feature encoding parameters
minWaveLength = 18
mult = 1
sigmaOnf = 0.5


##-----------------------------------------------------------------------------
##  Function
##-----------------------------------------------------------------------------
def extractFeature(im_filename, eyelashes_thres=80, use_multiprocess=True):
	"""
	Description:
		Extract features from an iris image

	Input:
		im_filename			- The input iris image
		use_multiprocess	- Use multiprocess to run

	Output:
		template			- The extracted template
		mask				- The extracted mask
		im_filename			- The input iris image
	"""
	# Perform segmentation
	im = imread(im_filename, 0)
	ciriris, cirpupil, imwithnoise = segment(im, eyelashes_thres, use_multiprocess)
	
	
	#cv2.imshow("a", imwithnoise)
	
    
	# Perform normalization
	polar_array, noise_array = normalize(imwithnoise, ciriris[1], ciriris[0], ciriris[2],
										 cirpupil[1], cirpupil[0], cirpupil[2],
										 radial_res, angular_res)
	#noise_array = noise_array.astype(float)
	
	cv2.imwrite('polar.jpg', polar_array*255)
	cv2.imwrite('noise.jpg', noise_array.astype(float)*255)
	polar = cv2.imread('polar.jpg')
	noise = cv2.imread('noise.jpg')
	polar = cv2.resize(polar, (polar.shape[1]*5,polar.shape[0]*5))
	noise = cv2.resize(noise, (noise.shape[1]*5,noise.shape[0]*5))
	cv2.imwrite('polar.jpg', polar)
	cv2.imwrite('noise.jpg', noise)
	#cv2.imshow("polar", polar_array)
	#cv2.imshow("noise", noise_array.astype(float))

	# Perform feature encoding
	template, mask = encode(polar_array, noise_array, minWaveLength, mult, sigmaOnf)
	#cv2.imshow('a',template)
	#cv2.imshow('b',mask)
	cv2.imwrite('polar_encode.jpg', template*255)
	cv2.imwrite('noise_encode.jpg', mask.astype(float)*255)
	polar_encode = cv2.imread('polar_encode.jpg')
	noise_encode = cv2.imread('noise_encode.jpg')
	polar_encode = cv2.resize(polar_encode, (polar_encode.shape[1]*5,polar_encode.shape[0]*5))
	noise_encode = cv2.resize(noise_encode, (noise_encode.shape[1]*5,noise_encode.shape[0]*5))
	cv2.imwrite('polar_encode.jpg', polar_encode)
	cv2.imwrite('noise_encode.jpg', noise_encode)
	#cv2.waitKey(0)
	
    
    
	# Return
	return template, mask, im_filename