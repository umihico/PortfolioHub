module "acm" {
  source      = "terraform-aws-modules/acm/aws"
  domain_name = var.vars.route53.domain
  zone_id     = var.vars.route53.zone_id

  subject_alternative_names = [
    "*.${var.vars.route53.domain}",
  ]
  wait_for_validation = true
}
