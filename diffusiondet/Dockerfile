# Environment cuda:11.3.0-cudnn8-devel-ubuntu20.04-python3.7-pytorch1.12.0-torchvision0.13.0
FROM nvidia/cuda:11.3.0-cudnn8-devel-ubuntu20.04

WORKDIR /work
COPY ./docker_build/* ./
RUN nvidia-smi

RUN rm /etc/apt/sources.list.d/cuda.list
RUN rm /etc/apt/sources.list.d/nvidia-ml.list
RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		git vim libgl1-mesa-glx libglib2.0-0 wget \
	&& rm -rf /var/lib/apt/lists/*

ENV CONDA_DIR /opt/conda
RUN /bin/bash ./Miniconda3-py37_4.12.0-Linux-x86_64.sh -b -p /opt/conda
ENV PATH=$CONDA_DIR/bin:$PATH
RUN conda create -n diffusiondet python=3.7 -y
RUN echo "source activate diffusiondet" > ~/.bashrc
ENV PATH /opt/conda/envs/diffusiondet/bin:$PATH

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install torch-1.12.0+cu113-cp37-cp37m-linux_x86_64.whl
RUN pip install torchvision-0.13.0+cu113-cp37-cp37m-linux_x86_64.whl
RUN pip install 'git+https://ghproxy.com/https://github.com/facebookresearch/detectron2.git'
RUN pip install opencv_python-4.6.0.66-cp36-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
