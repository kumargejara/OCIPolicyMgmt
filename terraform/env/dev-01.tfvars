region="us-ashburn-1" 
compartment_ocid="ocid1.tenancy.oc1..aaaaaaaad3m5voewraokiw5gede3t3ahaz3zsuy7bs5iqecxujvedfzv3cea"
tenancy_ocid="ocid1.tenancy.oc1..aaaaaaaad3m5voewraokiw5gede3t3ahaz3zsuy7bs5iqecxujvedfzv3cea"
policy_sets = [
{
policy_name="Tenancy-OCI-Administrator-Policies"
policy_description="The policy set defined for role OCI-Administrator at tenancy level for different groups"
policy_statements=[
"Allow group OCI-Administrator-CorpFunctions-Prod to use tag-namespaces in tenancy",
"Allow group OCI-Administrator-CorpFunctions-Prod to read all-resources in tenancy",
"Allow group OCI-Administrator-EngTools to use tag-namespaces in tenancy",
"Allow group OCI-Administrator-EngTools to read all-resources in tenancy",
"Allow group OCI-Administrator-Infrastructure-Prod to use tag-namespaces in tenancy",
"Allow group OCI-Administrator-Infrastructure-Prod to read all-resources in tenancy",
"Allow group OCI-Administrator-Migration to use tag-namespaces in tenancy",
"Allow group OCI-Administrator-Migration to read all-resources in tenancy",
"Allow group OCI-Administrator-PEO-Demo to use tag-namespaces in tenancy",
"Allow group OCI-Administrator-PEO-Demo to read all-resources in tenancy",
"Allow group OCI-Administrator-PEO-Dev to use tag-namespaces in tenancy",
"Allow group OCI-Administrator-PEO-Dev to read all-resources in tenancy",
"Allow group OCI-Administrator-PEO-LiteR to use tag-namespaces in tenancy",
"Allow group OCI-Administrator-PEO-LiteR to read all-resources in tenancy",
"Allow group OCI-Administrator-PEO-Prod to use tag-namespaces in tenancy",
"Allow group OCI-Administrator-PEO-Prod to read all-resources in tenancy",
"Allow group OCI-Administrator-PEO-QE to use tag-namespaces in tenancy",
"Allow group OCI-Administrator-PEO-QE to read all-resources in tenancy",
"Allow group OCI-Administrator-PEO-SDLC to use tag-namespaces in tenancy",
"Allow group OCI-Administrator-PEO-SDLC to read all-resources in tenancy",
"Allow group OCI-Administrator-Sandbox to use tag-namespaces in tenancy",
"Allow group OCI-Administrator-Sandbox to read all-resources in tenancy",
"Allow group OCI-Administrator-SharedServices-Prod to use tag-namespaces in tenancy",
"Allow group OCI-Administrator-SharedServices-Prod to read all-resources in tenancy"
]
},
{
policy_name="Tenancy-OCI-BillingAdministrator-Policies"
policy_description="The policy set defined for role OCI-Administrator at tenancy level for different groups"
policy_statements=[
"Allow group OCI-BillingAdmin-Master to read computed-usages in tenancy",
"Allow group OCI-BillingAdmin-Master to read subscribed-services in tenancy",
"Allow group OCI-BillingAdmin-Master to manage accountmanagement-family in tenancy",
"Allow group OCI-BillingAdmin-Master to manage tickets in tenancy",
"Allow group OCI-BillingAdmin-Master to manage invoices in tenancy",
"Allow group OCI-BillingAdmin-Master to manage invoice-preferences in tenancy",
"Allow group OCI-BillingAdmin-Master to read subscription in tenancy",
"Allow group OCI-BillingAdmin-Master to read billing-schedules in tenancy",
"Allow group OCI-BillingAdmin-Master to read subscribed-services in tenancy",
"Allow group OCI-BillingAdmin-Master to read rate-cards in tenancy",
"Allow group OCI-BillingAdmin-Master to read usage-reports in tenancy"
]
},
{
policy_name="Tenancy-OCI-MonitoringAdministrator-Policies"
policy_description="The policy set defined for role OCI-Administrator at tenancy level for different groups"
policy_statements=[
"Allow group OCI-MonitorAdmin-Global to inspect all-resources in tenancy",
"Allow group OCI-MonitorAdmin-Global to read instances in tenancy",
"Allow group OCI-MonitorAdmin-Global to read audit-events in tenancy",
"Allow group OCI-MonitorAdmin-Global to inspect alarms in tenancy",
"Allow group OCI-MonitorAdmin-Global to read metrics in tenancy",
"Allow group OCI-MonitorAdmin-Global to use streams in tenancy",
"Allow group OCI-MonitorAdmin-Global to inspect logging-family in tenancy",
"Allow group OCI-MonitorAdmin-Global to read database-family in tenancy",
"Allow group OCI-MonitorAdmin-Global to use metrics in tenancy",
"Allow group OCI-MonitorAdmin-Global to manage alarm in tenancy",
"Allow group OCI-MonitorAdmin-Global to manage ons-topics in tenancy",
"Allow group OCI-MonitorAdmin-Global to use buckets in tenancy",
"Allow group OCI-MonitorAdmin-Global to use objects in tenancy"
]
}
]