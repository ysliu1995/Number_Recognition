#coding:utf-8
import os
import sys, getopt
from shot import Screenshot
from recognition import Recognition

def main():

    path = sys.argv[1]
    time_shot = int(sys.argv[2])
    category = ['CO2', 'temperature', 'PM10', 'PM2.5']

    for dir in ['crop','output']:
        if not os.path.isdir(dir):
            os.mkdir(dir)
    for dir in category:
        if not os.path.isdir('crop/{}'.format(dir)):
            os.mkdir('crop/{}'.format(dir))

    s = Screenshot(path, time_shot)
    r = Recognition()
    
    #截圖
    print('Start screenshot')
    for c in category:
        s.shot(c)
    print('End')

    # #辨識
    print('Start recognition')
    for c in category:
        r.recognition_digit(c)
    print('End')

if __name__ == '__main__':
    main()