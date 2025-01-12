# -*- coding: utf-8 -*-
"""Capston-1-MLZoomcamp2024-25.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1LJjlbY34BlfFbt9t08Z-fivM7T-E_gSG
"""

#Installing all the libraries
!pip install tensorflow opencv-python matplotlib

!pip list

import tensorflow as tf
import os

#Acoid OOM errors by setting up GPU memory consumption growth
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
  tf.config.experimental.set_memory_growth(gpu,True)

tf.config.list_physical_devices('GPU')

!pwd

!mkdir Image_Data

cd Image_Data

!pwd

import kagglehub

# Download latest version
path = kagglehub.dataset_download("balabaskar/wonders-of-the-world-image-classification")

print("Path to dataset files:", path)

cd /root/.cache/kagglehub/datasets/balabaskar/wonders-of-the-world-image-classification/versions/2

pwd

ls -ltr

cp -r 'Wonders of World'/  wonders_of_world_images.csv /content/Image_Data/

#Performing EDA on the dataset
import os
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import cv2
from collections import Counter

#The Below shows the number of images containing in each of the folders
dataset_path = '/content/Image_Data/Wonders of World/Wonders of World'
classes = os.listdir(dataset_path)
print(f"Classes: {classes}")
for class_name in classes:
    class_path = os.path.join(dataset_path, class_name)
    num_images = len(os.listdir(class_path))
    print(f"Class '{class_name}' has {num_images} images.")

#Visualizing the number of Images per class to detect Imbalances
class_counts = {class_name: len(os.listdir(os.path.join(dataset_path, class_name))) for class_name in classes}

# Plot distribution
plt.figure(figsize=(10, 6))
plt.bar(class_counts.keys(), class_counts.values(), color='Green')
plt.title('Class Distribution')
plt.xlabel('Wonders')
plt.ylabel('Number of Images')
plt.xticks(rotation=45)
plt.show()

"""From the above we can conclude that there are significant number of images in each of the wonders of the world folders"""

#Visualizing sample images from some of the folders of the images from each class to inspect visual consistency
plt.figure(figsize=(16, 18))
for i, class_name in enumerate(classes[:8]):  # Adjust to visualize more classes
    class_path = os.path.join(dataset_path, class_name)
    sample_image_path = os.path.join(class_path, os.listdir(class_path)[0])  # First image
    img = Image.open(sample_image_path)
    plt.subplot(1, 8, i + 1)
    plt.imshow(img)
    plt.title(class_name)
    plt.axis('off')
plt.show()

#Now we are going to check for variation in image sizes and aspect ratios
image_shapes = []
for class_name in classes:
    class_path = os.path.join(dataset_path, class_name)
    for image_name in os.listdir(class_path):
        image_path = os.path.join(class_path, image_name)
        with Image.open(image_path) as img:
            image_shapes.append(img.size)

widths, heights = zip(*image_shapes)
aspect_ratios = np.array(widths) / np.array(heights)

# Plot distributions
plt.figure(figsize=(16, 18))
plt.subplot(1, 3, 1)
plt.hist(widths, bins=20, color='blue', alpha=0.7)
plt.title('Width Distribution')
plt.subplot(1, 3, 2)
plt.hist(heights, bins=20, color='green', alpha=0.7)
plt.title('Height Distribution')
plt.subplot(1, 3, 3)
plt.hist(aspect_ratios, bins=20, color='red', alpha=0.7)
plt.title('Aspect Ratio Distribution')
plt.show()

#Checking for Blurry Imagesdef calculate_blurriness(image_path):
import os
import cv2
import matplotlib.pyplot as plt

# Function to calculate blurriness using variance of Laplacian
def calculate_blurriness(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Load image in grayscale
    if img is None:
        return None  # Handle invalid image files
    return cv2.Laplacian(img, cv2.CV_64F).var()

# Initialize list to store blurriness scores
blurriness_scores = []

# Base dataset path (master folder containing subfolders)
dataset_path = "/content/Image_Data/Wonders of World/Wonders of World"

# List all subfolders (classes) in the dataset folder
classes = os.listdir(dataset_path)

# Iterate over each class folder
for class_name in classes:
    class_path = os.path.join(dataset_path, class_name)  # Path to the class folder

    # Ensure it's a directory (to skip files accidentally present in the dataset folder)
    if not os.path.isdir(class_path):
        continue

    # Iterate over each image in the class folder
    for image_name in os.listdir(class_path):
        image_path = os.path.join(class_path, image_name)  # Full path to the image

        # Only process valid image files
        if image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            blurriness_score = calculate_blurriness(image_path)
            if blurriness_score is not None:  # Only append valid scores
                blurriness_scores.append(blurriness_score)

# Plotting the blurriness score distribution
plt.figure(figsize=(10, 6))
plt.hist(blurriness_scores, bins=50, color='purple')
plt.title('Blurriness Score Distribution')
plt.xlabel('Blurriness Score')
plt.ylabel('Number of Images')
plt.show()

"""From the above we can interpret the following :

	Images with Very Low Scores (< 500):**bold text**
These images are likely very blurry. We might want to inspect and potentially exclude these from your dataset, as they could negatively impact your model’s ability to learn.
	Images with Moderate Scores (500–5000):**bold text**
These are likely acceptable in terms of sharpness for training. They might have some blurriness but still retain enough detail for feature extraction.
	Images with High Scores (> 5000):**bold text**
These are likely very sharp images with good detail, which are ideal for training an image classification model.
"""

from sklearn.model_selection import train_test_split
import shutil
import os

# Define paths
base_dir = "/content/Image_Data/Wonders of World/Wonders of World"
train_dir = "/content/Image_Data/Wonders of World/train"
val_dir = "/content/Image_Data/Wonders of World/val"
test_dir = "/content/Image_Data/Wonders of World/test"

# Create directories
os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# Split into train, validation, and test
for class_name in os.listdir(base_dir):
    class_path = os.path.join(base_dir, class_name)
    if not os.path.isdir(class_path):
        continue  # Skip non-directory files

    # Filter valid image files
    images = [img for img in os.listdir(class_path) if img.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if not images:
        print(f"No valid images found in {class_name}")
        continue

    # Split images
    train, temp = train_test_split(images, test_size=0.3, random_state=42)
    val, test = train_test_split(temp, test_size=0.5, random_state=42)

    # Move files to respective folders
    for folder, split in zip([train_dir, val_dir, test_dir], [train, val, test]):
        class_folder = os.path.join(folder, class_name)
        os.makedirs(class_folder, exist_ok=True)
        for img in split:
            try:
                shutil.copy(os.path.join(class_path, img), os.path.join(class_folder, img))
            except Exception as e:
                print(f"Error copying {img} from {class_name}: {e}")

"""Now, I am going to work on an Image preprocessing for the images"""

from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Define the data generators
train_datagen = ImageDataGenerator(
    rescale=1.0 / 255,   # Normalize pixel values (0-255 -> 0-1)
    rotation_range=20,   # Random rotation
    width_shift_range=0.2,  # Horizontal shift
    height_shift_range=0.2,  # Vertical shift
    shear_range=0.2,     # Shear transformation
    zoom_range=0.2,      # Zoom-in and zoom-out
    horizontal_flip=True,  # Randomly flip images horizontally
    fill_mode='nearest'  # Fill in missing pixels
)

val_test_datagen = ImageDataGenerator(rescale=1.0 / 255)

# Load the data from directories
train_generator = train_datagen.flow_from_directory(
    "/content/Image_Data/Wonders of World/train",
    target_size=(150, 150),  # Resize images to 150x150
    batch_size=32,
    class_mode='categorical'  # For multi-class classification
)

val_generator = val_test_datagen.flow_from_directory(
    "/content/Image_Data/Wonders of World/val",
    target_size=(150, 150),
    batch_size=32,
    class_mode='categorical'
)

test_generator = val_test_datagen.flow_from_directory(
    "/content/Image_Data/Wonders of World/test",
    target_size=(150, 150),
    batch_size=32,
    class_mode='categorical'
)

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

model = Sequential([
    # Convolutional layers
    Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
    MaxPooling2D(2, 2),

    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),

    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),

    # Flattening layer
    Flatten(),

    # Print the output shape after flattening
    Dense(512, activation='relu'),
    Dropout(0.5),
    Dense(12, activation='softmax')  # Output layer
])

# Display the model summary to check output shapes
model.summary()

"""The above is the summary of the neural networks build, summarizing the above we have :Explanation of the Model Summary
	1.	Layer Details:
	•	Each row in the table represents a layer in your model.
	•	Layer Type:
	•	Conv2D: Convolutional layers used to extract spatial features from the image.
	•	MaxPooling2D: Pooling layers used to down-sample feature maps and reduce computational load.
	•	Flatten: Flattens the multidimensional feature maps into a single vector.
	•	Dense: Fully connected layers used for classification.
	•	Dropout: A regularization layer that helps prevent overfitting.
	2.	Output Shape:
	•	Displays the dimensions of the output after each layer. For example:
	•	The first Conv2D outputs feature maps of shape (148, 148, 32) because it applies 32 filters, and the image size is reduced slightly due to the kernel size.
	3.	Parameters (Param #):
	•	Shows the total trainable parameters in each layer.
	•	For instance, the first Conv2D has 896 parameters (calculated as (3*3*3*32) + 32 for kernel weights and biases).
	4.	Total Params:
	•	19,039,820 is the total number of trainable parameters in your model.
	•	This is quite a large model, so training it might take some time, depending on your compute resources.
"""

# Compile the model (make sure to do this before fitting the model)
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Now, retrain the model
history = model.fit(
    train_generator,
    epochs=13,  # Number of epochs to train
    validation_data=val_generator,  # Validation data to track progress
    callbacks=[reduce_lr]  # If you are using ReduceLROnPlateau, else remove this line
)

# Evaluate the model on the test data
# Define the test data generator with the same preprocessing as the training data
test_datagen = ImageDataGenerator(rescale=1./255)

# Assuming you have defined the test directory, set the target size to (150, 150)
test_generator = test_datagen.flow_from_directory(
    '/content/Image_Data/Wonders of World/test',
    target_size=(150, 150),  # Resize to match the model's input size
    batch_size=32,
    class_mode='categorical'
)

# Now, evaluate the model on the resized test data
test_loss, test_accuracy = model.evaluate(test_generator)

# Print the results
print(f"Test Loss: {test_loss}")
print(f"Test Accuracy: {test_accuracy}")

# Check the shape of a sample batch from the test generator
for batch in test_generator:
    print(batch[0].shape)
    break

#Saving the model

model.save('my_model.keras')

