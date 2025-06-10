# TP-REDES

Proyecto de Machine Learning con MLflow y infraestructura en Terraform.

## 📋 Requisitos del Sistema

### Software necesario:
- **Python 3.8+** (cualquier sistema operativo)
- **Git** para clonar el repositorio
- **Terraform** (opcional, solo para infraestructura)

### Sistemas operativos compatibles:
- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Linux (Ubuntu, CentOS, etc.)

## 🚀 Instalación y Configuración

### Opción 1: Configuración Automática (Recomendada) 🎯

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/TP-REDES.git
cd TP-REDES

# 2. Ejecutar configuración automática
cd models
python setup_environment.py
```

¡Listo! El script detecta tu sistema operativo y configura todo automáticamente.

### Opción 2: Configuración Manual

#### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/TP-REDES.git
cd TP-REDES
```

#### 2. Configurar entorno virtual

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

#### 3. Verificar instalación
```bash
python --version  # Debe ser 3.8+
pip list          # Verificar que las dependencias están instaladas
```

## 🧪 Ejecutar Experimentos de ML

### Generar configuraciones de experimentos
```bash
cd models
python generate_json_configs.py
```

### Opciones para ejecutar experimentos:

#### 1. Ejecutor interactivo (recomendado)
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

### Ver resultados en MLflow
```bash
mlflow ui
```
Luego abre tu navegador en: http://localhost:5000

## 📁 Estructura del Proyecto

```
TP-REDES/
├── models/                     # Código de Machine Learning
│   ├── configs/               # Configuraciones de experimentos (*.json - no incluido en Git)
│   ├── mlruns/               # Runs de MLflow (no incluido en Git)
│   ├── mlartifacts/          # Artefactos de MLflow (no incluido en Git)
│   ├── requirements.txt      # Dependencias de Python
│   ├── setup.py             # Configuración del proyecto
│   ├── generate_json_configs.py
│   ├── run_json_experiments.py
│   ├── predictor_from_json.py
│   ├── predictor_*.py        # Diferentes modelos
│   └── dataset_futbol_simulado.csv
├── modules/                   # Módulos de Terraform
│   ├── vpc/
│   ├── ec2/
│   └── rds/
├── *.tf                      # Archivos de Terraform
└── README.md
```

## 🔧 Solución de Problemas Comunes

### Error: "python3 no encontrado" (Windows)
- Usar `python` en lugar de `python3`
- Verificar que Python está en el PATH

### Error: "permiso denegado" (Linux/macOS)
```bash
chmod +x *.py
```

### Error: "módulo no encontrado"
- Verificar que el entorno virtual está activado
- Reinstalar dependencias: `pip install -r requirements.txt`

### MLflow UI no abre
- Verificar que está en el directorio `models/`
- Verificar puerto 5000 disponible: `lsof -i :5000` (macOS/Linux)

## 🌐 Comandos por Sistema Operativo

| Acción | Windows | macOS/Linux |
|--------|---------|-------------|
| Activar entorno | `venv_mlflow\Scripts\activate` | `source venv_mlflow/bin/activate` |
| Desactivar entorno | `deactivate` | `deactivate` |
| Python | `python` | `python3` o `python` |
| Ver procesos en puerto | `netstat -an \| findstr 5000` | `lsof -i :5000` |

## 📊 Modelos Disponibles

- **Linear Regression**: Regresión lineal básica
- **Random Forest Regressor**: Bosques aleatorios
- **Gradient Boosting Regressor**: Boosting de gradiente
- **Poisson Regressor**: Regresión de Poisson

## 🏗️ Infraestructura (Terraform)

### Requisitos adicionales:
- AWS CLI configurado
- Credenciales de AWS

### Comandos:
```bash
terraform init
terraform plan
terraform apply
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama de feature: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -m 'Agregar nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Abrir Pull Request

## 📞 Soporte

Si tienes problemas ejecutando los experimentos, verifica:
1. ✅ Python 3.8+ instalado
2. ✅ Entorno virtual activado
3. ✅ Dependencias instaladas
4. ✅ Estás en el directorio `models/`