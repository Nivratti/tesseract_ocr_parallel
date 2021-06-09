"""
Initialize tess_api for each worker process -- only once

Note:
    Use Pool(initializer=...) to initialize the Tesseract object once per worker process before they start 
    reading their job queue.
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

tess_api = None

def initialize_worker():
    global tess_api
    tess_api = PyTessBaseAPI()  # initialize a copy for this instance

def ocr(image):
    if isinstance(image, str):
        tess_api.SetImageFile(image)
    else:
        tess_api.SetImage(image)

    text = tess_api.GetUTF8Text()
    return text


def main():
    total_cpu_cores = psutil.cpu_count(logical=False)
    print(f"total_cpu_cores: {total_cpu_cores}")

    start = time.process_time()
    
    img_path = 'images/num.png'

    ## How many times to repeat single item
    repeat = 30

    image_list = [img_path] * repeat

    with multiprocessing.Pool(processes=total_cpu_cores, initializer=initialize_worker) as p:
        for result in p.imap_unordered(ocr, image_list):
            print(result)
            pass

    print(f"Elapsed time: {time.process_time() - start}")


if __name__ == "__main__":
    main()