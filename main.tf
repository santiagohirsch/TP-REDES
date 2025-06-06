#########################################
###                VPC                ###
#########################################

module "my_vpc" {
  source   = "./modules/vpc"
  vpc_cidr = var.vpc_cidr
  vpc_name = var.vpc_name
  subnets = [
    {
      cidr_block        = var.public_subnet_cidr
      availability_zone = var.public_subnet_az
      name              = var.public_subnet_name
      public            = true
    },
    {
      cidr_block        = var.private_subnet_cidr
      availability_zone = var.private_subnet_az
      name              = var.private_subnet_name
      public            = false
    },
  ]
}

#########################################
###           EC2 Instance            ###
#########################################

module "ec2_ml_flow" {
  source              = "./modules/ec2"
  instance_type       = var.ml_flow_instance_type
  subnet_id           = module.my_vpc.subnets[var.public_subnet_name].id
  key_name            = aws_key_pair.ec2.key_name
  security_group_ids  = [aws_security_group.ec2_ml_flow-sg.id]
  instance_name       = var.ml_flow_server_name
  public              = module.my_vpc.subnets[var.public_subnet_name].public
  # rds_endpoint       = module.rds.rds_endpoint
  # rds_port           = module.rds.rds_port

  depends_on = [ 
    aws_key_pair.ec2,
    module.my_vpc
  ]
}

#########################################
###             Key Pair              ###
#########################################

resource "tls_private_key" "ec2" {
  algorithm = "RSA"
  rsa_bits  = 4096
}
# Create the Key Pair
resource "aws_key_pair" "ec2" {
  key_name   = var.ml_flow_server_name
  public_key = tls_private_key.ec2.public_key_openssh
}
# Save file
resource "local_file" "ssh_key" {
  filename        = "${aws_key_pair.ec2.key_name}.pem"
  content         = tls_private_key.ec2.private_key_pem
  file_permission = "0400"
}

#########################################
###           Security Group          ###
#########################################

resource "aws_security_group" "ec2_ml_flow-sg" {
  name        = var.ml_flow_security_group_name
  description = "allow incoming ssh connections"
  vpc_id      = module.my_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow incoming SSH connections (Linux)"
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow incoming HTTP connections"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = var.ml_flow_security_group_name
  }
}


resource "aws_security_group" "rds-sg" {
  name        = var.rds_security_group_name
  description = "Security group for RDS to allow access from EC2 master"
  vpc_id      = module.my_vpc.id

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    security_groups = [aws_security_group.ec2_ml_flow-sg.id]
    description = "Allow MySQL access from EC2 master"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = var.rds_security_group_name
  }
}