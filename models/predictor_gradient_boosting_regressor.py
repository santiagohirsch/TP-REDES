import numpy as np
import pandas as pd
import math
import mlflow
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score, precision_score, recall_score, f1_score

mlflow.set_tracking_uri(uri="http://localhost:8080")

df = pd.read_csv("dataset_futbol_simulado.csv")

# Features: ratings de equipos (puedes agregar más features si deseas)
X = df[['rating_local', 'rating_visitante']]

# Target: goles de cada equipo
y_local = df['goles_local']
y_visitante = df['goles_visitante']

# Entrenamiento y test split
X_train, X_test, y_train_local, y_test_local, y_train_visitante, y_test_visitante = train_test_split(
    X, y_local, y_visitante, test_size=0.2, random_state=42)

params = {
    "n_estimators": 100,
    "learning_rate": 0.1,
    "max_depth": 3,
    "min_samples_split": 2,
    "min_samples_leaf": 1,
    "subsample": 1.0,
    "random_state": 42
}

# Inicializar y entrenar GradientBoostingRegressor para goles del equipo local
reg_local = GradientBoostingRegressor(**params)

# Entrenar el modelo con los datos de entrenamiento
reg_local.fit(X_train, y_train_local)

# Predecir goles para el equipo local
y_pred_local = reg_local.predict(X_test)

# Inicializar y entrenar GradientBoostingRegressor para goles del equipo visitante
reg_visitante = GradientBoostingRegressor(**params)

# Entrenar el modelo con los datos de entrenamiento
reg_visitante.fit(X_train, y_train_visitante)

# Predecir goles para el equipo visitante
y_pred_visitante = reg_visitante.predict(X_test)

# Evaluar el rendimiento del modelo
mse_local = mean_squared_error(y_test_local, y_pred_local)
mse_visitante = mean_squared_error(y_test_visitante, y_pred_visitante)

accuracy_local = accuracy_score(y_test_local, np.round(y_pred_local))
accuracy_visitante = accuracy_score(y_test_visitante, np.round(y_pred_visitante))

precision_local = precision_score(y_test_local, np.round(y_pred_local), average='weighted', zero_division=0)
precision_visitante = precision_score(y_test_visitante, np.round(y_pred_visitante), average='weighted', zero_division=0)

recall_local = recall_score(y_test_local, np.round(y_pred_local), average='weighted', zero_division=0)
recall_visitante = recall_score(y_test_visitante, np.round(y_pred_visitante), average='weighted', zero_division=0)

f1_local = f1_score(y_test_local, np.round(y_pred_local), average='weighted', zero_division=0)
f1_visitante = f1_score(y_test_visitante, np.round(y_pred_visitante), average='weighted', zero_division=0)

# Guardar los resultados en MLflow
# Create a new MLflow Experiment
mlflow.set_experiment("GradientBoostingRegressor_Futbol")

with mlflow.start_run():
    # Log parameters
    mlflow.log_params(params)

    # Log metrics
    mlflow.log_metric("mse_local", mse_local)
    mlflow.log_metric("mse_visitante", mse_visitante)
    mlflow.log_metric("accuracy_local", accuracy_local)
    mlflow.log_metric("accuracy_visitante", accuracy_visitante)
    mlflow.log_metric("precision_local", precision_local)
    mlflow.log_metric("precision_visitante", precision_visitante)
    mlflow.log_metric("recall_local", recall_local)
    mlflow.log_metric("recall_visitante", recall_visitante)
    mlflow.log_metric("f1_local", f1_local)
    mlflow.log_metric("f1_visitante", f1_visitante)

    # Set tags
    mlflow.set_tag("model_type", "GradientBoostingRegressor")
    mlflow.set_tag("model_version", "1.0")
    mlflow.set_tag("dataset", "futbol_simulado")

    # Infer the model signature
    signature = mlflow.models.infer_signature(X_train, y_pred_local)

    # Log the model
    mlflow.sklearn.log_model(
        sk_model=reg_local,
        artifact_path="model_local",
        signature=signature,
        input_example=X_train.iloc[0].to_dict(),
        registered_model_name="GradientBoostingRegressor_Futbol_Local"
    )
    mlflow.sklearn.log_model(
        sk_model=reg_visitante,
        artifact_path="model_visitante",
        signature=signature,
        input_example=X_train.iloc[0].to_dict(),
        registered_model_name="GradientBoostingRegressor_Futbol_Visitante"
    ) 