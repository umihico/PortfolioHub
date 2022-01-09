module "route53" {
  source = "./route53"
}

module "acm" {
  source = "./acm"
  vars   = { route53 : module.route53.all }
}

module "acm_us" {
  source = "./acm"
  vars   = { route53 : module.route53.all }
  providers = {
    aws = aws.us
  }
}

module "apigateway" {
  source = "./apigateway"
  vars = {
    route53 : module.route53.all
    acm : module.acm.all
  }
}
