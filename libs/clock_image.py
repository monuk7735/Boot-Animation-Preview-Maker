from datetime import datetime
from PIL import Image

def createImage(data, finalTextImage, width, height):
    centerX = False
    centerY = False

    posX = 0
    posY = 0

    if len(data) > 1:
        if data[0] == 'c':
            centerX = True
        else:
            posX = int(data[0])
        if data[1] == 'c':
            centerY = True
        else:
            posY = int(data[1])
    else:
        centerX = True
        if data[0] == 'c':
            centerY = True
        else:
            posY = int(data[0])
    retImage = Image.new("RGBA", (width, height), (0,0,0, 0))
    if centerX:
        posX = int(width/2 - finalTextImage.width/2)
    else:
        if posX < 0:
            posX = width - posX
        else:
            posX
    if centerY:
        posY = int(height/2 - finalTextImage.height/2)
    else:
        if posY < 0:
            posY = -posY
        else:
            posY = height - posY
    retImage.paste(finalTextImage, (posX, posY), mask = finalTextImage)
    return retImage

def createMainImage(data, width, height, clockFontFile):
    currentTime = datetime.now().strftime("%I:%M")

    im = Image.new("RGBA", (400, 300), (0, 0, 0, 250))

    textPng = Image.open(clockFontFile + "clock_font.png").convert("RGBA")

    w, h = textPng.size

    allLightTextImages = []

    for col in range(11):
        colImage = textPng.crop(box = ( (col * (w/16)), (2 * h / 12), (col + 1) * (w / 16), (3 * h / 12)))
        allLightTextImages.append(colImage)

    finalTextImage = Image.new("RGBA", (0, 0), color = (0, 0, 0, 0))

    for i in currentTime:
        if i == ':':
            index = 10
        else:
            index = int(i)
        temp = Image.new("RGBA", (finalTextImage.width + allLightTextImages[index].width, allLightTextImages[index].height), color = (0, 0, 0, 0))
        temp.paste(finalTextImage, (0, 0), mask = finalTextImage)
        temp.paste(allLightTextImages[index], ( temp.width - allLightTextImages[index].width, 0), mask = allLightTextImages[index])
        finalTextImage = temp

    return createImage(data, finalTextImage, width, height)