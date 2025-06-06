output "ec2_public_ip" {
    value = module.ec2_ml_flow.public_ip
}

output "rds_endpoint" {
    value = module.rds.rds_endpoint
}

output "rds_port" {
    value = module.rds.rds_port
}