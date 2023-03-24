data "oci_identity_policies" "test_policies" {
    compartment_id = var.tenancy_ocid
    name = var.policy_name
}

variable region { 
    type    = string
    default = "us-ashburn-1" 
}

variable compartment_ocid { 
    type    = string
    default = "ocid1.tenancy.oc1..aaaaaaaad3m5voewraokiw5gede3t3ahaz3zsuy7bs5iqecxujvedfzv3cea" 
}

variable tenancy_ocid {
    type    = string
    default = "ocid1.tenancy.oc1..aaaaaaaad3m5voewraokiw5gede3t3ahaz3zsuy7bs5iqecxujvedfzv3cea"
}

variable policy_name {
    type    = string
    default = "oci_developer_policies"
}

variable policy_statements {
    type    = list(string)
    default = ["test", "test123"]
}

output "policy_statements" {
  description = "oci policies list"
  value       = data.oci_identity_policies.test_policies.policies
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
