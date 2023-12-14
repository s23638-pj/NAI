"""
Opis problemu:
Program wykorzystuje proste sieci neuronowe
do przewidzenia przeżycia pasażerów na pokładzie Titanica na podstawie określonych cech.

Autorzy: Sebastian Augustyniak & Wiktor Krieger

Sposób użycia:
- Upewnij się, że Python oraz wymagane biblioteki
    (pandas, scikit-learn, tensorflow) są zainstalowane.
- Uruchom skrypt, aby wczytać dane Titanic, przetworzyć dane,
    zbudować i wytrenować model sieci neuronowej.
- Sprawdź drukowaną dokładność i raport klasyfikacyjny,
    aby ocenić wydajność modelu sieci neuronowej.
"""


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import seaborn as sns
import matplotlib.pyplot as plt

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
titanic_data = pd.read_csv(url)

features = titanic_data[['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']]
label = titanic_data['Survived']
features = pd.get_dummies(features, columns=['Sex', 'Embarked'], drop_first=True)

imputer = SimpleImputer(strategy='mean')
features_imputed = imputer.fit_transform(features)

X_train, X_test, y_train, y_test = train_test_split(features_imputed, label, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = Sequential()
model.add(Dense(256, activation='relu', input_dim=X_train_scaled.shape[1]))
model.add(Dense(16, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X_train_scaled, y_train, epochs=10, batch_size=32, validation_data=(X_test_scaled, y_test))

predictions_nn = (model.predict(X_test_scaled) > 0.5).astype(int)
accuracy_nn = accuracy_score(y_test, predictions_nn)

print(f'Neural Network Accuracy: {accuracy_nn:.2f}')
print('\nNeural Network Classification Report:')
print(classification_report(y_test, predictions_nn))

conf_matrix = confusion_matrix(y_test, predictions_nn)
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=['Not Survived', 'Survived'], yticklabels=['Not Survived', 'Survived'])
plt.title('Confusion Matrix')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()
