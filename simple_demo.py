import time

from tesserocr import PyTessBaseAPI

start = time.process_time()

image = 'images/num.png'

with PyTessBaseAPI() as api:
    api.SetImageFile(image)
    print(api.GetUTF8Text())
    print(api.AllWordConfidences())
    
# api is automatically finalized when used in a with-statement (context manager).
# otherwise api.End() should be explicitly called when it's no longer needed.

print(f"Elapsed time: {time.process_time() - start}")