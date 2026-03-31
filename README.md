# 🛡️ Dashboard de Detección de Fraude con Machine Learning

## 📌 Descripción

Este proyecto consiste en el desarrollo de un sistema de detección de fraude en transacciones con tarjeta de crédito utilizando técnicas de Machine Learning.

Incluye análisis de datos, entrenamiento de modelos y visualización interactiva mediante un dashboard desplegado en la nube.

---

## 🌐 Demo en vivo

👉 [[Ver aplicación](https://TU-APP.streamlit.app)](https://fraud-detection-dashboard-rmfafyypdweu23vff6cswt.streamlit.app/)

---

## ⚙️ Tecnologías utilizadas

* Python
* Pandas
* NumPy
* Scikit-learn
* Imbalanced-learn (SMOTE)
* Matplotlib / Seaborn
* Streamlit

---

## 🧠 Modelos implementados

* Random Forest
* K-Nearest Neighbors (KNN)
* Técnicas de balanceo de datos (SMOTE)

---

## 📊 Dataset

El dataset no se incluye en este repositorio debido a restricciones de tamaño.

Puedes descargarlo desde:
👉 https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud

También se utiliza una versión accesible en línea para el despliegue:
👉 https://storage.googleapis.com/download.tensorflow.org/data/creditcard.csv

---

## 📈 Funcionalidades del dashboard

* Visualización de la distribución de fraudes
* Métricas clave (transacciones, fraudes, no fraudes)
* Análisis exploratorio de datos
* Simulación básica de transacciones
* Visualización de importancia de variables

---

## 🚀 Cómo ejecutar el proyecto

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/DavidZepedaC/fraud-detection-dashboard.git
   ```

2. Instalar dependencias:

   ```bash
   pip install -r requirements.txt
   ```

3. Ejecutar la aplicación:

   ```bash
   streamlit run app/app.py
   ```

---

## 📂 Estructura del proyecto

```id="estructura1"
fraud-detection-dashboard/
│
├── app/
│   └── app.py
│
├── notebooks/
│   └── fraud_detection_analysis.ipynb
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🎯 Objetivo del proyecto

Desarrollar un sistema capaz de identificar transacciones fraudulentas de manera eficiente, priorizando la detección de fraudes (recall) en escenarios con datos desbalanceados.

---

## 👨‍💻 Autor

**David Zepeda**
