output "all" {
  value = {
    route53 : module.route53.all,
    acm : module.acm.all,
    acm_us : module.acm_us.all,
    apigateway : module.apigateway.all,
  }
}
