output "rds_endpoint" {
  value = aws_db_instance.this.endpoint
}

output "rds_port" {
  value = aws_db_instance.this.port
}

output "rds_username" {
  value = aws_db_instance.this.username
}

output "rds_db_name" {
  value = aws_db_instance.this.db_name
}