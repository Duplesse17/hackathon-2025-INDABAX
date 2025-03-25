import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib
from datetime import datetime

# ======================
# 🟢 Chargement du dataset
# ======================
df = pd.read_excel('data/donneurs_geocode_update.xlsx')

# ======================
# 🟢 Prétraitement
# ======================

# Age à partir de la date de naissance
df['Date de naissance'] = pd.to_datetime(df['Date de naissance'], errors='coerce')
df['Age'] = df['Date de naissance'].apply(lambda x: datetime.now().year - x.year if pd.notnull(x) else np.nan)
df['Age'] = df['Age'].fillna(df['Age'].median())  # Correction pour éviter FutureWarning

# Nettoyage du Taux d’hémoglobine
df['Taux d’hémoglobine'] = (
    df['Taux d’hémoglobine']
    .astype(str)
    .str.replace('g/dl', '', case=False, regex=False)
    .str.replace(' ', '', regex=False)
    .str.replace(',', '.', regex=False)
    .str.replace('123.1', '12.1', regex=False)
    .str.replace('111.9', '11.9', regex=False)
)
df['Taux d’hémoglobine'] = pd.to_numeric(df['Taux d’hémoglobine'], errors='coerce')
df['Taux d’hémoglobine'] = df['Taux d’hémoglobine'].fillna(df['Taux d’hémoglobine'].median())

# Encodage des colonnes catégorielles
label_cols = ['Genre', "Niveau d'etude", 'Situation Matrimoniale (SM)', 'Profession', 
                'Nationalité', 'Religion', 'A-t-il (elle) déjà donné le sang']

label_encoders = {}
for col in label_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))
    label_encoders[col] = le  # Stockage des encodeurs



# Sélection des features
features = ['Age', 'Genre', "Niveau d'etude", 'Situation Matrimoniale (SM)', 
            'Profession', 'Nationalité', 'Religion', 'A-t-il (elle) déjà donné le sang', 
            'Taux d’hémoglobine']

X = df[features]

# Encodage de la variable cible en multi-classes
le_target = LabelEncoder()
df['ÉLIGIBILITÉ AU DON.'] = le_target.fit_transform(df['ÉLIGIBILITÉ AU DON.'].astype(str))

# Sauvegarde du label encoder pour les prédictions futures
joblib.dump(le_target, 'data/target_label_encoder.pkl')

y = df['ÉLIGIBILITÉ AU DON.']

# ======================
# 🟢 Entraînement du modèle
# ======================

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print(f"Distribution des classes dans y_train : {np.bincount(y_train)}")
print(f"Distribution des classes dans y_test  : {np.bincount(y_test)}")

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ======================
# 🟢 Sauvegarde du modèle
# ======================

joblib.dump(model, 'data/eligibility_model.pkl')
joblib.dump(label_encoders, 'data/label_encoders.pkl')

print("✅ Modèle sauvegardé avec succès !")

# ======================
# 🟢 Évaluation du modèle
# ======================

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(cm)

print("Classification Report:")
print(classification_report(y_test, y_pred, target_names=le_target.classes_))
