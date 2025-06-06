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