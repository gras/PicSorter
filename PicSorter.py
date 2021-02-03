from PIL import Image

baseDir = '/data/'
fileDir = '/photos/testarea/IMG_4994.JPG'
photo = Image.open(baseDir + fileDir)
pDateTime = photo.getexif()[36867]
pDate = pDateTime.split(' ')[0].split(':')
yearDir = pDate[0]
monthDir = pDate[1] + '-' + pDate[2]


print(yearDir)
print(monthDir)
