import requests
import os

# Endpoints
BASE_URL = os.getenv("BASE_URL")
experiments_url = f"http://{BASE_URL}:5000/api/2.0/mlflow/experiments/search"
runs_url = f"http://{BASE_URL}:5000/api/2.0/mlflow/runs/search"

# Optional: Query parameters
params = {
    "max_results": 8
}

def metrics_handler(event, context):
    """
    This handler takes the data from the mlflow api and return data in a format to be consumed by prometheus.
    """

    response = requests.get(experiments_url, params=params)

    if response.status_code != 200:
        raise Exception(f"Failed to get experiments: {response.text}")

    experiments = response.json().get("experiments", [])

    if not experiments:
        raise Exception("No experiments found.")   
    
    experiments = [exp for exp in experiments if exp['name'] != "Default"]
    experiment_ids = [exp['experiment_id'] for exp in experiments]

    body = {
        "experiment_ids": experiment_ids
    }
    runs_response = requests.post(runs_url, json=body)
    if runs_response.status_code != 200:
        raise Exception(f"Failed to get runs: {runs_response.text}")

    runs = runs_response.json().get("runs", [])

    latest_runs = {}
    for run in runs:
        info = run["info"]
        exp_id = info["experiment_id"]
        end_time = int(info.get("end_time", 0))

        if exp_id not in latest_runs or end_time > int(latest_runs[exp_id]["info"].get("end_time", 0)):
            latest_runs[exp_id] = run

    prometheus_metrics = []
    for exp_id, run in latest_runs.items():
        run_id = run["info"]["run_id"]
        metrics = run.get("data", {}).get("metrics", [])

        for metric in metrics:
            key = metric["key"]
            value = metric["value"]
            line = f'mlflow_{key}{{run_id="{run_id}"}} {value}'
            prometheus_metrics.append(line)

    return "\n".join(prometheus_metrics)