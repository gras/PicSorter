from PIL import Image
from shutil import move
import os



def movePhotos(photo_dir):
    mov_cnt = 0
    png_cnt = 0
    ini_cnt = 0
    aae_cnt = 0
    jpg_cnt = 0
    unk_cnt = 0
    for entry in os.scandir(photo_dir):
        e_path = entry.path.lower()
        if e_path.endswith(".mov"):
            mov_cnt += 1
        elif e_path.endswith(".png"):
            png_cnt += 1
        elif e_path.endswith(".ini"):
            ini_cnt += 1
        elif e_path.endswith(".aae"):
            aae_cnt += 1
        elif e_path.endswith(".jpg"):
            jpg_cnt += 1
            movePhoto(entry.path)
        else:
            unk_cnt += 1
            print("UNKNOWN:  {}" % e_path)
    print("\nProcessed:  %d jpg files" % jpg_cnt)
    print("Skipped:    %d png files" % png_cnt)
    print("Skipped:    %d mov files" % mov_cnt)
    print("Skipped:    %d ini files" % ini_cnt)
    print("Skipped:    %d aae files" % aae_cnt)
    print("Skipped:    %d unk files" % unk_cnt)


def movePhoto(photo_path):
    photo = Image.open(photo_path)
    pDateTime = photo.getexif()[36867]
    pDate = pDateTime.split(' ')[0].split(':')
    yearDir = pDate[0]
    monthDir = pDate[1] + '-' + pDate[2]
    print("%s %s %s" % (yearDir, monthDir, photo_path))
    # make year directory
    dest_path = baseDir + yearDir

    try:
        os.mkdir(dest_path)
    except OSError:
        pass
    f_name = os.path.basename(photo_path)

    # move(photo_path, dest_path)

# Main routine
baseDir = '/data/'
fileDir = '/photos/iphone/'
movePhotos(baseDir + fileDir)
