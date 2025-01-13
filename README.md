# ML_ZoomCamp_Capston_Project_2025
# Wonders of the World Image Classification

## Overview

This project focuses on classifying images of the Wonders of the World using a deep learning model. The model is trained to recognize and categorize images into their respective wonder classes.

## Table of Contents

- [Overview](#overview)
- [Dataset](#dataset)
- [Model Architecture](#model-architecture)
- [Training](#training)
- [Evaluation](#evaluation)
- [Usage](#usage)
- [Results](#results)
- [Contributing](#contributing)https://github.com/anurag1210/ML_ZoomCamp_Capston_Project_2025/blob/main/README.md#overview
- [License](#license)

## Dataset

The dataset comprises images of various Wonders of the World, categorized into 12 classes. Each class represents a different wonder. The dataset is structured with separate directories for training and testing images.

## Model Architecture

The model is built using TensorFlow and Keras, leveraging a pre-trained convolutional neural network (CNN) for feature extraction, followed by custom dense layers for classification. Transfer learning is employed to enhance performance given the limited dataset size.

## Training

- **Data Augmentation:** Applied to increase dataset variability and prevent overfitting.
- **Optimizer:** Adam optimizer with a learning rate of 0.001.
- **Loss Function:** Categorical Crossentropy.
- **Batch Size:** 32.
- **Epochs:** 30.

## Evaluation

The model achieved a test accuracy of approximately 63.5% and a test loss of 1.174 on the evaluation dataset.

## Usage

To use the model for classifying your own images:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/anurag1210/ML_ZoomCamp_Capston_Project_2025
