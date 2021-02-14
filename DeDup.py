# USAGE
# python detect_and_remove.py --dataset dataset
# python detect_and_remove.py --dataset dataset --remove 1

from imutils import paths
import numpy as np
# import argparse
import cv2
import os
import shutil

imagePaths = "/gras-data/photos/"
# imagePaths = "/gras-data/photos/To_be_sorted/misc/"
deletePath = "/gras-data/photos-deleted/"


def dhash(image, hashSize=8):
    # convert the image to grayscale and resize the grayscale image,
    # adding a single column (width) so we can compute the horizontal
    # gradient
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (hashSize + 1, hashSize))

    # compute the (relative) horizontal gradient between adjacent
    # column pixels
    diff = resized[:, 1:] > resized[:, :-1]

    # convert the difference image to a hash and return it
    return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

"""
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required=True,
                help="path to input dataset")
ap.add_argument("-r", "--remove", type=int, default=-1,
                help="whether or not duplicates should be removed (i.e., dry run)")
args = vars(ap.parse_args())
"""
# grab the paths to all images in our input dataset directory and
# then initialize our hashes dictionary
print("[INFO] computing image hashes...")
# imagePaths = list(paths.list_images(args["dataset"]))

imagePaths = list(paths.list_images(imagePaths))
hashes = {}

# loop over our image paths
for imagePath in imagePaths:
    print(imagePath)
    if os.stat(imagePath).st_size == 0:
        os.remove(imagePath)
    # load the input image and compute the hash
    image = cv2.imread(imagePath)
    h = dhash(image)

    # grab all image paths with that hash, add the current image
    # path to it, and store the list back in the hashes dictionary
    p = hashes.get(h, [])
    p.append(imagePath)
    hashes[h] = p

# loop over the image hashes
print(" %d Images found." % (len(hashes)))
for (h, hashedPaths) in hashes.items():
    # check to see if there is more than one image with the same hash
    if len(hashedPaths) > 1:
        # loop over all image paths with the same hash
        dups = []
        for p in hashedPaths:
            dups.append(p)
        while len(dups) > 1:
            print("Which one to delete? (x means skip, q means Quit)")
            # initialize a montage to store all images with the same hash
            montage = None
            for i, p in enumerate(dups):
                print(" %d : %s" % (i, p))
                # load the input image and resize it to a fixed width
                # and height
                image = cv2.imread(p)
                image = cv2.resize(image, (150, 150))

                # if our montage is None, initialize it
                if montage is None:
                    montage = image

                # otherwise, horizontally stack the images
                else:
                    montage = np.hstack([montage, image])
            # show the montage for the hash
            # print("[INFO] hash: {}".format(h))
            cv2.imshow("Montage", montage)
            c = cv2.waitKey(0) % 256
            if c == ord('x'):
                print("Skipping...")
                break
            if c == ord('q'):
                print("Quitting...")
                exit('1')
            try:
                num = int(chr(c))
                if num >= len(dups):
                    raise ValueError

                print("moving: %s" % dups[num])
                basename = os.path.basename(dups[num])
                delName = deletePath + basename
                # print(delName)
                shutil.move(dups[num], delName)
                dups.remove(dups[num])
            except ValueError:
                print("you pressed %s, which is invalid" % chr(c))
