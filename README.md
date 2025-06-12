# TP-REDES AI/ML PLATFORMS 

Trabajo practico especial de la materia Redes de Información (72.20).
Utilizando _MLflow_ como herramienta para gestionar el ciclo de vida de modelos de Machine Learning y _Terraform_ para la infraestructura de la nube.

**Grupo 1**
- Santiago Tomás Medin - Legajo Nº 62076
- Bruno Enzo Baumgart  - Legajo Nº 62161
- Santiago José Hirsch - Legajo Nº 62169

---

## Requisitos del Sistema

### Software necesario:

Para poder levantar la infraestructura son necesarias las siguientes herramientas:
- [**Terraform**](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) 
- [**AWS CLI**](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

### Configuración

Una vez instaladas las herramientas se deben configurar la región de AWS y las claves de acceso de _AWS CLI_. Para hacer esto se deben ejecutar los siguientes comandos en la terminal:

```bash
nano ~/.aws/config
```
Dentro de este archivo se debe especificar la región en la que se desplegará la infraestructura. El contenido debe tener el siguiente formato:

```
[default]
region = <aws-region>
```

Luego, se deben configurar las claves de acceso:

```bash
nano ~/.aws/credentials
```
En este archivo se deben incluir las claves de acceso proporcionadas por el laboratorio de AWS, disponibles en **AWS Details → AWS CLI**. El formato esperado es:
```
[default]
aws_access_key_id=<aws_access_key_id>
aws_secret_access_key=<aws_secret_access_key>
aws_session_token=<aws_session_token>
```

## Ejecución

Una vez completada la [configuración](#configuración), se deben ejecutar los siguientes comandos para desplegar la infraestructura:

> **NOTA**: El laboratorio de AWS debe estar en ejecución para poder realizar el despliegue.

1. Inicializar los módulos de Terraform:
    ```bash
    terraform init
    ```

2. Revisar el plan de despliegue:
    ```bash
    terraform plan
    ```

3. Aplicar el despliegue (requiere confirmación manual con `"yes"`):
    ```bash
    terraform apply
    ```

Una vez finalizada la ejecución (puede demorar más de 5 minutos), se mostrarán dos líneas en la salida estándar:

```bash
api_gateway_endpoint = <api_gateway_endpoint>
ec2_public_ip = <ec2_public_ip>
```
Para acceder a la interfaz de gestión del ciclo de vida de los modelos de Machine Learning, ingresar a:
```
http://<ec2_public_ip>:5000
```

El valor de api_gateway_endpoint se utiliza para la integración con el Grupo 8. En particular, se puede consultar el endpoint:

`GET <api_gateway_endpoint>/metrics`

donde se exponen las métricas de las últimas ejecuciones de cada experimento registrado en _MLflow_.

## Integración de MLflow a un modelo de Machine Learning

[_MLflow_](https://mlflow.org/docs/latest/) facilita la gestión del ciclo de vida de modelos de Machine Learning. Para integrarlo en un modelo (asumiendo que esté desarrollado en Python), se deben seguir los siguientes pasos:

1. Configurar la URI del servidor de seguimiento:
    ```python
    mlflow.set_tracking_uri(uri=<tracking_uri>)
    ```

    Donde `<tracking_uri>` es la URL `http://<ec2_public_ip>:5000` previamente mencionada.

2. Definir el nombre del experimento (suele coincidir con el nombre del modelo):
    ```python
    mlflow.set_experiment(<experiment_name>)
    ```

3. Registrar métricas, parámetros y artefactos dentro de un bloque de ejecución:
    ```python
    with mlflow.start_run(run_name=<run_name>):
        mlflow.log_params(<params>)
        
        for metric_name, metric_value in metrics.items():
            mlflow.log_metric(metric_name, metric_value)
        
        mlflow.set_tag("model_type", <model_type>)
        for tag_name, tag_value in config['tags'].items():
            mlflow.set_tag(tag_name, tag_value)
        
        signature = mlflow.models.infer_signature(model_input, model_output)  
        
        mlflow.sklearn.log_model(
            sk_model=<model>,
            signature=signature,
            input_example=<input_example>,
            registered_model_name=<model_name>
        )
    ```

## Integración con Grupo 8 - Grafana con Prometheus y Loki

La integración con el Grupo 8 implicaba:
> "Modificar MLflow para exponer métricas en un formato que Prometheus pueda consumir, permitiendo su visualización en los dashboards de Grafana."

Para lograrlo, se incorporaron dos componentes en la infraestructura:
- **API Gateway**
- **Lambda Function**

La API Gateway expone un endpoint `GET /metrics`, que invoca una función Lambda encargada de recuperar las métricas de la última ejecución de cada experimento y convertirlas al formato compatible con Prometheus:
```
mlflow_<metric_name>{run_id="<run_id>"} <metric_value>
```

## Estructura del Proyecto
```
TP-REDES/
├── README.md
├── api
│   ├── api_layer.zip
│   ├── metrics.py
│   └── metrics.zip
├── main.tf
├── models
│   ├── README.md
│   ├── configs
│   ├── dataset_futbol_simulado.csv
│   ├── generate_json_configs.py
│   ├── predictor_from_json.py
│   ├── predictor_gradient_boosting_regressor.py
│   ├── predictor_linear_regression.py
│   ├── predictor_poisson_regressor.py
│   ├── predictor_random_forest_regressor.py
│   ├── requirements.txt
│   ├── run_json_experiments.py
│   ├── setup.py
│   └── setup_environment.py
├── modules
│   ├── api_gw
│   │   ├── main.tf
│   │   ├── outputs.tf
│   │   └── variables.tf
│   ├── ec2
│   │   ├── main.tf
│   │   ├── outputs.tf
│   │   ├── scripts
│   │   │   ├── mlflow-server.sh
│   │   │   └── service.txt
│   │   └── variables.tf
│   ├── lambda
│   │   ├── main.tf
│   │   ├── outputs.tf
│   │   └── variables.tf
│   ├── rds
│   │   ├── main.tf
│   │   ├── outputs.tf
│   │   └── variables.tf
│   └── vpc
│       ├── main.tf
│       ├── outputs.tf
│       └── variables.tf
├── outputs.tf
├── provider.tf
├── terraform.tfvars
├── variables.tf
└── version.tf
```