variable "instance_name" {
  type = string
}

variable "instance_type" {
  type    = string
  default = "t2.small"
}

variable "subnet_id" {
  type = string
}

variable "public" {
  type = bool
}

variable "key_name" {
  type = string
}

variable "security_group_ids" {
  type    = list(string)
  default = []
}

/*variable "user_data_path" {
  type = string
}*/

variable "rds_endpoint" {
  description = "Endpoint de la base de datos RDS"
  type        = string
  default     = ""
}

variable "rds_port" {
  description = "Puerto de la base de datos RDS"
  type        = number
  default     = 3306
}

variable "master_server_ip" {
  description = "IP del servidor maestro"
  type        = string
  default     = ""
}