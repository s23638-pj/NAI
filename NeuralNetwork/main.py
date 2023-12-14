"""
Skrypt wykorzystuje model sieci neuronowej do klasyfikacji obrazów z zestawu danych CIFAR-10.

Autorzy: Sebastian Augustyniak & Wiktor Krieger

Sposób użycia:
- Upewnij się, że Python oraz wymagane biblioteki
    (tensorflow) są zainstalowane.
- Jeżeli nie miałeś zainstalowanego wcześniej zestawu CIFAR-10,
    zestaw ten zostanie pobrany przy pierwszym uruchomieniu
- Uruchom skrypt, aby wczytać dane CIFAR-10, przetworzyć je,
    zbudować i wytrenować model sieci neuronowej.

"""

from tensorflow.keras import layers, models
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.utils import to_categorical

(train_images, train_labels), (test_images, test_labels) = cifar10.load_data()
train_images, test_images = train_images / 255.0, test_images / 255.0
train_labels = to_categorical(train_labels, num_classes=10)
test_labels = to_categorical(test_labels, num_classes=10)

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(10, activation='softmax'))

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.fit(train_images, train_labels, epochs=10, validation_data=(test_images, test_labels))
test_loss, test_acc = model.evaluate(test_images, test_labels)

print(f"Dokładność na zestawie testowym: {test_acc}")