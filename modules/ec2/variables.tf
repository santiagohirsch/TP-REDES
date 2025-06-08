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

variable "rds_username" {
  description = "Nombre de usuario de la base de datos RDS"
  type        = string
  default     = ""
}

variable "rds_password" {
  description = "Contraseña de la base de datos RDS"
  type        = string
  sensitive   = true
  default     = ""
}

variable "rds_db_name" {
  description = "Nombre de la base de datos RDS"
  type        = string
  default     = ""
}

variable "rds_endpoint" {
  description = "Endpoint de la base de datos RDS"
  type        = string
}

variable "master_server_ip" {
  description = "IP del servidor maestro"
  type        = string
  default     = ""
}