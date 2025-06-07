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
sudo systemctl enable firewalld
sudo systemctl start firewalld
sudo firewall-cmd --permanent --add-port=5000/tcp
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload

sudo chmod 777 /home/ubuntu/mlflow.log

# Start MLflow server from the virtual environment
# nohup /home/ubuntu/mlflow-venv/bin/mlflow server --backend-store-uri postgresql://${db_user}:${db_password}@${db_endpoint}/${db_name} > /home/ubuntu/mlflow.log 2>&1 &

sudo tee /etc/systemd/system/mlflow.service > /dev/null <<EOF
${mlflow_service}
EOF

sudo tee /home/ubuntu/start-mlflow.sh > /dev/null <<EOF
#!/bin/bash
source /home/ubuntu/mlflow-venv/bin/activate
exec mlflow server --host 0.0.0.0 --port 5000
EOF

sudo chmod +x /home/ubuntu/start-mlflow.sh

sudo systemctl daemon-reload
sudo systemctl start mlflow
sudo systemctl enable mlflow
