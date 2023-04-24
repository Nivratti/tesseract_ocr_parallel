# tesseract_ocr_parallel
Speed up tesseract ocr by running parallel instances on cpu cores. Only one instance will be created for each cpu core. Tesserocr will not work properly if we use multithreading (multiple threads on each core).


## Testing conclusion:

Global single initialization of tessapi in single_instance_v2.py giving best result among all other files.