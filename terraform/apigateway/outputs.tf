output "all" {
  value = {
    api_gws : data.aws_apigatewayv2_apis.api_gws,
  }
}
