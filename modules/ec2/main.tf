#########################################
###           EC2 INSTANCE            ###
#########################################

resource "aws_instance" "this" {
    ami                         = "ami-0731becbf832f281e"
    instance_type               = var.instance_type
    subnet_id                   = var.subnet_id
    key_name                    = var.key_name
    vpc_security_group_ids      = var.security_group_ids
    associate_public_ip_address = var.public

    user_data = templatefile("${path.module}/scripts/mlflow-server.sh", {
        db_user        = var.rds_username
        db_password    = var.rds_password
        db_endpoint    = var.rds_endpoint
        db_name        = var.rds_db_name
        mlflow_service = file("${path.module}/scripts/service.txt")
    })

    tags = {
        Name = var.instance_name
    }
}

#########################################
###             EIP                   ###
#########################################

resource "aws_eip" "this" {
    instance = aws_instance.this.id
    domain   = "vpc"

    tags = {
        Name = "${var.instance_name}-eip"
    }
}
