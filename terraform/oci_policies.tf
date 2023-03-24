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

resource "oci_objectstorage_bucket" "test_bucket" {
    compartment_id = "ocid1.compartment.oc1..aaaaaaaaoorr4zezczh4zsq2kcngjbeic7d66eh5xfifkid2gth4kcxwirra"
    name = "my_sample_test_bucket123999"
    namespace = "idlbk5tfnj1l"
}

output "policy_list" {
  description = "oci policies list"
  value       = data.oci_identity_policies.test_policies.policies
}
