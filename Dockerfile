FROM nvidia/cuda:11.8.0-base-ubuntu22.04

SHELL ["/bin/bash", "-c"]

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install --no-install-recommends -y python3 python3-pip libgl1 libglib2.0-0

COPY requirements.txt /requirements.txt

RUN --mount=type=cache,target=/root/.cache \
    pip install -r requirements.txt

ENV PATH="/usr/local/cuda-10.1/bin:${PATH}"
ENV LD_LIBRARY_PATH="/usr/local/cuda/extras/CUPTI/lib64:/usr/local/cuda-10.1/lib64:${LD_LIBRARY_PATH}"

RUN ldconfig

ENV TF_CUDA_PATHS=/usr/local/cuda-10.1,/usr/lib/x86_64-linux-gnu,/usr/include

WORKDIR /workspace
COPY . /workspace

# ENTRYPOINT ["python3", "-m", "serve", "0.0.0.0", "8001"]
ENTRYPOINT ["bash"]
