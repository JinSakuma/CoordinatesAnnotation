import numpy as np
import cv2


def resize(img, SIZE):
    tmp = img[:, :]
    height, width = img.shape[:2]
    if(height > width):
        size = height
        limit = width
    else:
        size = width
        limit = height
    start = int((size - limit) / 2)
    fin = int((size + limit) / 2)
    new_img = cv2.resize(np.ones((1, 1, 3), np.uint8)*255, (size, size))
    if(size == height):
        new_img[:, start:fin] = tmp
    else:
        new_img[start:fin, :] = tmp

    resized = cv2.resize(new_img, (SIZE, SIZE))
    return resized


def reproduce(h, w, landmarks, SIZE):
    if h > w:
        size = h
        add = (size - w) / 2
    else:
        size = w
        add = (size - h) / 2

    ori_land = landmarks * (size / SIZE)
    if h > w:
        ori_land[0] -= add
    else:
        ori_land[1] -= add

    return ori_land
