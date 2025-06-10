import numpy as np
import pandas as pd
import json
import sys
import mlflow
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, PoissonRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score, precision_score, recall_score, f1_score

def load_config(config_path):
    """
    Carga la configuración desde un archivo JSON
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"✅ Configuración cargada desde: {config_path}")
        return config
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {config_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Error: El archivo {config_path} no es un JSON válido")
        sys.exit(1)

def get_model_class(model_type):
    """
    Retorna la clase del modelo según el tipo especificado
    """
    models = {
        "RandomForestRegressor": RandomForestRegressor,
        "GradientBoostingRegressor": GradientBoostingRegressor,
        "LinearRegression": LinearRegression,
        "PoissonRegressor": PoissonRegressor
    }
    
    if model_type not in models:
        raise ValueError(f"Tipo de modelo no soportado: {model_type}")
    
    return models[model_type]

def train_and_evaluate_model(config):
    """
    Entrena y evalúa el modelo según la configuración
    """
    print(f"\n🚀 Iniciando entrenamiento: {config['run_name']}")
    print(f"📊 Modelo: {config['model_type']}")
    print(f"⚙️  Parámetros: {config['parameters']}")
    
    # Configurar MLflow
    mlflow.set_tracking_uri(uri="http://localhost:8080")
    mlflow.set_experiment(config['experiment_name'])
    
    # Cargar dataset
    df = pd.read_csv(config['dataset']['file_path'])
    print(f"📂 Dataset cargado: {config['dataset']['file_path']} ({len(df)} filas)")
    
    # Preparar features y targets
    X = df[config['dataset']['features']]
    y_local = df[config['dataset']['targets'][0]]  # goles_local
    y_visitante = df[config['dataset']['targets'][1]]  # goles_visitante
    
    # Split de entrenamiento y test
    X_train, X_test, y_train_local, y_test_local, y_train_visitante, y_test_visitante = train_test_split(
        X, y_local, y_visitante, 
        test_size=config['training']['test_size'], 
        random_state=config['training']['random_state']
    )
    
    print(f"📈 Datos de entrenamiento: {len(X_train)} muestras")
    print(f"📉 Datos de test: {len(X_test)} muestras")
    
    # Obtener clase del modelo
    ModelClass = get_model_class(config['model_type'])
    
    # Entrenar modelo para equipo local
    print("\n🏠 Entrenando modelo para equipo local...")
    reg_local = ModelClass(**config['parameters'])
    reg_local.fit(X_train, y_train_local)
    y_pred_local = reg_local.predict(X_test)
    
    # Entrenar modelo para equipo visitante
    print("✈️  Entrenando modelo para equipo visitante...")
    reg_visitante = ModelClass(**config['parameters'])
    reg_visitante.fit(X_train, y_train_visitante)
    y_pred_visitante = reg_visitante.predict(X_test)
    
    # Calcular métricas
    print("\n📊 Calculando métricas...")
    metrics = calculate_metrics(y_test_local, y_pred_local, y_test_visitante, y_pred_visitante)
    
    # Mostrar resultados
    print_results(metrics)
    
    # Registrar en MLflow
    register_in_mlflow(config, metrics, reg_local, reg_visitante, X_train, y_pred_local)
    
    return metrics

def calculate_metrics(y_test_local, y_pred_local, y_test_visitante, y_pred_visitante):
    """
    Calcula todas las métricas de evaluación
    """
    metrics = {}
    
    # MSE
    metrics['mse_local'] = mean_squared_error(y_test_local, y_pred_local)
    metrics['mse_visitante'] = mean_squared_error(y_test_visitante, y_pred_visitante)
    metrics['mse_promedio'] = (metrics['mse_local'] + metrics['mse_visitante']) / 2
    
    # Accuracy
    metrics['accuracy_local'] = accuracy_score(y_test_local, np.round(y_pred_local))
    metrics['accuracy_visitante'] = accuracy_score(y_test_visitante, np.round(y_pred_visitante))
    metrics['accuracy_promedio'] = (metrics['accuracy_local'] + metrics['accuracy_visitante']) / 2
    
    # Precision
    metrics['precision_local'] = precision_score(y_test_local, np.round(y_pred_local), average='weighted', zero_division=0)
    metrics['precision_visitante'] = precision_score(y_test_visitante, np.round(y_pred_visitante), average='weighted', zero_division=0)
    
    # Recall
    metrics['recall_local'] = recall_score(y_test_local, np.round(y_pred_local), average='weighted', zero_division=0)
    metrics['recall_visitante'] = recall_score(y_test_visitante, np.round(y_pred_visitante), average='weighted', zero_division=0)
    
    # F1-score
    metrics['f1_local'] = f1_score(y_test_local, np.round(y_pred_local), average='weighted', zero_division=0)
    metrics['f1_visitante'] = f1_score(y_test_visitante, np.round(y_pred_visitante), average='weighted', zero_division=0)
    
    return metrics

def print_results(metrics):
    """
    Imprime los resultados de forma organizada
    """
    print("\n" + "="*50)
    print("📊 RESULTADOS DEL EXPERIMENTO")
    print("="*50)
    print(f"🏠 Equipo Local:")
    print(f"   MSE: {metrics['mse_local']:.4f}")
    print(f"   Accuracy: {metrics['accuracy_local']:.4f}")
    print(f"   Precision: {metrics['precision_local']:.4f}")
    print(f"   Recall: {metrics['recall_local']:.4f}")
    print(f"   F1-score: {metrics['f1_local']:.4f}")
    
    print(f"\n✈️  Equipo Visitante:")
    print(f"   MSE: {metrics['mse_visitante']:.4f}")
    print(f"   Accuracy: {metrics['accuracy_visitante']:.4f}")
    print(f"   Precision: {metrics['precision_visitante']:.4f}")
    print(f"   Recall: {metrics['recall_visitante']:.4f}")
    print(f"   F1-score: {metrics['f1_visitante']:.4f}")
    
    print(f"\n📈 Promedios:")
    print(f"   MSE Promedio: {metrics['mse_promedio']:.4f}")
    print(f"   Accuracy Promedio: {metrics['accuracy_promedio']:.4f}")

def register_in_mlflow(config, metrics, reg_local, reg_visitante, X_train, y_pred_local):
    """
    Registra el experimento en MLflow
    """
    print("\n💾 Registrando en MLflow...")
    
    with mlflow.start_run(run_name=config['run_name']):
        # Log parameters
        mlflow.log_params(config['parameters'])
        
        # Log metrics
        for metric_name, metric_value in metrics.items():
            mlflow.log_metric(metric_name, metric_value)
        
        # Set tags
        mlflow.set_tag("model_type", config['model_type'])
        for tag_name, tag_value in config['tags'].items():
            mlflow.set_tag(tag_name, tag_value)
        
        # Infer model signature
        signature = mlflow.models.infer_signature(X_train, y_pred_local)
        
        # Log models
        mlflow.sklearn.log_model(
            sk_model=reg_local,
            artifact_path="model_local",
            signature=signature,
            input_example=X_train.iloc[0].to_dict(),
            registered_model_name=f"{config['model_type']}_JSON_Local_{config['run_name']}"
        )
        
        mlflow.sklearn.log_model(
            sk_model=reg_visitante,
            artifact_path="model_visitante",
            signature=signature,
            input_example=X_train.iloc[0].to_dict(),
            registered_model_name=f"{config['model_type']}_JSON_Visitante_{config['run_name']}"
        )
    
    print(f"✅ Experimento '{config['run_name']}' registrado exitosamente en MLflow!")

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 predictor_from_json.py <config_file.json>")
        print("Ejemplo: python3 predictor_from_json.py configs/random_forest_config_1.json")
        sys.exit(1)
    
    config_path = sys.argv[1]
    
    print("🔬 PREDICTOR BASADO EN CONFIGURACIÓN JSON")
    print("=" * 50)
    
    # Cargar configuración
    config = load_config(config_path)
    
    # Entrenar y evaluar
    metrics = train_and_evaluate_model(config)
    
    print(f"\n✅ Experimento completado exitosamente!")
    print(f"🌐 Revisa los resultados en MLflow: http://localhost:8080")

if __name__ == "__main__":
    main() 