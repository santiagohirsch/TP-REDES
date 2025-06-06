resource "aws_instance" "this" {
    ami                    = "ami-084568db4383264d4"
    instance_type          = var.instance_type
    subnet_id              = var.subnet_id
    key_name               = var.key_name
    vpc_security_group_ids = var.security_group_ids

    associate_public_ip_address = var.public
    # user_data = file("${path.module}/user_data.sh")

    tags = {
        Name = var.instance_name
    }
}