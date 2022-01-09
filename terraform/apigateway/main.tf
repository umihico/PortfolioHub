data "aws_apigatewayv2_apis" "api_gws" {
  name          = "${terraform.workspace}-portfoliohub"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_domain_name" "domain" {
  domain_name = var.vars.route53.domain

  domain_name_configuration {
    certificate_arn = var.vars.acm.acm_certificate_arn
    endpoint_type   = "REGIONAL"
    security_policy = "TLS_1_2"
  }
}

resource "aws_apigatewayv2_api_mapping" "domain" {
  api_id      = one(data.aws_apigatewayv2_apis.api_gws.ids)
  domain_name = aws_apigatewayv2_domain_name.domain.domain_name
  stage       = "$default"
}

resource "aws_route53_record" "domain" {
  name    = aws_apigatewayv2_domain_name.domain.domain_name
  type    = "A"
  zone_id = var.vars.route53.zone_id

  alias {
    evaluate_target_health = true
    name                   = aws_apigatewayv2_domain_name.domain.domain_name_configuration[0].target_domain_name
    zone_id                = aws_apigatewayv2_domain_name.domain.domain_name_configuration[0].hosted_zone_id
  }
}
