"""
"""
import os
import cv2
from tesserocr import PyTessBaseAPI
from timeit import default_timer as timer

def ocr(img_path):
    with PyTessBaseAPI() as api:
        api.SetImageFile(img_path)
        print(api.GetUTF8Text())
        print(api.AllWordConfidences())
    return True

def main():
    start = timer()
    
    img_path = 'images/num.png'

    ## How many times to repeat single item
    repeat = 30

    image_list = [img_path] * repeat

    ## run multiple times
    for i in image_list:
        ocr(img_path)

    print(f"Elapsed time: {timer() - start}")


if __name__ == "__main__":
    main()