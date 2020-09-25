from PIL import Image
from PIL import ImageFilter
from easytello import tello
from langdetect import detect
import time
import pytesseract
import os
import pyautogui
import cv2
import sys

#program to have attach OCR reader to tello camera to create a software that is capable of reacting/following commands that are 
#printed in text

#public variables
pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\Brandon Miller\\AppData\\Local\\Tesseract-OCR\\tesseract.exe'

drone = tello.Tello()

commandList = ['land','fly','up','down','left','right','forward','square','test','stop']
commandListChin = ['落','起','上','下','左','右','前','后','方','验']

#funcs and private variables
def activateStream():

    drone.streamon()
    print('Streaming...')

def deactivateStream():
    drone.streamoff()
    print('Stream Has Ended...')
    False

def activateOCR():

    #first screenshots the default area of the screen that the Tello drone's stream displays on
    sc = pyautogui.screenshot(region=(114,137,958,716))
    os.remove('C:\\Users\\Brandon Miller\\Documents\\Python Scripts\\WB\\raw_image.png')
    sc.save('C:\\Users\\Brandon Miller\\Documents\\Python Scripts\\WB\\raw_image.png')
    
    try:
        #sharpens this screenshot and converts colors to grey to get the clearest image to detect text
        rawImage = Image.open('C:\\Users\\Brandon Miller\\Documents\\Python Scripts\\WB\\raw_image.png')
        rawImage = rawImage.filter(ImageFilter.SHARPEN)
        rawImage = rawImage.filter(ImageFilter.SHARPEN)
        os.remove('C:\\Users\\Brandon Miller\\Documents\\Python Scripts\\WB\\raw_image.png')
        sc.save('C:\\Users\\Brandon Miller\\Documents\\Python Scripts\\WB\\raw_image.png')
        rawImage = cv2.imread('C:\\Users\\Brandon Miller\\Documents\\Python Scripts\\WB\\raw_image.png')
        rawImage = cv2.cvtColor(rawImage,cv2.COLOR_BayerRG2GRAY)
        detectedTextEng = pytesseract.image_to_string(rawImage)
        detectedLangEng = detect(detectedTextEng)
        rawImage.show()
        try:
            #executes if the text displayed is determined to be english
            if detectedLangEng == 'en':
                print('EN Detected')
                commands = detectedTextEng.lower()
                commands = commands.split()
                print(commands)

                for command in commands:
                    if command in commandList:
                        if command == 'land':
                            drone.land()
                        elif command == 'fly':
                            drone.takeoff()
                        elif command == 'up':
                            drone.up(2)
                        elif command == 'down':
                            drone.down(2)
                        elif command == 'right':
                            drone.right(2)
                        elif command == 'left':
                            drone.left(2)
                        elif command == 'forward':
                            drone.forward(1)
                        elif command == 'square':
                            for i in range(4):
                                drone.forward(4)
                                drone.cw(3)
                        elif command == 'test':
                            print('Test Success')
                        elif command == 'stop':
                            deactivateStream()
                        
                        time.sleep(4)
                        break

                    else:
                        pass
            else:
                #if the text is not in english, the program will try to determine if the text is Chinese
                detectedTextChin = pytesseract.image_to_string(rawImage, lang = 'chi_tra')
                detectedLangChin = detect(detectedTextChin)
                if detectedLangChin == 'zh-cn':
                
                    print('CM Detected')

                    try:
                        commands = detectedTextChin.split()
                        print(commands)
                    except:
                        commands = detectedTextChin
                        print(commands)

                    for command in commands:
                        if command in commandListChin:
                            if command == '落':
                                drone.land()
                            elif command == '起':
                                drone.takeoff()
                            elif command == '上':
                                drone.up(2)
                            elif command == '下':
                                drone.down(2)
                            elif command == '右':
                                drone.right(2)
                            elif command == '左':
                                drone.left(2)
                            elif command == '前':
                                drone.forward(1)
                            elif command == '方':
                                for i in range(4):
                                    drone.forward(4)
                                    drone.cw(3)
                            elif command == '验':
                                print('Test Success')
                            else:
                                pass
        except:
            pass

    except:
        pass
    #we use several try/except statements as there are a couple of errors that occur in different situations, so we just
    #have the program continue to run despite these errors

if __name__ == '__main__':
    drone.takeoff()
    activateStream()
    while True:
        time.sleep(3)
        activateOCR()
