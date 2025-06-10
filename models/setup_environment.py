#!/usr/bin/env python3
"""
Script de configuración automática del entorno para experimentos de ML
Compatible con Windows, macOS y Linux
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def get_system_info():
    """Obtiene información del sistema operativo"""
    system = platform.system()
    return {
        'os': system,
        'is_windows': system == 'Windows',
        'is_mac': system == 'Darwin',
        'is_linux': system == 'Linux',
        'python_version': sys.version,
        'python_executable': sys.executable
    }

def check_python_version():
    """Verifica que la versión de Python sea compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def create_virtual_environment():
    """Crea el entorno virtual"""
    venv_name = "venv_mlflow"
    
    if os.path.exists(venv_name):
        print(f"⚠️  El entorno virtual '{venv_name}' ya existe")
        response = input("¿Quieres recrearlo? (s/N): ").lower().strip()
        if response in ['s', 'si', 'sí', 'y', 'yes']:
            import shutil
            shutil.rmtree(venv_name)
            print(f"🗑️  Entorno anterior eliminado")
        else:
            print("📂 Usando entorno virtual existente")
            return True
    
    print(f"🔨 Creando entorno virtual '{venv_name}'...")
    try:
        subprocess.run([sys.executable, "-m", "venv", venv_name], check=True)
        print("✅ Entorno virtual creado exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creando entorno virtual: {e}")
        return False

def get_activation_commands():
    """Obtiene los comandos de activación según el sistema operativo"""
    system_info = get_system_info()
    
    if system_info['is_windows']:
        return {
            'activate': 'venv_mlflow\\Scripts\\activate',
            'python': 'python',
            'pip': 'pip'
        }
    else:  # macOS/Linux
        return {
            'activate': 'source venv_mlflow/bin/activate',
            'python': 'python',  # En el venv ya es el correcto
            'pip': 'pip'
        }

def install_requirements():
    """Instala las dependencias de requirements.txt"""
    if not os.path.exists('requirements.txt'):
        print("❌ No se encontró el archivo requirements.txt")
        return False
    
    system_info = get_system_info()
    
    # Determinar el comando pip del entorno virtual
    if system_info['is_windows']:
        pip_cmd = os.path.join('venv_mlflow', 'Scripts', 'pip')
    else:
        pip_cmd = os.path.join('venv_mlflow', 'bin', 'pip')
    
    print("📦 Instalando dependencias...")
    try:
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencias instaladas exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False

def verify_installation():
    """Verifica que las dependencias estén correctamente instaladas"""
    system_info = get_system_info()
    
    if system_info['is_windows']:
        python_cmd = os.path.join('venv_mlflow', 'Scripts', 'python')
    else:
        python_cmd = os.path.join('venv_mlflow', 'bin', 'python')
    
    required_packages = ['numpy', 'pandas', 'scikit-learn', 'mlflow', 'matplotlib', 'seaborn']
    
    print("\n🔍 Verificando instalación...")
    for package in required_packages:
        try:
            result = subprocess.run([python_cmd, "-c", f"import {package}; print(f'{package}: OK')"], 
                                  capture_output=True, text=True, check=True)
            print(f"  ✅ {package}: OK")
        except subprocess.CalledProcessError:
            print(f"  ❌ {package}: Error")
            return False
    
    return True

def show_next_steps():
    """Muestra los siguientes pasos para el usuario"""
    commands = get_activation_commands()
    system_info = get_system_info()
    
    print("\n" + "="*60)
    print("🎉 ¡CONFIGURACIÓN COMPLETADA!")
    print("="*60)
    
    print(f"\n📋 SIGUIENTES PASOS para {system_info['os']}:")
    print(f"1. Activar el entorno virtual:")
    print(f"   {commands['activate']}")
    
    print(f"\n2. Generar configuraciones de experimentos:")
    print(f"   {commands['python']} generate_json_configs.py")
    
    print(f"\n3. Ejecutar experimentos:")
    print(f"   {commands['python']} run_json_experiments.py")
    
    print(f"\n4. Ver resultados en MLflow:")
    print(f"   mlflow ui")
    print(f"   Abrir navegador en: http://localhost:5000")
    
    print(f"\n💡 TIP: Para desactivar el entorno virtual usa: deactivate")

def main():
    """Función principal del script de configuración"""
    print("🛠️  CONFIGURADOR DE ENTORNO PARA EXPERIMENTOS ML")
    print("="*60)
    
    # Mostrar información del sistema
    system_info = get_system_info()
    print(f"🖥️  Sistema operativo: {system_info['os']}")
    print(f"🐍 Python: {system_info['python_executable']}")
    
    # Verificar versión de Python
    if not check_python_version():
        return 1
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('requirements.txt'):
        print("\n❌ Error: No se encontró requirements.txt")
        print("   Asegúrate de estar en el directorio 'models/'")
        return 1
    
    # Crear entorno virtual
    if not create_virtual_environment():
        return 1
    
    # Instalar dependencias
    if not install_requirements():
        return 1
    
    # Verificar instalación
    if not verify_installation():
        return 1
    
    # Mostrar siguientes pasos
    show_next_steps()
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 