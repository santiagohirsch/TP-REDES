#!/bin/bash

# Update system
sudo apt update -y
sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3 python3-pip python3-venv firewalld

# Create a virtual environment for MLflow
python3 -m venv /home/ubuntu/mlflow-venv
source /home/ubuntu/mlflow-venv/bin/activate

# Upgrade pip inside the venv and install MLflow
pip install --upgrade pip
pip install mlflow psycopg2-binary

# Start and configure firewall
systemctl enable firewalld
systemctl start firewalld
firewall-cmd --permanent --add-port=5000/tcp
firewall-cmd --permanent --add-service=http
firewall-cmd --permanent --add-service=https
firewall-cmd --reload

# Start MLflow server from the virtual environment
nohup /home/ubuntu/mlflow-venv/bin/mlflow server \
  --backend-store-uri postgresql://${db_user}:${db_password}@${db_endpoint}/${db_name} > /home/ubuntu/mlflow.log 2>&1 &
