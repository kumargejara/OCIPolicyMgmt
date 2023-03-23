resource "oci_identity_policy" "test_policy" {
    #Required
    compartment_id = var.tenancy_ocid
    description = var.policy_description
    name = var.policy_name
    statements = var.policy_statements
}