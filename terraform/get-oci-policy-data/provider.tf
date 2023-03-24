provider oci {
	region = var.region
}

terraform {
  required_providers {
    oci = {
      source  = "oracle/oci"
      version = ">= 4.0.0"
    }
  }
  backend "local" {
  }
}
