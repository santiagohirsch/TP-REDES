import json
import os
from itertools import product
from datetime import datetime

def ensure_configs_dir():
    """
    Asegura que exista el directorio configs/
    """
    if not os.path.exists('configs'):
        os.makedirs('configs')
        print("Directorio 'configs/' creado")

def generate_random_forest_configs():
    """
    Genera múltiples configuraciones JSON para RandomForest
    """
    print("Generando configuraciones para RandomForest...")
    
    # Definir variaciones de parámetros
    n_estimators_options = [50, 100, 200]
    max_depth_options = [5, 10, 15, None]
    min_samples_split_options = [2, 5]
    min_samples_leaf_options = [1, 3]
    
    configs = []
    config_counter = 1
    
    # Generar algunas combinaciones (no todas para evitar explosión combinatoria)
    selected_combinations = [
        (50, 5, 2, 1),
        (50, 10, 2, 1),
        (100, 5, 2, 1),
        (100, 10, 2, 1),
        (100, 15, 2, 1),
        (100, None, 2, 1),
        (200, 10, 2, 1),
        (100, 10, 5, 1),
        (100, 10, 2, 3),
        (200, 15, 5, 3),
    ]
    
    for n_est, max_d, min_split, min_leaf in selected_combinations:
        config = {
            "model_type": "RandomForestRegressor",
            "run_name": f"RF_config_{config_counter:02d}",
            "experiment_name": "RandomForestRegressor_JSON_Futbol",
            "parameters": {
                "n_estimators": n_est,
                "max_depth": max_d,
                "min_samples_split": min_split,
                "min_samples_leaf": min_leaf,
                "random_state": 42,
                "n_jobs": -1
            },
            "dataset": {
                "file_path": "dataset_futbol_simulado.csv",
                "features": ["rating_local", "rating_visitante"],
                "targets": ["goles_local", "goles_visitante"]
            },
            "training": {
                "test_size": 0.2,
                "random_state": 42
            },
            "tags": {
                "model_version": "json_config",
                "dataset": "futbol_simulado",
                "experiment_type": "json_hyperparameter_tuning",
                "generated_at": datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
            }
        }
        
        filename = f"configs/random_forest_config_{config_counter:02d}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
        configs.append(filename)
        config_counter += 1
        
        print(f"     Generado: {filename}")
    
    return configs

def generate_gradient_boosting_configs():
    """
    Genera múltiples configuraciones JSON para GradientBoosting
    """
    print("Generando configuraciones para GradientBoosting...")
    
    # Definir variaciones de parámetros  
    selected_combinations = [
        (50, 0.05, 3, 1.0),
        (50, 0.1, 3, 1.0),
        (50, 0.2, 3, 1.0),
        (100, 0.05, 3, 1.0),
        (100, 0.1, 3, 1.0),
        (100, 0.2, 3, 1.0),
        (200, 0.1, 3, 1.0),
        (100, 0.1, 5, 1.0),
        (100, 0.1, 7, 1.0),
        (100, 0.1, 3, 0.8),
        (100, 0.1, 3, 0.9),
        (150, 0.15, 4, 0.85),
    ]
    
    configs = []
    config_counter = 1
    
    for n_est, lr, max_d, subsample in selected_combinations:
        config = {
            "model_type": "GradientBoostingRegressor",
            "run_name": f"GB_config_{config_counter:02d}",
            "experiment_name": "GradientBoostingRegressor_JSON_Futbol",
            "parameters": {
                "n_estimators": n_est,
                "learning_rate": lr,
                "max_depth": max_d,
                "min_samples_split": 2,
                "min_samples_leaf": 1,
                "subsample": subsample,
                "random_state": 42
            },
            "dataset": {
                "file_path": "dataset_futbol_simulado.csv",
                "features": ["rating_local", "rating_visitante"],
                "targets": ["goles_local", "goles_visitante"]
            },
            "training": {
                "test_size": 0.2,
                "random_state": 42
            },
            "tags": {
                "model_version": "json_config",
                "dataset": "futbol_simulado",
                "experiment_type": "json_hyperparameter_tuning",
                "generated_at": datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
            }
        }
        
        filename = f"configs/gradient_boosting_config_{config_counter:02d}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
        configs.append(filename)
        config_counter += 1
        
        print(f"     Generado: {filename}")
    
    return configs

def generate_linear_regression_configs():
    """
    Genera configuraciones JSON para LinearRegression
    """
    print("Generando configuraciones para LinearRegression...")
    
    configs = []
    config_counter = 1
    
    # LinearRegression tiene pocos parámetros, pero podemos crear variaciones
    variations = [
        {"fit_intercept": True, "positive": False},
        {"fit_intercept": False, "positive": False},
        {"fit_intercept": True, "positive": True},
    ]
    
    for params in variations:
        config = {
            "model_type": "LinearRegression",
            "run_name": f"LR_config_{config_counter:02d}",
            "experiment_name": "LinearRegression_JSON_Futbol",
            "parameters": {
                **params,
                "copy_X": True,
                "n_jobs": None
            },
            "dataset": {
                "file_path": "dataset_futbol_simulado.csv",
                "features": ["rating_local", "rating_visitante"],
                "targets": ["goles_local", "goles_visitante"]
            },
            "training": {
                "test_size": 0.2,
                "random_state": 42
            },
            "tags": {
                "model_version": "json_config",
                "dataset": "futbol_simulado",
                "experiment_type": "json_hyperparameter_tuning",
                "generated_at": datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
            }
        }
        
        filename = f"configs/linear_regression_config_{config_counter:02d}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
        configs.append(filename)
        config_counter += 1
        
        print(f"     Generado: {filename}")
    
    return configs

def generate_poisson_regression_configs():
    """
    Genera configuraciones JSON para PoissonRegressor
    """
    print("Generando configuraciones para PoissonRegressor...")
    
    configs = []
    config_counter = 1
    
    # Variaciones de parámetros para Poisson
    variations = [
        {"alpha": 1.0, "solver": "lbfgs", "max_iter": 1000},
        {"alpha": 0.5, "solver": "lbfgs", "max_iter": 1000},
        {"alpha": 2.0, "solver": "lbfgs", "max_iter": 1000},
        {"alpha": 1.0, "solver": "newton-cholesky", "max_iter": 1000},
    ]
    
    for params in variations:
        config = {
            "model_type": "PoissonRegressor",
            "run_name": f"PR_config_{config_counter:02d}",
            "experiment_name": "PoissonRegressor_JSON_Futbol",
            "parameters": {
                **params,
                "tol": 1e-4
            },
            "dataset": {
                "file_path": "dataset_futbol_simulado.csv",
                "features": ["rating_local", "rating_visitante"],
                "targets": ["goles_local", "goles_visitante"]
            },
            "training": {
                "test_size": 0.2,
                "random_state": 42
            },
            "tags": {
                "model_version": "json_config",
                "dataset": "futbol_simulado",
                "experiment_type": "json_hyperparameter_tuning",
                "generated_at": datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
            }
        }
        
        filename = f"configs/poisson_regressor_config_{config_counter:02d}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
        configs.append(filename)
        config_counter += 1
        
        print(f"     Generado: {filename}")
    
    return configs

def main():
    print("GENERADOR DE CONFIGURACIONES JSON")
    print("=" * 50)

    # Asegurar que existe el directorio
    ensure_configs_dir()
    
    all_configs = []
    
    # Generar configuraciones para cada tipo de modelo
    all_configs.extend(generate_random_forest_configs())
    all_configs.extend(generate_gradient_boosting_configs())
    all_configs.extend(generate_linear_regression_configs())
    all_configs.extend(generate_poisson_regression_configs())
    
    print("\n" + "=" * 50)
    print("RESUMEN DE GENERACIÓN")
    print("=" * 50)
    print(f"Total de archivos JSON generados: {len(all_configs)}")
    print("\nArchivos creados:")
    for config_file in all_configs:
        print(f"   • {config_file}")
    
    print(f"\nTodos los archivos JSON han sido generados en el directorio 'configs/'")
    print(f"Ahora puedes ejecutar experimentos con:")
    print(f"   python3 predictor_from_json.py configs/<nombre_del_archivo>.json")
    
    # Crear un archivo de índice con todos los configs
    index = {
        "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "total_configs": len(all_configs),
        "config_files": all_configs,
        "usage": "python3 predictor_from_json.py <config_file>"
    }
    
    with open('configs/index.json', 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=4, ensure_ascii=False)
    
    print(f"Archivo de índice creado: configs/index.json")

if __name__ == "__main__":
    main() 