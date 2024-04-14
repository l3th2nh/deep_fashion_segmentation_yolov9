FROM nvidia/cuda:11.7.1-devel-ubuntu20.04

# Prevent stop building ubuntu at time zone selection.  
ENV DEBIAN_FRONTEND=noninteractive

# Prepare and empty machine for building
RUN apt-get update && apt-get install -y apt-transport-https
RUN apt-get install -y --fix-missing \
    git \
    cmake \
    build-essential \
    libboost-program-options-dev \
    libboost-filesystem-dev \
    libboost-graph-dev \
    libboost-system-dev \
    libboost-test-dev \
    libeigen3-dev \
    libsuitesparse-dev \
    libfreeimage-dev \
    libmetis-dev \
    libgoogle-glog-dev \
    libgflags-dev \
    libflann-dev \
    libglew-dev \
    qtbase5-dev \
    libqt5opengl5-dev \
    libcgal-dev \
    libsqlite3-dev \
    libceres-dev \
    libmetis-dev \
    ninja-build \
    libsuitesparse-dev \
    ffmpeg 

RUN apt-get install unzip

RUN apt-get install libatlas-base-dev 


RUN apt-get install -y python3-pip python3-dev && \
    pip3 install --upgrade pip

RUN pip3 install torch==1.13.1+cu117 torchvision==0.14.1+cu117 torchaudio==0.13.1 --extra-index-url https://download.pytorch.org/whl/cu117

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY ./yolov9_instance_segment ./yolov9_instance_segment

WORKDIR /yolov9_instance_segment
