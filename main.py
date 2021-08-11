import os
import shutil
import zipfile
import time

from PIL import Image

from libs import clock_image

input_folder = "input"
extracted_folder = f"{input_folder}/bootanimation"
bootanimation_zip_path = f"{input_folder}/bootanimation.zip"

output_folder = "output"
output_bootanimation_zip_path = f"{output_folder}/bootanimation.zip"
output_bootanimation_preview = f"{output_folder}/preview.gif"


allImages = []

def extract_zip():
    if not os.path.exists(bootanimation_zip_path):
        print(f"{bootanimation_zip_path} not found!")
        print('GoodBye!!')
        exit()

    zip_file = zipfile.ZipFile(bootanimation_zip_path, 'r')
    zip_file.extractall(extracted_folder)
    zip_file.close()

def create_zip():
    zipf = zipfile.ZipFile(output_bootanimation_zip_path, 'w', zipfile.ZIP_STORED)

    if not os.path.exists(f"{extracted_folder}/desc.txt"):
        print("desc.txt file not found")
        os.remove(output_bootanimation_zip_path)
        exit()

    zipf.write(f"{extracted_folder}/desc.txt", arcname="desc.txt" )
    with open(f"{extracted_folder}/desc.txt") as descFile:
        descData = descFile.readlines()
    for data in descData[1:]:
        temp = data.split(" ")
        if len(temp) < 4:
            continue
        temp[3] = temp[3].strip("\n")
        images = os.listdir(f"{extracted_folder}/{temp[3]}")
        for image in images:
            zipf.write(f"{extracted_folder}/{temp[3]}/{image}", arcname=f"{temp[3]}/{image}")
    
    zipf.close()
    print("output/bootanimation.zip created\n")

def getColor(color):
    return (int(color[1:3], 16), int(
        color[3:5], 16), int(color[5:7], 16))


def createAndWriteImage(count, pathOfImage, data, trimdata):
    if len(trimdata) > count:
        if(lengthOfData > 4):
            bgColor = getColor(data[4])
        else:
            bgColor = getColor("#000000")

        # Create a new background according to dimensions and color
        toSave = Image.new('RGB', (width, height), bgColor)

        # Extract trim data from trim.txt
        position = [int(i) for i in trimdata[count].split("+")[1:]]
        dimensions = [int(i) for i in trimdata[count].split("+")[0].split("x")]

        # Open the frame Image and resize it according to data
        imgg = Image.open(pathOfImage).resize(dimensions)

        # Paste image onto the background
        toSave.paste(imgg, box=position)
        imgg.close()

    else:
        if(lengthOfData > 4):
            bgColor = getColor(data[4])
        else:
            bgColor = getColor("#000000")
        toSave: Image.Image = Image.new('RGB', (width, height), bgColor)

        toSaveTemp = Image.open(pathOfImage)

        toSave.paste(toSaveTemp, box=(
            int(width/2 - toSaveTemp.width/2), int(height/2 - toSaveTemp.height/2)))
        toSaveTemp.close()

    if len(data) > 5:
        if "clock_font.png" in os.listdir(extracted_folder):
            clockImg = clock_image.createMainImage(
                data[5:], width, height, extracted_folder)
            toSave.paste(clockImg, mask=clockImg)

    allImages.append(toSave.copy())
    toSave.close()
    # try:
    #     anim = Image.open(output_folder
    # + "bootanimation.gif")
    #     anim.save(output_folder
    # + "bootanimation.gif", format="GIF", append_images=toSave)
    # except FileNotFoundError:
    #     toSave.save(output_folder
    # + "bootanimation.gif", format="GIF")


if os.path.exists(f"{extracted_folder}/desc.txt"):
    if input("already extracted files found. Use them?(Y/N): ").lower() == 'n':
        shutil.rmtree(extracted_folder)
        extract_zip()
else:
    extract_zip()

with open(f"{extracted_folder}/desc.txt") as f:
    desc_data = f.readlines()

details = desc_data[0]
width, height, fps = [int(i) for i in details.strip().split(" ")]

print("\nWidth: ", width)
print("Height: ", height)
print("FPS: ", fps)

for oneLine in desc_data[1:]:
    data = oneLine.split(" ")
    lengthOfData = len(data)
    if lengthOfData < 4:
        print("Error in desc file. Refer to official documentation")
        print(f"[ERROR]: {data}")
    print("\nProcessing", data[3])
    data[lengthOfData - 1] = data[lengthOfData - 1].strip("\n")
    print("Type:", data[0])
    if (data[1] == '0'):
        data[1] = '3'
        print("Repeat Times: 0 (Changed to 3 for Preview)")
    else:
        print("Repeat Times:", data[1])

    print("Delay After End:", data[2], "Frames")
    if len(data) > 4:
        print("Background Color:", data[4])
    else:
        print("Background Color: Not Found (Using Default: Black)")

    images = sorted(os.listdir(f"{extracted_folder}/{data[3]}"))

    print(f"{len(images) - images.count('trim.txt')} image(s) found")
    # print(images)
    for i in range(int(data[1])):
        if images.count("trim.txt") != 0:
            images.remove("trim.txt")
            with open(f"{extracted_folder}/{data[3]}/trim.txt") as trimFile:
                trimdata = trimFile.readlines()
        else:
            trimdata = []
        for counter in range(len(images)):
            print(f"Processing Image {counter}        ", end="\r")
            imgpth = f"{extracted_folder}/{data[3]}/{images[counter]}"
            if counter == len(images) - 1:
                for num in range(int(data[2])):
                    createAndWriteImage(counter, imgpth, data, trimdata)

            createAndWriteImage(counter, imgpth, data, trimdata)
    print("                                         ", end="")

# for im in allImages[-4:-1]:
#     im.show()

print(f"\nCreating {output_bootanimation_preview}")

allImages[0].save(output_bootanimation_preview,
                  save_all = True,
                  optimize=False,
                  append_images = allImages[1:],
                  duration = 1000/fps)
                #   loop = 0)

c = ''
while True:
    c = input("\nCreate bootanimation.zip?(Y/N): ")[0].lower()
    if c in ['n', 'y']:
        break
if c == 'y':
    create_zip()

