import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import mlflow
import mlflow.keras

IMG_SIZE = (224,224)
BATCH_SIZE = 16
EPOCHS = 10

# Adding data augmentation to the training generator to make the model more robust
# and prevent overfitting. This helps the model generalize better to new, unseen images.
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True,
)
test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    "dataset/train",
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="binary",
    classes=["real", "fake"]
)

val_generator = test_datagen.flow_from_directory(
    "dataset/val",
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="binary",
    classes=["real", "fake"]
)

test_generator = test_datagen.flow_from_directory(
    "dataset/test",
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="binary",
    classes=["real", "fake"]
)

base_model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(224,224,3)
)

base_model.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation="relu")(x)
x = Dropout(0.5)(x)
predictions = Dense(1, activation="sigmoid")(x)

model = Model(inputs=base_model.input, outputs=predictions)

model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

# Enable MLflow auto-logging for MLOps
mlflow.keras.autolog()

with mlflow.start_run() as run:
    mlflow.log_param("IMG_SIZE", IMG_SIZE)
    mlflow.log_param("BATCH_SIZE", BATCH_SIZE)
    
    model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=EPOCHS
    )
    loss, acc = model.evaluate(test_generator)
    
    print("Test Accuracy:", acc)
    model.save("deepfake_cnn_model.h5")
    print("\n===============================")
    print("MLOps Tracking Enabled!")
    print("Run 'mlflow ui' in your terminal to see the dashboard.")
    print("===============================\n")