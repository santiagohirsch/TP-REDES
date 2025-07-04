# VPC variables

variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}

variable "vpc_name" {
  type    = string
  default = "my_vpc"
}

variable "public_subnet_cidr" {
  type    = string
  default = "10.0.1.0/24"
}

variable "public_subnet_az" {
  type    = string
  default = "us-east-1a"
}

variable "public_subnet_name" {
  type    = string
  default = "ec2_public_subnet_name"
}

variable "private_subnet_cidr" {
  type    = string
  default = "10.0.2.0/24"
}

variable "private_subnet_az" {
  type    = string
  default = "us-east-1a"
}

variable "private_subnet_name" {
  type    = string
  default = "ec2_private_subnet_name"
}

variable "private_subnet2_cidr" {
  type    = string
  default = "10.0.3.0/24"
}

variable "private_subnet2_az" {
  type    = string
  default = "us-east-1b"
}

variable "private_subnet2_name" {
  type    = string
  default = "ec2_private_subnet2_name"
}

variable "ig_name" {
  type    = string
  default = "ig"
}

variable "public_route_table_name" {
  type    = string
  default = "public_route_table"
}

variable "private_route_table_name" {
  type    = string
  default = "private_route_table"
}


# EC2 instance variables

variable "ml_flow_instance_type" {
  type    = string
  default = "t2.micro"
}

variable "ml_flow_server_name" {
  type    = string
  default = "ml_flow_server"
}


# Security Group variables

variable "ml_flow_security_group_name" {
  type    = string
  default = "ec2_ml_flow-sg"
}

variable "rds_security_group_name" {
  type    = string
  default = "rds-sg"
}

# RDS variables

variable "rds_instance_identifier" { 
  default = "mlflow-db" 
}

variable "rds_instance_class" { 
  default = "db.t3.micro"
}

variable "rds_allocated_storage" {
  default = 20
}

variable "rds_db_name" { 
  default = "mlflowdb"
}

variable "rds_username" {
  default = "admin"
}

variable "rds_password" { 
  sensitive = true 
}

# API Gateway variables
variable "api_method" {
  type    = string
  default = "GET"
}

variable "api_name" {
  type    = string
  default = "mlflow-api"
}

# Lambda variables
variable "lambda_names" {
  type = map(object({
    handler = string
    method  = string
    env_vars = list(string)
  }))
}

variable "api_folder" {
  type    = string
  default = "./api"
}