from time import time
from fnc.extractFeature import extractFeature
from fnc.matching import matching
from picamera import PiCamera
from time import sleep
from PIL import Image

start = time()

temp_dir = "templates/temp/"
thres = 0.38
camera = PiCamera()
camera.start_preview()

for i in range(5):
    sleep(1)
    capture_path = 'captures/image%s.jpg' % i
    camera.capture(capture_path)

    image = Image.open(capture_path)
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
        cropped_image.save(capture_path)
        
    template, mask, file = extractFeature(capture_path)
    result = matching(template, mask, temp_dir, thres)
    
    if result == -1:
        print('>>> No registered sample.')
        break;

    elif result == 0 and i == 4:
        print('>>> No sample matched.')
        break;

    elif result != 0:
        print('>>> {} samples matched (descending reliability):'.format(len(result[0])))
        for res in result:
            print("\t", res[0], '-->', res[1])
        break;

camera.stop_preview()
end = time()
print('\n>>> Verification time: {} [s]\n'.format(end - start))