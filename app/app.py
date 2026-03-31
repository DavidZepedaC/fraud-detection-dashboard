import streamlit as st
import pandas as pd
import numpy as np
import random
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from imblearn.over_sampling import SMOTE

st.set_page_config(page_title="Fraud Dashboard", layout="wide")

# =========================
# HEADER
# =========================
st.title("💳 Dashboard Ejecutivo - Detección de Fraude")
st.markdown("Simulación y análisis de transacciones financieras mediante Machine Learning.")

# =========================
# DATA
# =========================
@st.cache_data
def load_data():
    url = "https://storage.googleapis.com/download.tensorflow.org/data/creditcard.csv"
    return pd.read_csv(url)
    return data.sample(10000)  # más rápido

data = load_data()

# =========================
# MODELO
# =========================
@st.cache_resource
def train_model(data):
    X = data.drop("Class", axis=1)
    y = data["Class"]

    X_train, _, y_train, _ = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    smote = SMOTE(random_state=42)
    X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

    base_model = RandomForestClassifier(n_estimators=30, random_state=42)
    model = CalibratedClassifierCV(base_model, method='sigmoid', cv=3)
    model.fit(X_train_res, y_train_res)

    return model, X.columns

model, feature_names = train_model(data)

# =========================
# CONTROLES
# =========================
st.subheader("🎮 Controles")

if st.button("🎲 Generar transacción", use_container_width=True):

    tipo = random.choice(["normal", "medio", "fraude"])

    if tipo == "normal":
        sample = data[data["Class"] == 0].sample(1)

    elif tipo == "fraude":
        sample = data[data["Class"] == 1].sample(1)

    else:
        normal = data[data["Class"] == 0].sample(1)
        fraude = data[data["Class"] == 1].sample(1)

        sample = normal.copy()

        for col in normal.columns:
            if col != "Class":
                sample[col] = (normal[col].values[0] + fraude[col].values[0]) / 2

        sample["Class"] = np.nan  # 🔥 clave

    st.session_state.sample = sample

st.markdown("---")

# =========================
# BUSCADOR
# =========================
st.markdown("### 🔎 Buscar transacción por ID")

search_id = st.number_input("Ingresa el ID de la transacción", min_value=0, step=1)

if st.button("Buscar transacción"):
    if search_id in data.index:
        st.session_state.sample = data.loc[[search_id]]
        st.success("Transacción cargada correctamente")
    else:
        st.error("ID no encontrado")

# =========================
# DEFAULT
# =========================
if "sample" not in st.session_state:
    st.session_state.sample = data.sample(1)

sample = st.session_state.sample

# =========================
# DETALLE
# =========================
st.subheader("🧾 Transacción evaluada")

col1, col2 = st.columns(2)

with col1:
    st.metric("ID", sample.index[0] if hasattr(sample.index, "__len__") else "Simulada")

with col2:
    amount = sample["Amount"].values[0]
    if pd.isna(amount):
        amount = 0
    st.metric("Monto", f"${amount:.2f}")

# =========================
# PREDICCIÓN
# =========================
X_input = sample.drop("Class", axis=1, errors="ignore")

prediction = model.predict(X_input)[0]
probability = model.predict_proba(X_input)[0][1]

probability = max(0.01, min(0.99, probability))

# =========================
# IDENTIFICAR TIPO
# =========================
real_value = sample["Class"].values[0]

if pd.isna(real_value):
    tipo = "medio"
else:
    tipo = "fraude" if int(real_value) == 1 else "normal"

# =========================
# KPI
# =========================
st.subheader("📊 Evaluación de riesgo")

col1, col2 = st.columns(2)

with col1:
    st.metric("Probabilidad de fraude", f"{probability:.2%}")

with col2:
    if tipo == "medio":
        st.warning("🟡 RIESGO MEDIO")
    elif prediction == 1:
        st.error("🚨 ALTO RIESGO")
    else:
        st.success("🟢 BAJO RIESGO")

# =========================
# SEMÁFORO
# =========================
st.subheader("🚦 Nivel de riesgo")

if tipo == "medio":
    st.warning("🟡 Medio (simulación)")
    st.progress(0.5)

else:
    if probability < 0.4:
        st.success("🟢 Bajo")
    elif probability < 0.75:
        st.warning("🟡 Medio")
    else:
        st.error("🔴 Alto")

    st.progress(float(probability))

# =========================
# VALIDACIÓN
# =========================
st.subheader("🔍 Validación")

if tipo == "medio":
    st.info("Caso simulado (no existe en dataset real)")
else:
    st.write(f"Real: {'Fraude' if tipo == 'fraude' else 'Normal'}")
    st.write(f"Predicción: {'Fraude' if prediction == 1 else 'Normal'}")

# =========================
# EXPLICABILIDAD
# =========================
st.subheader("🧠 Variables que influyen")

rf_model = model.calibrated_classifiers_[0].estimator
importances = rf_model.feature_importances_

impact = []

for i, f in enumerate(feature_names):
    val = sample[f].values[0]
    imp = importances[i]
    impact.append((f, val * imp))

impact_df = pd.DataFrame(impact, columns=["Feature", "Impacto"])
impact_df = impact_df.sort_values(by="Impacto", key=abs, ascending=False).head(10)

st.bar_chart(impact_df.set_index("Feature"))

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("Sistema robusto con simulación de escenarios y evaluación de riesgo en tiempo real")