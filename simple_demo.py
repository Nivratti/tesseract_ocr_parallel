from timeit import default_timer as timer
from tesserocr import PyTessBaseAPI

start = timer()

image = 'images/num.png'

with PyTessBaseAPI() as api:
    api.SetImageFile(image)
    print(api.GetUTF8Text())
    print(api.AllWordConfidences())
    
# api is automatically finalized when used in a with-statement (context manager).
# otherwise api.End() should be explicitly called when it's no longer needed.

print(f"Elapsed time: {timer() - start}")