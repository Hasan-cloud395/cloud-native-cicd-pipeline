terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    # Configure with your own bucket/key/region, e.g. via `terraform init -backend-config=...`
    # bucket = "my-tfstate-bucket"
    # key    = "cloud-native-cicd-pipeline/terraform.tfstate"
    # region = "ap-south-1"
  }
}

provider "aws" {
  region = var.aws_region
}
