


from PIL import Image
import zipfile
from os import listdir, rmdir, remove, environ
from os.path import isfile, join, isdir, exists
import cv2 as cv
import numpy as np
import shutil
import glob
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame

input_path = "input/"
extracted_path = input_path + "bootanimation/"
output_path = "output/"
bootanimation_zip_path = input_path + "bootanimation.zip"

try:
    f = open( extracted_path + "desc.txt")
    f.close()
    # print("Existing Extracted Bootanimation Found")
    # if input("Use Existing Files?(y/n)")[0].lower() == 'n':
    #     f.close()
    #     shutil.rmtree(extracted_path)
    #     try:
    #         zip_file = zipfile.ZipFile(input_path + 'bootanimation.zip', 'r')
    #         zip_file.extractall(extracted_path)
    #     except FileNotFoundError:
    #         print('bootanimation.zip not found!!')
    #         print('Exiting Program')
    #         exit()
except FileNotFoundError:
    try:
        zip_file = zipfile.ZipFile(bootanimation_zip_path, 'r')
        zip_file.extractall(extracted_path)
    except FileNotFoundError:
        print(bootanimation_zip_path + ' not found!!')
        print('Exiting Program')
        exit()

descFile = open(extracted_path + 'desc.txt')

details = descFile.readline()
w, h, f = details.split(" ")

width = int(w)
height = int(h)
fps = int(f)

print("\nWidth: ", width)
print("Height: ", height)
print("FPS: ", fps)

out = cv.VideoWriter('.temppreview.avi', cv.VideoWriter_fourcc(
    *'DIVX'), fps, (width, height))


def createAndWriteImage(count, pathOfImage, data, trimdata):
    if len(trimdata) > count:
        if(lengthOfData > 4):
            k = pygame.Color(data[4])
            bgColor = (k[0], k[1], k[2])
            toSave = Image.new('RGB', (width, height), bgColor)
        else:
            toSave = Image.new('RGB', (width, height), (0, 0, 0))
        dimensions = trimdata[count].split("+")
        imgg = Image.open(extracted_path + data[3] + "/" + images[count])
        toSave.paste(imgg, box=(int(dimensions[1]), int(dimensions[2])))
    else:
        toSaveTemp = Image.open(extracted_path + data[3] + "/" + images[count])
        if width != toSaveTemp.width or height != toSaveTemp.height:
            if(lengthOfData > 4):
                k = pygame.Color(data[4])
                bgColor = (k[0], k[1], k[2])
                toSave = Image.new('RGB', (width, height), bgColor)
            else:
                toSave = Image.new('RGB', (width, height), (0, 0, 0))
            toSave.paste(toSaveTemp, box = ((int)(width/2 - toSaveTemp.width/2), (int)(height/2 - toSaveTemp.height/2)))
        else:
            toSave = toSaveTemp
    toSave.save(input_path + ".temp.png", format="PNG")
    outfile = cv.imread(input_path + ".temp.png", cv.IMREAD_COLOR)
    out.write(outfile)


for oneLine in descFile.readlines():
    if(len(oneLine) < 2):
        continue
    data = oneLine.split(" ")
    lengthOfData = len(data)
    data[lengthOfData - 1] = data[lengthOfData - 1].strip("\n")  
    print("\nProcessing", data[3])
    print("Type:", data[0])
    if (data[1] == '0'):
        data[1] = '5'
        print("Repeat Times: 0 (Changed to 5 for Preview Only)")
    else:
        print("Repeat Times:", data[1])
    print("Delay After End:", data[2], "Frames")
    if len(data) > 4:
        print("Background Color:", data[4])
    else:
        print("Background Color: Not Found (Using Default: Black)")
    images = listdir(extracted_path + data[3])
    print(len(images) - images.count("trim.txt"),"image(s) found")
    for i in range(int(data[1])):

        if images.count("trim.txt") != 0:
            images.remove("trim.txt")
            try:
                trimFile = open(extracted_path + data[3] + "/trim.txt")
                trimdata = trimFile.readlines()
                trimFile.close()
            except FileNotFoundError:
                trimdata = []
                print('not found')
        else:
            trimdata = []
        for counter in range(len(images)):
            if counter == len(images) - 1:
                for num in range(int(data[2])):
                    imgpth = extracted_path + data[3] + "/" + images[counter]
                    createAndWriteImage(counter, imgpth, data, trimdata)
            imgpth = extracted_path + data[3] + "/" + images[counter]
            createAndWriteImage(counter, imgpth, data, trimdata)

descFile.close()
remove(input_path + ".temp.png")
out.release()
shutil.move(".temppreview.avi", output_path + "preview.avi")
c = ''
while True:
    c = input("\nDelete extracted files(y/n): ")[0]
    if( c.lower() == 'n' or c.lower() == 'y'):
        break
if c == 'y':
    shutil.rmtree(extracted_path)