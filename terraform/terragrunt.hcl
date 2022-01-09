remote_state {
  backend = "s3"
  generate = {
    path              = "backend.tf"
    if_exists         = "overwrite"
    disable_signature = true
  }
  config = {
    profile              = "portfoliohub"
    region               = "ap-northeast-1"
    bucket               = "terraform-states-${run_cmd("aws", "sts", "get-caller-identity", "--profile", "portfoliohub", "--query", "Account", "--output", "text")}-portfoliohub"
    key                  = "${path_relative_to_include()}/terraform.tfstate"
    encrypt              = true
    workspace_key_prefix = "workspaces"
    dynamodb_table       = "terraform-lock-table-${run_cmd("aws", "sts", "get-caller-identity", "--profile", "portfoliohub", "--query", "Account", "--output", "text")}"
  }
}

generate "provider" {
  path              = "generated.tf"
  if_exists         = "overwrite"
  disable_signature = true
  contents          = <<EOF
provider "aws" {
  profile               = "portfoliohub"
  region = "ap-northeast-1"
}

provider "aws" {
  alias  = "us"
  region = "us-east-1"
  profile               = "portfoliohub"
}
EOF
}