variable "name" {
  description = "Identifier for the RDS instance"
  type        = string
}

variable "instance_class" {
  description = "Instance type (e.g. db.t3.micro)"
  type        = string
}

variable "allocated_storage" {
  description = "Size in GB"
  type        = number
}

variable "db_name" {
  description = "Database name"
  type        = string
}

variable "username" {
  description = "Master DB username"
  type        = string
  sensitive   = true
}

variable "password" {
  description = "Master DB password"
  type        = string
  sensitive   = true
}

variable "subnet_ids" {
  description = "List of subnet IDs for the subnet group"
  type        = list(string)
}

variable "security_group_ids" {
  description = "List of security group IDs to attach to the RDS instance"
  type        = list(string)
}

variable "publicly_accessible" {
  description = "Whether the DB should be publicly accessible"
  type        = bool
  default     = false
}
