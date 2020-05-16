import os
import zipfile

def zipdir(path, ziph):
    try:
        ziph.write(path + "desc.txt", arcname="desc.txt" )
        with open(path + "desc.txt") as descFile:
            descFile.readline()
            for data in descFile.readlines():
                temp = data.split(" ")
                if len(temp) < 4:
                    continue
                temp[3] = temp[3].strip("\n")
                images = os.listdir(path + temp[3])
                for image in images:
                    zipf.write(path + temp[3] + "/" + image, temp[3] + "/" + image)
    except FileNotFoundError:
        print("desc.txt not Found!")
        print("Closing Program")
        zipf.close()
        os.remove("output/bootanimation.zip")
        exit()


if __name__ == '__main__':
    zipf = zipfile.ZipFile('output/bootanimation.zip', 'w', zipfile.ZIP_STORED)
    zipdir('input/bootanimation/', zipf)
    zipf.close()
    print("\nbootanimation.zip created in output/\n")