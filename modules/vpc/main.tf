#########################################
###                VPC                ###
#########################################

resource "aws_vpc" "this" {
  cidr_block = var.vpc_cidr
  tags = {
    Name = var.vpc_name
  }
}

#########################################
###               SUBNET              ###
#########################################

resource "aws_subnet" "this" {
  for_each          = { for subnet in var.subnets : subnet.name => subnet }
  vpc_id            = aws_vpc.this.id
  cidr_block        = each.value.cidr_block
  availability_zone = each.value.availability_zone
  tags = {
    Name = each.value.name
  }
}

#########################################
###                IGW                ###
#########################################

resource "aws_internet_gateway" "this" {
  vpc_id = aws_vpc.this.id

  tags = {
    Name = var.ig_name
  }
}

#########################################
###            ROUTE TABLE            ###
#########################################

resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.this.id

  tags = {
    Name = var.public_route_table_name
  }
}

resource "aws_route_table" "private_route_table" {
  vpc_id = aws_vpc.this.id

  tags = {
    Name = var.private_route_table_name
  }
}

resource "aws_route" "public_route" {
  route_table_id         = aws_route_table.public_route_table.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.this.id
}

locals {
  subnets_map = {
    for subnet in var.subnets : subnet.name => subnet
  }

  public_subnet_ids = [
    for name, subnet in aws_subnet.this :
    subnet.id if local.subnets_map[name].public
  ]

  private_subnet_ids = [
    for name, subnet in aws_subnet.this :
    subnet.id if !local.subnets_map[name].public
  ]
}

resource "aws_route_table_association" "public_subnet_association" {
  for_each = {
    for name, subnet in aws_subnet.this :
    name => subnet
    if local.subnets_map[name].public
  }

  subnet_id      = each.value.id
  route_table_id = aws_route_table.public_route_table.id
}

resource "aws_route_table_association" "private_subnet_association" {
  for_each = {
    for name, subnet in aws_subnet.this :
    name => subnet
    if !local.subnets_map[name].public
  }

  subnet_id      = each.value.id
  route_table_id = aws_route_table.private_route_table.id
}

#########################################
###            NAT Gateway            ###
#########################################

resource "aws_eip" "nat_gw" {
  count  = var.enable_nat_gateway ? 1 : 0
  domain = "vpc"

  tags = {
    Name = "${var.vpc_name}-nat-eip"
  }
}

resource "aws_nat_gateway" "this" {
  count         = var.enable_nat_gateway ? 1 : 0
  allocation_id = aws_eip.nat_gw[0].id
  subnet_id     = local.public_subnet_ids[0]   # <--- use computed public subnet inside module!

  tags = {
    Name = "${var.vpc_name}-nat-gw"
  }
}

resource "aws_route" "private_nat_route" {
  count                   = var.enable_nat_gateway ? 1 : 0
  route_table_id          = aws_route_table.private_route_table.id
  destination_cidr_block  = "0.0.0.0/0"
  nat_gateway_id          = aws_nat_gateway.this[0].id
}