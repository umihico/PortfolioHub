output "all" {
  value = {
    zone_detail : module.zone,
    zone_id : values(module.zone.route53_zone_zone_id)[0]
    domain : keys(module.zone.route53_zone_zone_id)[0]
  }
}
