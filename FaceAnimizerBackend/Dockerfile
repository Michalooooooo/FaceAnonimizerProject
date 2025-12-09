FROM nvidia/cuda:12.3.1-runtime-ubuntu22.04

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /faceanimizer_backend

# system deps
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    libgl1 libglib2.0-0 \
    ffmpeg libavcodec-dev libavformat-dev libavdevice-dev \
    libavfilter-dev libavutil-dev libswscale-dev libswresample-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
