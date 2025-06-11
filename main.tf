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
    {
      cidr_block        = var.private_subnet2_cidr
      availability_zone = var.private_subnet2_az
      name              = var.private_subnet2_name
      public            = false
    }
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
  rds_endpoint        = module.rds.rds_endpoint
  rds_username        = module.rds.rds_username
  rds_password        = var.rds_password
  rds_db_name         = module.rds.rds_db_name

  depends_on = [ 
    aws_key_pair.ec2,
    module.my_vpc,
    module.rds
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

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow incoming connections to MLflow server"
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
    from_port   = 5432
    to_port     = 5432
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

#########################################
###               RDS                 ###
#########################################

module "rds" {
  source              = "./modules/rds"
  name                = var.rds_instance_identifier
  instance_class      = var.rds_instance_class
  allocated_storage   = var.rds_allocated_storage
  db_name             = var.rds_db_name
  username            = var.rds_username
  password            = var.rds_password
  subnet_ids          = [module.my_vpc.subnets[var.private_subnet_name].id, 
                        module.my_vpc.subnets[var.private_subnet2_name].id]
  security_group_ids  = [aws_security_group.rds-sg.id]
  publicly_accessible = false
}

##########################################
###              Lambda                ###
##########################################

locals {
  lambda_names = var.lambda_names
  env_vars     = {
    "BASE_URL" = module.ec2_ml_flow.public_ip
  }
}

module "lambda" {
  for_each   = local.lambda_names

  name       = each.key
  source     = "./modules/lambda"
  handler    = each.value.handler
  method     = each.value.method
  env_vars   = {
    for k in each.value.env_vars : k => local.env_vars[k]
  }
  api_folder = var.api_folder
}

#########################################
###              API GW               ###
#########################################

module "apigw" {
  for_each    = var.lambda_names

  source      = "./modules/api_gw"
  name        = each.key
  lambda_arn  = module.lambda[each.key].arn
  method      = each.value.method
  api_id      = aws_apigatewayv2_api.http_api.id

  depends_on = [module.lambda]
}

resource "aws_apigatewayv2_api" "http_api" {
  name           = "http-api"
  protocol_type  = "HTTP"

  cors_configuration {
      allow_origins     = ["*"]
      allow_methods     = ["OPTIONS", "GET", "POST"]
      allow_headers     = ["Content-Type", "Authorization"]
    }
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.http_api.id
  name        = "$default"
  auto_deploy = true
}
