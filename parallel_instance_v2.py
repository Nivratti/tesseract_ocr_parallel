"""
Global tesserocr api intialition for speedup
"""
import os
import cv2
from tesserocr import PyTessBaseAPI
 
import os
import glob
import concurrent.futures
import multiprocessing
import time
import psutil

# Only one tesserocr instance per core
os.environ['OMP_THREAD_LIMIT'] = '1'

api = PyTessBaseAPI()


def ocr(img_path):
    api.SetImageFile(img_path)
    print(api.GetUTF8Text())
    print(api.AllWordConfidences())
    return True

def main():
    total_cpu_cores = psutil.cpu_count(logical=False)
    print(f"total_cpu_cores: {total_cpu_cores}")

    start = time.process_time()
    
    img_path = 'images/num.png'

    ## How many times to repeat single item
    repeat = 200

    image_list = [img_path] * repeat

    with concurrent.futures.ProcessPoolExecutor(max_workers=total_cpu_cores) as executor:
        for img_path in zip(image_list, executor.map(ocr, image_list)):
            pass

    print(f"Elapsed time: {time.process_time() - start}")


if __name__ == "__main__":
    main()