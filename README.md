# 🎬 Automated Video Face Anonymization System for Short Films

## 🎓 Academic Information

**Engineering Thesis (Praca Inżynierska)**

| Field | Value |
|---------|---------|
| Author | *Michał Niziołek* |
| University | *Politechnika Rzeszowska im. Ignacego Łukasiewicza* |
| Faculty | *Wydział Elektrotechniki i Informatyki* |
| Academic Year | 2025/2026 |

---

## 📖 Project Description

This project presents a complete automated face anonymization system designed for short films and video productions. The primary objective is to protect personal privacy while significantly reducing the manual effort required for frame-by-frame video editing.

The solution combines modern Deep Learning techniques for face detection with robust object tracking algorithms to ensure consistent anonymization throughout the entire video sequence.

The application is delivered as a full-stack web platform consisting of:

- **React** frontend
- **FastAPI** backend
- **YOLO-based face detection**
- **Norfair face tracking**
- **CUDA acceleration**
- **Docker containerization**

---

## ✨ Features

### 🎯 Face Detection

- Real-time face detection using **YOLO (Ultralytics)**.
- High detection accuracy and fast inference performance.
- Adjustable confidence thresholds.

### 🔄 Object Tracking

- Multi-object tracking using **Norfair**.
- Stable face tracking across frames.
- Reduced flickering during temporary occlusions or rapid camera movement.

### 🎛️ User Configuration option

- Tuning detection parameters.
- Adjustable tracking settings.
- Intuitive web interface for video processing.

### ⚡ Hardware Acceleration

- NVIDIA CUDA support.
- GPU-accelerated inference with PyTorch.
- Significantly reduced processing time.

### 🎥 Video Processing

- Efficient decoding and encoding using **PyAV (FFmpeg bindings)**.
- Frame manipulation with **NumPy**.
- Support for common video formats.

### 🐳 Containerized Deployment

- Docker-based architecture.
- One-command startup using Docker Compose.
- Reproducible deployment environment.

---

---

# 🔄 Processing Pipeline

The anonymization workflow consists of the following stages:

### 1. Video Upload

The user uploads a video through the React-based web interface.

### 2. Video Decoding

FastAPI receives the file and forwards it to the processing pipeline, where frames are decoded using PyAV.

### 3. Face Detection

Each frame is analyzed by the YOLO model, producing bounding boxes around detected faces.

### 4. Face Tracking

Norfair associates detections across frames and assigns unique IDs to maintain temporal consistency.

### 5. Face Anonymization

A Gaussian blur is applied to selected crop.

### 6. Video Export

Processed frames are encoded back into a video file and made available for download.

---

# 📸 User Interface

## Main Dashboard & Video Upload

Upload videos and configure anonymization settings.

<img width="1919" height="925" alt="image" src="https://github.com/user-attachments/assets/99f96159-6b4f-49f8-80c9-5bf9789d343a" />

---

## Hyperparameter Configuration

Adjust detection confidence and tracking parameters.

<img width="1919" height="925" alt="image" src="https://github.com/user-attachments/assets/32caab28-8ef5-4b94-a7b9-5fec83ca644f" />

---

## Selection of faces to anonimize

Select which detected faces should be anonymized.

<img width="1919" height="925" alt="image" src="https://github.com/user-attachments/assets/8083bf13-7ea8-4d4a-a98a-d5ce0af91493" />

---

## Download

Download modified video.

<img width="1919" height="925" alt="image" src="https://github.com/user-attachments/assets/215ca886-45f4-472a-9bfb-a90684d0d35c" />

---

# 🚀 Getting Started

## Prerequisites

Before running the project, make sure the following software is installed:

- Docker
- Docker Compose
- NVIDIA Drivers
- NVIDIA Container Toolkit

---

## Running the Application

Clone the repository:

```bash
git clone https://github.com/Michalooooooo/FaceAnonimizerProject

cd FaceAnonimizerProject
```

Build and start all services:

```bash
docker compose up --build
```

---

## Accessing the Application

After successful startup:

### Frontend

```text
http://localhost:5173
```

### Backend API

```text
http://localhost:8000
```

### FastAPI Documentation

```text
http://localhost:8000/docs
```

---

# 🧠 Technology Stack

## Computer Vision & AI

- Python
- PyTorch
- Ultralytics YOLO
- Norfair
- NumPy
- PyAV
- NVIDIA CUDA

---

## Backend

- FastAPI
- Uvicorn
- Pydantic

---

## Frontend

- React
- TypeScript

---

## DevOps

- Docker
- Docker Compose
- NVIDIA Container Toolkit

---
