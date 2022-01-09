locals {
  domains = {
    prod = "portfoliohub.umihi.co"
    stg  = "stg-portfoliohub.umihi.co"
  }
}

module "zone" {
  source  = "terraform-aws-modules/route53/aws//modules/zones"
  version = "~> 2.0"

  zones = {
    "${local.domains[terraform.workspace]}" : {},
  }
}
