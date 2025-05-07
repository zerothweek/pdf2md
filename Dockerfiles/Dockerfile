# Use the offcial Ubuntu base image
FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

# Set environment variables to non-interactive to avoid prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install necessary packages
RUN apt-get update && \
    apt-get install -y \
        software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y \
        python3.11 \
        python3.11-venv \
        python3.11-distutils \
        python3-pip \
        wget \
        git \
        libgl1 \
        libreoffice \
        fonts-noto-cjk \
        fonts-wqy-zenhei \
        fonts-wqy-microhei \
        ttf-mscorefonts-installer \
        fontconfig \
        libglib2.0-0 \
        libxrender1 \
        libsm6 \
        libxext6 \
        poppler-utils \
        && rm -rf /var/lib/apt/lists/*

# Set Python version using update-alternatives
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# Set python and pip symlinks to python3 and pip3
RUN ln -sf /usr/bin/python3.11 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip


RUN pip3 install --upgrade pip
# Copy the configuration file template and install magic-pdf latest
RUN wget https://github.com/opendatalab/MinerU/raw/master/magic-pdf.template.json \
    && cp magic-pdf.template.json /root/magic-pdf.json \
    && pip3 install -U magic-pdf[full]

# Download models and update the configuration file
RUN pip3 install huggingface_hub \
    && wget https://github.com/opendatalab/MinerU/raw/master/scripts/download_models_hf.py -O download_models.py \
    && python3 download_models.py \
    && sed -i 's|cpu|cuda|g' /root/magic-pdf.json

# requirements.txt installation
# COPY requirements.txt /workspace/
# RUN pip3 install --no-cache-dir -r /workspace/requirements.txt

CMD ["bin/bash"]
