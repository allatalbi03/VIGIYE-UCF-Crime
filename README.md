# VIGIYE - Privacy-Preserving Intelligent Surveillance System

<div align="center">
  <img src="https://img.shields.io/badge/Huawei-ICT%20Competition%202025--2026-red" alt="Huawei ICT Competition"/>
  <img src="https://img.shields.io/badge/Edge%20AI-Privacy%20First-blueviolet" alt="Edge AI"/>
  <img src="https://img.shields.io/badge/Federated%20Learning-Secure-green" alt="Federated Learning"/>
  <img src="https://img.shields.io/badge/PyTorch-1.9%2B-orange" alt="PyTorch"/>
  <img src="https://img.shields.io/badge/MediaPipe-Pose-blue" alt="MediaPipe"/>
  <img src="https://img.shields.io/badge/Made%20in-Algeria-008751" alt="Made in Algeria"/>
</div>

<br>

<p align="center">
  <b>Privacy-Preserving Early Warning System for Anomaly Detection in Video Surveillance</b>
</p>

<p align="center">
  <i>Detect threats 3 seconds in advance • Zero raw video leaves the edge • Federated Learning • 13 anomaly classes</i>
</p>

<p align="center">
  <b>Huawei ICT Competition 2025-2026 | E-SURGE Team | University of El-Oued, Algeria</b>
</p>

---

## Table of Contents
- [Overview](#overview)
- [Problem & Solution](#problem--solution)
- [Key Innovations](#key-innovations)
- [Technical Architecture](#technical-architecture)
- [Privacy Features](#privacy-features)
- [Dataset](#dataset)
- [Installation](#installation)
- [Usage](#usage)
- [Model Architecture](#model-architecture)
- [Results](#results)
- [Team](#team)
- [Acknowledgments](#acknowledgments)

---

## Overview

**VIGIYE** (Vigilance + Eye) is an intelligent video security system designed to detect dangerous behaviors and threats while **fully preserving user privacy**. Unlike traditional surveillance systems that transfer raw video to the cloud, VIGIYE performs feature extraction directly on AI-enabled cameras at the edge.

### Quick Statistics

| Metric | Value |
|--------|-------|
| Early Warning | 3 seconds before event |
| Classification Accuracy | 82.1% |
| Anomaly Classes | 13 classes |
| Privacy Level | 0% raw video leaves device |
| Model Size | 120K parameters |
| Inference Latency | <100ms on edge |

---

## Problem & Solution

### The Problem
Traditional surveillance systems face critical challenges:

| Challenge | Description |
|-----------|-------------|
| Privacy Violations | Raw video contains sensitive personal information (faces, features, locations) |
| High Bandwidth | Continuous video streaming consumes excessive bandwidth (MB/s) |
| Centralized Risks | Single point of failure and data breach vulnerabilities in the cloud |
| Reactive Monitoring | Human operators cannot monitor all feeds simultaneously |
| Delayed Response | Incidents are detected after they occur, not before |

### VIGIYE Solution

| Solution | Description |
|----------|-------------|
| Edge-First Architecture | Processing happens on camera/edge device - no raw video ever leaves |
| Privacy-by-Design | Only encrypted behavioral features are shared (99 numbers only) |
| Early Warning | Predict anomalies up to 3 seconds before occurrence using temporal modeling |
| Federated Learning | Collaborative improvement without data exposure - each device learns locally |
| Low Bandwidth | Only model weights (KB) instead of video (MB/GB) |

---

## Key Innovations

| Innovation | Description |
|------------|-------------|
| Privacy-Preserving Features | Uses only pose landmarks (33 body keypoints) normalized to remove identity cues - no faces, no raw pixels |
| Early Warning System | Predicts anomaly start within 3-second horizon using temporal modeling (GRU) |
| Federated Learning Ready | Architecture designed for distributed training without sharing raw data |
| Edge-Optimized | Lightweight GRU model (128-dim hidden) suitable for edge deployment on Huawei Atlas |
| Multi-Class Detection | 13 anomaly classes + normal behavior classification |
| Huawei Integration | Designed to work with Huawei ModelArts, Atlas Edge Computing, and Ascend AI |

---

### Technologies Used

| Component | Technology | Purpose |
|-----------|------------|---------|
| Edge AI | MediaPipe Pose | Privacy-preserving feature extraction |
| Deep Learning | PyTorch, GRU | Temporal modeling & classification |
| Federated Learning | Huawei ModelArts | Collaborative learning (design) |
| Edge Hardware | Atlas Edge Computing, Ascend AI | Target deployment platform |
| Cloud Services | Huawei OBS, AOM | Storage & monitoring |
| Applications | Mobile/Web App | Alert reception |

---

## Privacy Features

VIGIYE implements multiple layers of privacy protection:

### 1. No Facial Recognition
- Uses only 33 body pose landmarks (shoulders, hips, knees, etc.)
- No facial landmarks, no skin texture, no raw pixels

### 2. Normalized Coordinates

This normalization removes:
- Body shape/identity cues
- Absolute position in frame
- Camera perspective variations

### 3. Feature Dimension: 99 only
- 33 landmarks × (x, y, visibility)
- Impossible to reconstruct original video

### 4. Federated Learning Architecture
- Raw video NEVER leaves edge device
- Only encrypted model weights are shared
- Each device trains on local data only

### 5. Comparison with Existing Systems

| Feature | Traditional CCTV | Cloud-AI (Nest/Verkada) | VIGIYE (Ours) |
|---------|-----------------|------------------------|---------------|
| Raw Video Storage | Full footage | Cloud storage | NEVER leaves device |
| Privacy Risk | Physical theft | Data breaches | End-to-end encrypted |
| Bandwidth | High (continuous) | High | Ultra-low (weights only) |
| Learning | Static | Centralized | Federated |
| Intelligence | Passive | Basic detection | Complex behavior analysis |
| Offline Operation | Yes | No | Yes |
| Early Warning | No | No | 3 seconds |

---

## Dataset: UCF-Crime

We use the UCF-Crime dataset, a large-scale surveillance video dataset containing:

### Anomaly Classes (13)

| Category | Classes |
|----------|---------|
| Violence | Abuse, Arrest, Assault, Fighting |
| Theft | Burglary, Robbery, Stealing, Shoplifting |
| Destruction | Arson, Explosion, Vandalism |
| Traffic | RoadAccidents |
| Weapons | Shooting |

### Dataset Statistics
- Total videos: 1,900 hours of footage
- Anomaly videos: ~1,610
- Normal videos: ~290
- Temporal annotations: Frame-level start/end for anomalies

### Early Warning Task
We formulate the problem as: **Predict which anomaly class will START within the next 3 seconds**

---

## Installation

### Prerequisites
- Python 3.8+
- CUDA-capable GPU (optional, for training)
- 8GB+ RAM
- OpenCV

### Steps

```bash
# 1. Clone repository
git clone https://github.com/yourusername/VIGIYE-UCF-Crime.git
cd VIGIYE-UCF-Crime

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download UCF-Crime dataset
# Register at: https://www.crcv.ucf.edu/projects/real-world/
# Place videos in ./data/UCF-Crime/ with structure:
#   data/UCF-Crime/
#   ├── Abuse/
#   ├── Arrest/
#   ├── Arson/
#   ├── Assault/
#   ├── RoadAccidents/
#   ├── Burglary/
#   ├── Explosion/
#   ├── Fighting/
#   ├── Robbery/
#   ├── Shooting/
#   ├── Stealing/
#   ├── Shoplifting/
#   ├── Vandalism/
#   └── Normal/

# 4. Update paths in config.py
# Edit UCF_ROOT, FEAT_DIR, MODEL_OUT to your local paths