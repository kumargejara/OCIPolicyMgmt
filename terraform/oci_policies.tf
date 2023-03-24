resource "oci_identity_policy" "test_policy" {
    compartment_id = var.tenancy_ocid
    description = var.policy_description
    name = var.policy_name
    statements = var.policy_statements
}

data "oci_identity_policies" "test_policies" {
    compartment_id = var.tenancy_ocid
    name = var.policy_name
}

output "policy_list" {
  description = "oci policies list"
  value       = data.oci_identity_policies.test_policies.policies
}
