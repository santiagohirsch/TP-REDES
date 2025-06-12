import subprocess
import time
import os
import json
import glob
from datetime import datetime

def get_available_configs():
    """
    Obtiene la lista de archivos de configuración disponibles
    """
    config_files = glob.glob("configs/*.json")
    # Filtrar el archivo index.json
    config_files = [f for f in config_files if not f.endswith('index.json')]
    config_files.sort()
    return config_files

def load_config_info(config_path):
    """
    Carga información básica de un archivo de configuración
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return {
            'model_type': config.get('model_type', 'Unknown'),
            'run_name': config.get('run_name', 'Unknown'),
            'experiment_name': config.get('experiment_name', 'Unknown')
        }
    except:
        return {'model_type': 'Error', 'run_name': 'Error', 'experiment_name': 'Error'}

def run_experiment_from_json(config_file):
    """
    Ejecuta un experimento desde un archivo JSON
    """
    # Usar sys.executable para garantizar compatibilidad multiplataforma
    import sys
    cmd = [sys.executable, "predictor_from_json.py", config_file]
    
    print(f"\n{'='*60}")
    print(f"Ejecutando experimento desde: {config_file}")
    print(f"Comando: {' '.join(cmd)}")
    print(f"{'='*60}")
    
    start_time = time.time()
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        end_time = time.time()
        
        print("STDOUT:")
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        print(f"Experimento completado en {end_time - start_time:.2f} segundos")
        return True
    except subprocess.CalledProcessError as e:
        end_time = time.time()
        print(f"ERROR en experimento: {e}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        print(f"Experimento falló después de {end_time - start_time:.2f} segundos")
        return False

def run_all_experiments():
    """
    Ejecuta todos los experimentos disponibles
    """
    config_files = get_available_configs()
    
    if not config_files:
        print("No se encontraron archivos de configuración JSON")
        print("Ejecuta primero: python generate_json_configs.py")
        return
    
    print(f"Se encontraron {len(config_files)} archivos de configuración")
    
    # Mostrar resumen de experimentos
    print("\nEXPERIMENTOS A EJECUTAR:")
    print("-" * 60)
    for i, config_file in enumerate(config_files, 1):
        info = load_config_info(config_file)
        print(f"{i:2d}. {info['model_type']:25s} | {info['run_name']:20s} | {os.path.basename(config_file)}")
    
    print("\nIniciando ejecución de todos los experimentos...")
    
    successful = 0
    failed = 0
    
    for i, config_file in enumerate(config_files, 1):
        info = load_config_info(config_file)
        print(f"\nProgreso: {i}/{len(config_files)} - Ejecutando {info['model_type']} ({info['run_name']})")
        
        success = run_experiment_from_json(config_file)
        
        if success:
            successful += 1
        else:
            failed += 1
        
        # Pausa breve entre experimentos
        if i < len(config_files):  # No pausar después del último
            print("\nPausa de 2 segundos antes del siguiente experimento...")
            time.sleep(2)
    
    return successful, failed, len(config_files)

def run_selected_experiments(pattern=None, model_type=None):
    """
    Ejecuta experimentos filtrados por patrón o tipo de modelo
    """
    config_files = get_available_configs()
    
    # Filtrar por patrón
    if pattern:
        config_files = [f for f in config_files if pattern.lower() in f.lower()]
    
    # Filtrar por tipo de modelo
    if model_type:
        filtered_files = []
        for config_file in config_files:
            info = load_config_info(config_file)
            if model_type.lower() in info['model_type'].lower():
                filtered_files.append(config_file)
        config_files = filtered_files
    
    if not config_files:
        print(f"No se encontraron experimentos que coincidan con los filtros:")
        if pattern:
            print(f"   Patrón: {pattern}")
        if model_type:
            print(f"   Tipo de modelo: {model_type}")
        return
    
    print(f"Ejecutando {len(config_files)} experimentos filtrados")
    
    successful = 0
    failed = 0
    
    for i, config_file in enumerate(config_files, 1):
        info = load_config_info(config_file)
        print(f"\nProgreso: {i}/{len(config_files)} - Ejecutando {info['model_type']} ({info['run_name']})")
        
        success = run_experiment_from_json(config_file)
        
        if success:
            successful += 1
        else:
            failed += 1
        
        # Pausa breve entre experimentos
        if i < len(config_files):
            print("\nPausa de 2 segundos...")
            time.sleep(2)
    
    return successful, failed, len(config_files)

def show_available_experiments():
    """
    Muestra todos los experimentos disponibles sin ejecutarlos
    """
    config_files = get_available_configs()
    
    if not config_files:
        print("No se encontraron archivos de configuración JSON")
        print("Ejecuta primero: python generate_json_configs.py")
        return
    
    print(f"EXPERIMENTOS DISPONIBLES ({len(config_files)} total):")
    print("=" * 80)
    
    # Agrupar por tipo de modelo
    by_model = {}
    for config_file in config_files:
        info = load_config_info(config_file)
        model_type = info['model_type']
        if model_type not in by_model:
            by_model[model_type] = []
        by_model[model_type].append((config_file, info))
    
    for model_type, experiments in by_model.items():
        print(f"\n🔹 {model_type} ({len(experiments)} experimentos):")
        for config_file, info in experiments:
            print(f"   • {info['run_name']:20s} | {os.path.basename(config_file)}")

def main():
    print("EJECUTOR DE EXPERIMENTOS JSON")
    print("=" * 50)
    
    # Verificar que existe el directorio de configs
    if not os.path.exists('configs'):
        print("No se encontró el directorio 'configs/'")
        print("Ejecuta primero: python generate_json_configs.py")
        return
    
    # Mostrar opciones
    print("\nOPCIONES DISPONIBLES:")
    print("1. Ver todos los experimentos disponibles")
    print("2. Ejecutar TODOS los experimentos")
    print("3. Ejecutar solo experimentos de RandomForest")
    print("4. Ejecutar solo experimentos de GradientBoosting")
    print("5. Ejecutar solo experimentos de LinearRegression")
    print("6. Ejecutar solo experimentos de PoissonRegressor")
    
    choice = input("\nSelecciona una opción (1-6): ").strip()
    
    if choice == "1":
        show_available_experiments()
    
    elif choice == "2":
        print("\nEjecutando TODOS los experimentos...")
        successful, failed, total = run_all_experiments()
        print_summary(successful, failed, total)
    
    elif choice == "3":
        print("\nEjecutando experimentos de RandomForest...")
        successful, failed, total = run_selected_experiments(model_type="RandomForest")
        print_summary(successful, failed, total)
    
    elif choice == "4":
        print("\nEjecutando experimentos de GradientBoosting...")
        successful, failed, total = run_selected_experiments(model_type="GradientBoosting")
        print_summary(successful, failed, total)
    
    elif choice == "5":
        print("\nEjecutando experimentos de LinearRegression...")
        successful, failed, total = run_selected_experiments(model_type="LinearRegression")
        print_summary(successful, failed, total)
    
    elif choice == "6":
        print("\nEjecutando experimentos de PoissonRegressor...")
        successful, failed, total = run_selected_experiments(model_type="PoissonRegressor")
        print_summary(successful, failed, total)
    
    else:
        print("Opción no válida")

from dotenv import load_dotenv
import os

load_dotenv()

tracking_uri = os.getenv("MLFLOW_TRACKING_URI")

def print_summary(successful, failed, total):
    """
    Imprime un resumen de los experimentos ejecutados
    """
    print("\n" + "=" * 60)
    print("RESUMEN FINAL DE EXPERIMENTOS")
    print("=" * 60)
    print(f"Total ejecutados: {total}")
    print(f"Exitosos: {successful}")
    print(f"Fallidos: {failed}")
    print(f"Tasa de éxito: {(successful/total)*100:.1f}%")
    
    if successful > 0:
        print("\nRevisa los resultados en MLflow UI:")
        print(f"   {tracking_uri}")

if __name__ == "__main__":
    main() 