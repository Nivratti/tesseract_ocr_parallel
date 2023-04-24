FROM nvidia/cuda:10.2-cudnn7-runtime-ubuntu18.04

RUN apt-key del 7fa2af80
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/7fa2af80.pub

# Install some basic utilities
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    sudo \
    git \
    bzip2 \
    libx11-6 \
    build-essential \ 
    gcc 

## Tesseract
RUN apt-get install -y tesseract-ocr libtesseract-dev libleptonica-dev pkg-config

# Create a working directory
RUN mkdir /app
WORKDIR /app

# Create a non-root user and switch to it
RUN adduser --disabled-password --gecos '' --shell /bin/bash user \
 && chown -R user:user /app
RUN echo "user ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/90-user
USER user

# All users can use /home/user as their home directory
ENV HOME=/home/user
RUN chmod 777 /home/user

# Install Miniconda and Python
ENV CONDA_AUTO_UPDATE_CONDA=false
ENV PATH=/home/user/miniconda/bin:$PATH
RUN curl -sLo ~/miniconda.sh https://repo.continuum.io/miniconda/Miniconda3-py38_4.8.2-Linux-x86_64.sh \
 && chmod +x ~/miniconda.sh \
 && ~/miniconda.sh -b -p ~/miniconda \
 && rm ~/miniconda.sh \
 && conda install -y python==3.8.* \
 && conda clean -ya

## Switch to root -- to install extra ubuntu libraries
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgl1 \
        libglib2.0-0 

RUN apt-get install -y cmake

RUN export DEBIAN_FRONTEND=noninteractive && ln -fs /usr/share/zoneinfo/Asia/Calcutta /etc/localtime && apt-get install -y tzdata && dpkg-reconfigure --frontend noninteractive tzdata

# ## For ncnn
# RUN apt install -y libprotobuf-dev protobuf-compiler libvulkan-dev vulkan-utils libopencv-dev
# RUN git clone https://github.com/Tencent/ncnn.git && cd ncnn && git submodule init && git submodule update && mkdir -p build && cd build && cmake -DCMAKE_BUILD_TYPE=Release -DNCNN_VULKAN=ON -DNCNN_PYTHON=ON -DNCNN_SYSTEM_GLSLANG=OFF -DNCNN_AVXVNNI=OFF -DNCNN_BUILD_EXAMPLES=ON .. && make -j$(nproc) && cd ../python && python3 -m pip install . && python3 -m pip install -r requirements.txt

## Switch back to user 
USER user

RUN python3 -m pip install --upgrade pip

RUN python3 -m pip install tesserocr==2.5.0
# python3 -c "import tesserocr; print(tesserocr.get_languages())"

RUN python3 -m pip install opencv-python
RUN python3 -m pip install psutil

WORKDIR "/app"

# configure the container to run in an executed manner
ENTRYPOINT [ "bash" ]
# CMD ["main.py" ]

# ENTRYPOINT [ "python3", "main.py"  ]

