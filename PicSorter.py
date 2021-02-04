from PIL import Image
import os

baseDir = '/data/'
fileDir = '/photos/iphone/'

for entry in os.scandir(baseDir + fileDir):
    if (entry.path.endswith(".MOV")):
        print("skipping:  %s" % entry.path)
    elif (entry.path.endswith(".PNG")):
        print("skipping:  %s" % entry.path)
    elif (entry.path.endswith(".ini")):
        print("skipping:  %s" % entry.path)
    elif (entry.path.endswith(".AAE")):
        print("skipping:  %s" % entry.path)
    else:
        print("testing:  %s" % entry.path)
        photo = Image.open(entry.path)
        pDateTime = photo.getexif()[36867]
        pDate = pDateTime.split(' ')[0].split(':')
        yearDir = pDate[0]
        monthDir = pDate[1] + '-' + pDate[2]
        print("%s %s %s" % (yearDir, monthDir, entry.path))
