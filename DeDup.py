# USAGE
# python detect_and_remove.py --dataset dataset
# python detect_and_remove.py --dataset dataset --remove 1
from copy import copy

from imutils import paths
import numpy as np
import argparse
import cv2
import os
import shutil


def read_args():
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input",
                    default="/gras-data/photos/",
                    help="input path for images (default: gras-data/photos/)")
    ap.add_argument("-o", "--output",
                    default="/gras-data/photos-deleted/",
                    help="output path to place duplicate images (default: /gras-data/photos-deleted/)")
    return vars(ap.parse_args())


def dhash(image, hash_size=8):
    # convert the image to grayscale and resize the grayscale image,
    # adding a single column (width) so we can compute the horizontal gradient
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (hash_size + 1, hash_size))
    # compute the (relative) horizontal gradient between adjacent column pixels
    diff = resized[:, 1:] > resized[:, :-1]
    # convert the difference image to a hash and return it
    return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])


def get_hashes():
    # grab the paths to all images in our input dataset directory
    print("[INFO] computing image hashes...")
    image_paths = list(paths.list_images(args['input']))

    hashes = {}
    for imagePath in image_paths:
        if '.Thumbnails' in imagePath:
            continue
        if os.stat(imagePath).st_size == 0:
            os.remove(imagePath)
        # load the input image and compute the hash
        print(imagePath)
        image = cv2.imread(imagePath)
        h = dhash(image)
        # grab all image paths with that hash, add the current image path to it,
        # and store the list back in the hashes dictionary
        p = hashes.get(h, [])
        p.append(imagePath)
        hashes[h] = p
    return hashes


def auto_check(dups_in):
    num = 1    # figure out how to check for sizes
    dups_out = remove_dups(num, dups_in)
    return dups_out


def find_dups(hashes):
    # loop over the image hashes
    print(" %d Images found." % (len(hashes)))
    for (h, hashedPaths) in hashes.items():
        # check to see if there is more than one image with the same hash
        if len(hashedPaths) > 1:
            # loop over all image paths with the same hash
            dups = []
            for p in hashedPaths:
                dups.append(p)
            # handle the easy cases
            dups = auto_check(dups)
            # send the other cases to the user
            while len(dups) > 1:
                c = display_dups(dups)
                dups = check_response(c, dups)


def display_dups(dups):
    print("Which one to delete? (x means skip, a means delete all, q means Quit)")
    # initialize a montage to store all images with the same hash
    montage = None
    for i, p in enumerate(dups):
        print(" %d : %s" % (i, p))
        image = cv2.imread(p)
        image = cv2.resize(image, (250, 250))

        if montage is None:
            montage = image
        else:
            montage = np.hstack([montage, image])

    cv2.imshow("Montage", montage)
    # get the user's response
    c = cv2.waitKey(0) % 256
    return c


def check_response(c, dups):
    if c == ord('x'):
        print("Skipping...")
        return []
    if c == ord('q'):
        print("Quitting...")
        exit('1')
    if c == ord('a'):
        for i, _ in enumerate(dups):
            remove_dups(i, dups)
        return []
    try:
        num = int(chr(c))
        if num >= len(dups):
            raise ValueError
        dups = remove_dups(num, dups)
    except ValueError:
        print("you pressed %s, which is invalid" % chr(c))
    return dups


def remove_dups(num, dups):
    print("removing: %s" % dups[num])
    input_path = args['input']
    delete_path = args['output']
    # print(input_path)
    # print(dups[num])
    # print(num)
    basename = str(dups[num]).split(input_path)[1]
    delName = delete_path + basename
    os.makedirs(os.path.dirname(delName), exist_ok=True)
    shutil.move(dups[num], delName)
    result = copy(dups)
    result.remove(dups[num])
    return result


if __name__ == '__main__':
    args = read_args()
    hash_list = get_hashes()
    find_dups(hash_list)

