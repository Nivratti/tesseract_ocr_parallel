"""
Initialize tesserocr api at global level to speedup 2x-3x
"""
import os
import time
import cv2
from tesserocr import PyTessBaseAPI


api = PyTessBaseAPI()

def ocr(img_path):
    api.SetImageFile(img_path)
    print(api.GetUTF8Text())
    print(api.AllWordConfidences())
    return True

def main():
    start = time.process_time()
    
    img_path = 'images/num.png'

    ## How many times to repeat single item
    repeat = 30

    image_list = [img_path] * repeat

    ## run multiple times
    for i in image_list:
        ocr(img_path)

    print(f"Elapsed time: {time.process_time() - start}")


if __name__ == "__main__":
    main()