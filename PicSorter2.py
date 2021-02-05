import os
import shutil


movdir = r"C:\Scans"
basedir = r"C:\Links"
# Walk through all files in the directory that contains the files to copy
for root, dirs, files in os.walk(movdir):
    for filename in files:
        # I use absolute path, case you want to move several dirs.
        old_name = os.path.join( os.path.abspath(root), filename )

        # Separate base from extension
        base, extension = os.path.splitext(filename)

        # Initial new name
        new_name = os.path.join(basedir, base, filename)

        # If folder basedir/base does not exist... You don't want to create it?
        if not os.path.exists(os.path.join(basedir, base)):
            print(os.path.join(basedir,base), "not found")
            continue    # Next filename
        elif not os.path.exists(new_name):  # folder exists, file does not
            shutil.copy(old_name, new_name)
        else:  # folder exists, file exists as well
            ii = 1
            while True:
                new_name = os.path.join(basedir,base, base + "_" + str(ii) + extension)
                if not os.path.exists(new_name):
                   shutil.copy(old_name, new_name)
                   print("Copied", old_name, "as", new_name)
                   break
                ii += 1