import os
import cv2
import csv
import numpy as np


class Recognition:

    # def __init__(self)
#----------------------------------------------------------------------------

    def GetData(self, category):
        if category == 'CO2':
            with np.load('data/CO2_data.npz') as data:
                train = data['train']
                train_labels = data['train_labels']
        elif category == 'temperature':
            with np.load('data/temperature_data.npz') as data:
                train = data['train']
                train_labels = data['train_labels']
        else:
            with np.load('data/PM_data.npz') as data:
                train = data['train']
                train_labels = data['train_labels']
        return train, train_labels

    def Predict(self, test, category):
        train, train_labels = self.GetData(category)
        knn = cv2.ml.KNearest_create()
        knn.train(train, cv2.ml.ROW_SAMPLE, train_labels)
        ret,result,neighbours,dist = knn.findNearest(test,k=5)
        return ret

    #----------------------------------------------------------------------------

    def ReadImage(self, imagePath):
        image = cv2.imread(imagePath,cv2.IMREAD_GRAYSCALE)
        image = cv2.resize(image,(20,20),interpolation = cv2.INTER_AREA)
        return image

    def ImageThreshold(self, image):
        ret,image = cv2.threshold(image,50,255,cv2.THRESH_BINARY_INV)
        return image

    def ImageZeroAndOne(self, image):
        for i in range(20):
            for j in range(20):
                if image[i,j] == 255:
                    image[i,j] = 0
                else:
                    image[i,j] = 1
        return image

    #-----------------------------------------------------------------------------

    def split(self, img_thre, category):
        white = []  
        black = []  
        height = img_thre.shape[0]
        width = img_thre.shape[1]
        white_max = 0
        black_max = 0

        for i in range(width):
            s = 0  
            t = 0  
            for j in range(height):
                if img_thre[j][i] == 255:
                    s += 1
                if img_thre[j][i] == 0:
                    t += 1
            white_max = max(white_max, s)
            black_max = max(black_max, t)
            white.append(s)
            black.append(t)

        arg = False 
        if black_max > white_max:
            arg = True

        def find_end(start_):
            end_ = start_+1
            for m in range(start_+1, width-1):
                if (black[m] if arg else white[m]) > (.95 * black_max if arg else .95 * white_max): 
                    end_ = m
                    break
            return end_

        n = 1
        start = 1
        end = 2
        ans = ''
        while n < width-2:
            n += 1
            if (white[n] if arg else black[n]) > (.05 * white_max if arg else .05 * black_max):
                start = n
                end = find_end(start)
                n = end
                if end-start > 5:
                    c = img_thre[1:height, start:end]
                    c = cv2.resize(c,(20,20),interpolation = cv2.INTER_AREA)
                    a = self.ImageThreshold(c)
                    # b = ImageZeroAndOne(a)
                    img_fla = a.reshape(-1,400).astype(np.float32)
                    s = self.Predict(img_fla, category)
                    if str(int(s)) == '10':
                        ans += '.'
                    else:
                        ans += str(int(s))
        
        return ans

    #---------------------------------------------------------------------------------------

    def GetFileName(self, dir):
        all_file = os.listdir(dir)
        s = sorted([int(f.strip('.jpg')) for f in all_file])
        return s

    #----------------------------------------------------------------------------------------

    def recognition_digit(self, category):
        ans = []

        s = self.GetFileName('crop/{}/'.format(category))
        for i in s:
            img_gray = cv2.imread('crop/{}/{}.jpg'.format(category,i), cv2.IMREAD_GRAYSCALE)
            ret, img_thre = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)
            ans.append(self.split(img_thre, category))
        print(ans)
        with open('output/{}.csv'.format(category),'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(ans)