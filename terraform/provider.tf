provider oci {
	region = var.region
}

provider "aws" {
  region = "us-east-1"
}

terraform {
  required_providers {
    oci = {
      source  = "oracle/oci"
      version = ">= 4.103.0"
    }
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.50.0"
    }
  }
  backend "s3" {
    bucket   = "oci-policies-tf-state"
    encrypt = true
    dynamodb_table = "oci-policies-tf-state-db"
    key      = "oci-policies-terraform.tfstate"
    region   = "us-east-1" 
  }
}

