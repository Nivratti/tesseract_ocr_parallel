import os
import cv2
from tesserocr import PyTessBaseAPI
 
import os
import glob
import concurrent.futures
from timeit import default_timer as timer
import psutil

os.environ['OMP_THREAD_LIMIT'] = '1'

def ocr(img_path):
    with PyTessBaseAPI() as api:
        api.SetImageFile(img_path)
        print(api.GetUTF8Text())
        print(api.AllWordConfidences())
    return True

def main():
    total_cpu_cores = psutil.cpu_count(logical=False)
    print(f"total_cpu_cores: {total_cpu_cores}")

    start = timer()
    
    img_path = 'images/num.png'

    ## How many times to repeat single item
    repeat = 30

    image_list = [img_path] * repeat

    # with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
    #     image_list = glob.glob(path+"\\*.png")
    #     for img_path,out_file in zip(image_list,executor.map(ocr,image_list)):
    #         print(img_path.split("\\")[-1],',',out_file,', processed')

    with concurrent.futures.ProcessPoolExecutor(max_workers=total_cpu_cores) as executor:
        for img_path in zip(image_list, executor.map(ocr, image_list)):
            pass

    print(f"Elapsed time: {timer() - start}")


if __name__ == "__main__":
    main()