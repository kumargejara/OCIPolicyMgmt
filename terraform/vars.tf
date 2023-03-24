
variable region { 
    type    = string
    default = "us-ashburn-1" 
}
variable compartment_ocid { 
    type    = string
    default = "ocid1.compartment.oc1..aaaaaaaayxtqh4ur2ivznam3l4mjzg26wcytdujml4bm5rxfxznbxoqcbpra" 
}

variable tenancy_ocid {
    type    = string
    default = "test_instance_demo4"
}

variable policy_name {
    type    = string
    default = "oci_developer_policies"
}

variable policy_description {
    type    = string
    default = "This policy set defined for oci developer"
}

variable policy_statements {
    type    = list(string)
    default = [
"Allow group sandbox_group to use tag-namespaces in tenancy",
"Allow group sandbox_group to inspect tag-namespaces in tenancy",
"Allow group sandbox_group to read tag-namespaces in tenancy",
"Allow group sandbox_group to read app-catalog-listing in tenancy",
"Allow group dev_group to use tag-namespaces in tenancy",
"Allow group dev_group to inspect tag-namespaces in tenancy",
"Allow group dev_group to read tag-namespaces in tenancy",
"Allow group dev_group to read app-catalog-listing in tenancy",
"Allow group prod_group to use tag-namespaces in tenancy",
"Allow group prod_group to inspect tag-namespaces in tenancy",
"Allow group prod_group to read tag-namespaces in tenancy",
"Allow group prod_group to read app-catalog-listing in tenancy",
"Allow dynamic-group dev_dynamic_group1 to use tag-namespaces in tenancy",
"Allow dynamic-group dev_dynamic_group1 to inspect tag-namespaces in tenancy",
"Allow dynamic-group dev_dynamic_group1 to read tag-namespaces in tenancy",
"Allow dynamic-group dev_dynamic_group1 to read app-catalog-listing in tenancy",
"Allow group sandbox_group to use tag-namespaces in tenancy",
"Allow group sandbox_group to use instances in compartment sandbox",
"Allow group sandbox_group to use instance-images in compartment sandbox",
"Allow group sandbox_group to inspect instance-images in compartment sandbox",
"Allow group dev_group to use instances in compartment sandbox",
"Allow group dev_group to use instance-images in compartment sandbox",
"Allow group dev_group to inspect instance-images in compartment sandbox",
"Allow group prod_group to use instances in compartment sandbox",
"Allow group prod_group to use instance-images in compartment sandbox",
"Allow group prod_group to inspect instance-images in compartment sandbox",
"Allow dynamic-group dev_dynamic_group1 to use instances in compartment development",
"Allow dynamic-group dev_dynamic_group1 to use instance-images in compartment development",
"Allow dynamic-group dev_dynamic_group1 to inspect instance-images in compartment development",
"Allow group sandbox_group to use tag-namespaces in compartment development",
"Allow any-user to use tag-namespaces in compartment development"
]
}

variable policy_list {
    type    = list(string)
    default = ["test", "test123"]
}
