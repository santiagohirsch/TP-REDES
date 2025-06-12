variable "vpc_cidr" {
  type = string

}

variable "vpc_name" {
  type = string
}

variable "subnets" {
  type = list(object({
    cidr_block        = string
    availability_zone = string
    name              = string
    public            = bool
  }))
}

variable "ig_name" {
  type = string
  default = "ig"
}

variable "public_route_table_name" {
  type = string
  default = "public_route_table"
}

variable "private_route_table_name" {
  type = string
  default = "private_route_table"
}