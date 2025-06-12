# Models

Modelos de Machine Learning con MLflow integrado para simular clientes del sistema principal.

---

## Requisitos del Sistema

### Software necesario:
- [**Python 3.8+**](https://www.python.org/downloads/)

---

## Instalación y Configuración

**En Windows:**
```cmd
cd models
python -m venv venv_mlflow
venv_mlflow\Scripts\activate
pip install -r requirements.txt
```

**En macOS/Linux:**
```bash
cd models
python3 -m venv venv_mlflow
source venv_mlflow/bin/activate
pip install -r requirements.txt
```

## Ejecución de experimentos

### Generar configuraciones de experimentos
```bash
cd models
python generate_json_configs.py
```

### Opciones de ejecución:

#### 1. Ejecutor interactivo
```bash
python run_json_experiments.py
```

#### 2. Ejecutar experimento específico
```bash
python predictor_from_json.py configs/linear_regression_config_01.json
```

#### 3. Ejecutar todos los experimentos
```bash
python run_json_experiments.py --all
```

### Visualización de resultados
Para visualizar los resultados registrados por _MLflow_:
```bash
mlflow ui
```
Luego abre tu navegador en: http://localhost:5000

## Modelos Disponibles

- **Linear Regression**: Regresión lineal básica
- **Random Forest Regressor**: Bosques aleatorios
- **Gradient Boosting Regressor**: Boosting de gradiente
- **Poisson Regressor**: Regresión de Poisson
