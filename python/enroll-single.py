##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
import argparse, os
from time import time
from scipy.io import savemat
import numpy as np
from fnc.extractFeature import extractFeature
import cv2
from PIL import Image



#------------------------------------------------------------------------------
#	Argument parsing
#------------------------------------------------------------------------------
parser = argparse.ArgumentParser()

parser.add_argument("--file", type=str,
                    help="Path to the file that you want to verify.")

parser.add_argument("--temp_dir", type=str, default="./templates/temp/",
					help="Path to the directory containing templates.")

args = parser.parse_args()


##-----------------------------------------------------------------------------
##  Execution
##-----------------------------------------------------------------------------
start = time()

#image resize
image = Image.open(args.file)
size = image.size

if(size[1]!=280):
    gray = image.convert('L')
    oran = size[0]/size[1]
    img_h = 280
    img_w = int(280*oran)
    new_image = gray.resize((img_w,img_h))
    t = int((img_w-320)/2)
    box = (t,0,img_w-t,280)
    cropped_image = new_image.crop(box)
    cropped_image.save(args.file)
'''
if(size[0]!=320):
    oran = size[0]/size[1]
    new_image = image.resize((320,int(320/oran)))
    new_image.save(args.file)
'''



#args.file = "../CASIA1/001_1_1.jpg"

# Extract feature
print('>>> Enroll for the file ', args.file)
template, mask, file = extractFeature(args.file)
#print(template.shape)
#print(mask.shape)



# Save extracted feature
basename = os.path.basename(file)
out_file = os.path.join(args.temp_dir, "%s.mat" % (basename))
print(out_file)
mdict={'template':template, 'mask':mask}
savemat(out_file, mdict)
print('>>> Template is saved in %s' % (out_file))
cv2.imshow('aaa',template)
#save as txt
'''
out_file_template = os.path.join(args.temp_dir, "{}_tempate.txt".format(basename))
out_file_mask = os.path.join(args.temp_dir, "{}_mask.txt".format(basename))
np.savetxt(out_file_template, template)
np.savetxt(out_file_mask, mask)
'''


end = time()
print('>>> Enrollment time: {} [s]\n'.format(end-start))