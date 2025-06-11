output "ec2_public_ip" {
    value = module.ec2_ml_flow.public_ip
}

output "api_gateway_endpoint" {
    value = aws_apigatewayv2_api.http_api.api_endpoint
}