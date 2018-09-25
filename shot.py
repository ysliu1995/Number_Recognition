import cv2


# CO2 = crop[290:365,156:331]
# temperature = crop[454:528,185:323]
# PM10 = crop[344:411,653:733]
# PM25 = crop[440:508,657:734]

class Screenshot:

    def __init__(self, path, time_shot):

        self.path = path
        self.time_shot = time_shot
    
    def shot(self, category):
        
        vc = cv2.VideoCapture(self.path) 
        fps = vc.get(cv2.CAP_PROP_FPS)      # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
        frameCount = int(vc.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frameCount/fps

        if vc.isOpened(): 
            rval , frame = vc.read()
        else:
            rval = False
                    
        shot = (int(fps) + 1) * self.time_shot
        c = 1

        while rval:   
            rval, frame = vc.read()
            if c % shot == 0:
                sec = int(c/(fps*self.time_shot))
                if category == 'PM2.5':
                    category_image = frame[440:508,657:734]
                elif category == 'PM10':
                    category_image = frame[344:411,653:733]
                elif category == 'CO2':
                    category_image = frame[290:365,156:331]
                elif category == 'temperature':
                    category_image = frame[454:528,185:323]
                cv2.imwrite('crop/{}/{}.jpg'.format(category,sec),category_image)
            c = c + 1
            cv2.waitKey(1)

        vc.release()