FROM nvidia/cuda:12.1.1-devel-ubuntu22.04

# Install system deps
RUN apt-get update && apt-get install -y \
    python3.10 python3.10-dev python3.10-distutils \
    wget curl git gcc build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set Python symlinks
RUN ln -s /usr/bin/python3.10 /usr/bin/python && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python

ENV CUDA_HOME=/usr/local/cuda
ENV PATH="$CUDA_HOME/bin:$PATH"
ENV LD_LIBRARY_PATH="$CUDA_HOME/lib64:$LD_LIBRARY_PATH"

# Install uv and your deps
COPY requirements.txt .
RUN pip install uv
RUN uv pip install -r requirements.txt --system
RUN pip install "git+https://github.com/VarunGumma/IndicTransToolkit@37483c962c486f2f61d8b3f659c0a1064c55ac6c#egg=IndicTransToolkit"

# Install flash-attn
RUN nvcc --version
RUN uv pip install flash_attn --no-build-isolation --system

# Copy app source
WORKDIR /app
COPY app ./app

EXPOSE 8088
CMD ["uvicorn", "app.translate_openai_api:app", "--host", "0.0.0.0", "--port", "8088"]
