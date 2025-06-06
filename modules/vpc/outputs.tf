output "subnets" {
  description = "Map of subnet name to its id and public flag"
  value = {
    for k, subnet in var.subnets :
    subnet.name => {
      id     = aws_subnet.this[subnet.name].id
      public = subnet.public
    }
  }
}

output "id" {
  value = aws_vpc.this.id
}