from PIL import Image
import os
import shutil

base_dir = "/data"
src_dir = "/data/photos/To_be_sorted"
dest_dir = "/data/photos"
# Walk through all files in the directory that contains the files to copy
for root, dirs, files in os.walk(src_dir):
    for filename in files:
        print('')
        old_name = os.path.join(os.path.abspath(root), filename)
        print(old_name)
        # Separate base from extension
        base, extension = os.path.splitext(filename)
        # print(base, extension)
        if extension.lower() == ".jpg":
            photo = Image.open(old_name)
            pDateTime = photo.getexif()[36867]
            pDate = pDateTime.split(' ')[0].split(':')
            yearDir = pDate[0]
            monthDir = pDate[1] + '-' + pDate[2]
            print("%s %s %s" % (yearDir, monthDir, pDateTime))
        else:
            print('Skipping %s' % old_name)
            continue
        # Initial new name
        new_dir = os.path.join(dest_dir, yearDir, monthDir)
        # print(new_dir)
        os.makedirs(new_dir, exist_ok=True)
        new_name = os.path.join(new_dir, base + extension)
        if not os.path.exists(os.path.join(new_dir)):
            print(os.path.join(new_dir), "not found")
            assert new_dir is False
        elif not os.path.exists(new_name):  # folder exists, file does not
            print("Copied ", old_name, " as ", new_name)
            shutil.copy(old_name, new_name)
        else:  # folder exists, file exists as well
            ii = 1
            while True:
                new_name = os.path.join(new_dir, base + "_" + str(ii) + extension)
                if not os.path.exists(new_name):
                    shutil.copy(old_name, new_name)
                    print("Copied ", old_name, " AS ", new_name)
                    break
                ii += 1
