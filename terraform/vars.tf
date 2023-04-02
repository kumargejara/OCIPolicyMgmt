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

variable "policy_sets" {
    type = list(object({
        policy_name  = string,
        policy_description = string,
        policy_statements = list(string)
    }))
    default = []
}
