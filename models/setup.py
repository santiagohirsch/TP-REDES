#!/usr/bin/env python3
"""
Script de configuración para el proyecto de Machine Learning con MLflow
"""

import subprocess
import sys
import os

def run_command(command, description):
    """
    Ejecuta un comando y maneja errores
    """
    print(f"\n🔧 {description}")
    print(f"   Ejecutando: {' '.join(command)}")
    
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"   ✅ {description} completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Error en {description}:")
        print(f"      {e.stderr}")
        return False

def check_python_version():
    """
    Verifica que la versión de Python sea compatible
    """
    version = sys.version_info
    print(f"🐍 Versión de Python: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 8:
        print("   ✅ Versión de Python compatible")
        return True
    else:
        print("   ❌ Se requiere Python 3.8 o superior")
        return False

def install_requirements():
    """
    Instala las dependencias del requirements.txt
    """
    if not os.path.exists('requirements.txt'):
        print("❌ No se encontró el archivo requirements.txt")
        return False
    
    return run_command(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        "Instalando dependencias de Python"
    )

def verify_installation():
    """
    Verifica que las librerías se instalaron correctamente
    """
    print("\n🧪 Verificando instalación de librerías...")
    
    libraries = [
        'numpy',
        'pandas', 
        'sklearn',
        'mlflow',
        'matplotlib',
        'seaborn'
    ]
    
    all_ok = True
    for lib in libraries:
        try:
            __import__(lib)
            print(f"   ✅ {lib}")
        except ImportError:
            print(f"   ❌ {lib} - No instalado")
            all_ok = False
    
    return all_ok

def create_directories():
    """
    Crea los directorios necesarios
    """
    directories = ['configs', 'logs', 'data']
    
    print("\n📁 Creando directorios necesarios...")
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"   ✅ Directorio '{directory}' creado")
        else:
            print(f"   📁 Directorio '{directory}' ya existe")

def main():
    print("🚀 CONFIGURACIÓN DEL ENTORNO DE MACHINE LEARNING")
    print("=" * 60)
    
    # Verificar versión de Python
    if not check_python_version():
        sys.exit(1)
    
    # Crear directorios
    create_directories()
    
    # Instalar dependencias
    if not install_requirements():
        print("\n❌ Falló la instalación de dependencias")
        sys.exit(1)
    
    # Verificar instalación
    if not verify_installation():
        print("\n❌ Algunas librerías no se instalaron correctamente")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ CONFIGURACIÓN COMPLETADA EXITOSAMENTE")
    print("=" * 60)
    print("\n🎯 Próximos pasos:")
    print("1. Generar configuraciones JSON:")
    print("   python3 generate_json_configs.py")
    print("\n2. Ejecutar experimentos:")
    print("   python3 run_json_experiments.py")
    print("\n3. Ver resultados en MLflow:")
    print("   mlflow ui --port 8080")
    print("   Luego ve a: http://localhost:8080")
    
    print("\n📚 Archivos principales:")
    print("   • predictor_from_json.py - Script principal")
    print("   • generate_json_configs.py - Generador de configuraciones")
    print("   • run_json_experiments.py - Ejecutor de experimentos")
    print("   • requirements.txt - Dependencias")

if __name__ == "__main__":
    main() 