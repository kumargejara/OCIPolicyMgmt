resource "oci_identity_policy" "test_policy" {

    count = length(var.policy_sets)

    compartment_id = var.tenancy_ocid
    name = var.policy_sets[count.index].policy_name
    description = var.policy_sets[count.index].policy_description
    statements = var.policy_sets[count.index].policy_statements
}