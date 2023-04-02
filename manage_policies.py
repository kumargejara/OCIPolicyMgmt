import json
import jsonschema
from jsonschema import validate
import os
from fileinput import FileInput
import sys

# define a class
class PolicySetObj:
    # define an attribute
    policy_name = ""
    policy_description = ""
    policy_statements = [""]
  
    def __init__(self, name = ""):
        self.policy_name = name

    def objtoString(self):
        strData = "{\n"
        strData = strData + 'policy_name="' + self.policy_name
        strData = strData + '"\n'
        strData = strData + 'policy_description="' + self.policy_description
        strData = strData + '"\n'
        strData = strData + 'policy_statements=[\n'
        for i in range(0, len(self.policy_statements)):
            if (i+1==len(self.policy_statements)):
                strData = strData + '"' + self.policy_statements[i] +'"'
            else:
                strData = strData + '"' + self.policy_statements[i] +'",\n'
        strData = strData + "\n]\n"
        strData = strData + "}"
        return strData

def get_schema(file_name):
    with open(file_name, 'r') as file:
        schema = json.load(file)
    return schema

def get_json_data(file_name):
    with open(file_name, 'r') as file:
        json_data = json.load(file)
    return json_data

def validate_json(json_data, json_schema, schemaType):

    try:
        validate(instance=json_data, schema=json_schema)
    except jsonschema.exceptions.ValidationError as err:
        print(err)
        err = "Given Json Policy data is InValid with "+ schemaType
        return False, err

    message = "Given Json Policy data is Valid with "+ schemaType
    return True, message

def get_tenancy_policies(policy_document, policy_tag):
    policy_list = []
    name = policy_document[policy_tag]['name'].replace("<ENVIRONMENT>", env)
    description = policy_document[policy_tag]['description'].replace("<ENVIRONMENT>", env)
    version = policy_document[policy_tag]['version']
    for policy in policy_document[policy_tag]['policy']:
        policy_list.append(policy)

    policySet = PolicySetObj()
    policySet.policy_name = name
    policySet.policy_description = description + ', version=' + version
    policySet.policy_statements = policy_list
    return policySet

def get_role_policies(policy_document, policy_tag, sub_policy_tag, domain, env):
    policy_list = []
    name = policy_document[policy_tag]['name'].replace("<ENVIRONMENT>", env)
    description = policy_document[policy_tag]['description'].replace("<ENVIRONMENT>", env)
    version = policy_document[policy_tag]['version']
    for policy in policy_document[policy_tag][sub_policy_tag]['policy']:
        policy = policy.replace("<DOMAIN>", domain)
        policy = policy.replace("<ENVIRONMENT>", env)
        policy_list.append(policy)
    
    description = description + ', version=' + version
    return name, description, policy_list


def check_policy(policy, policylist):
    for j in range(len(policylist)):
        if policylist[j].lower() == policy.lower():
            return True
    return False

def replace_policy_list_in_tftemplate(policy_data, tf_var_template):
    with FileInput(tf_var_template, inplace=True, backup='.bak') as f:
        for line in f:
            print(line.replace("POLICIES_OBJECT_LIST", policy_data), end='')



print("\n**********************************************************************************")
print("Policy Data Loaded Successfully From Source Code")
print("**********************************************************************************\n")
tenancy_policy_schema = get_schema('./schema/tenancy_json_schema.json')
compartment_policy_schema = get_schema('./schema/compartment_json_schema.json')

domain = sys.argv[1]
env = sys.argv[2]

tenancy_administrator_policy_document = get_json_data(os.getcwd()+'/policies/Tenancy/Tenancy-OCI-Administrator.json')
tenancy_billingadministrator_policy_document = get_json_data(os.getcwd()+'/policies/Tenancy/Tenancy-OCI-BillingAdministrator.json')
tenancy_monitoringadministrator_policy_document = get_json_data(os.getcwd()+'/policies/Tenancy/Tenancy-OCI-MonitoringAdministrator.json')
tenancy_network_administrator_global_policy_document = get_json_data(os.getcwd()+'/policies/Tenancy/Network-OCI-NetworkAdminGlobal.json')

oci_auditor_environments_policy_document = get_json_data(os.getcwd()+'/policies/OCI-Auditor/OCI-Auditor-Environments.json')
oci_auditor_sandbox_policy_document = get_json_data(os.getcwd()+'/policies/OCI-Auditor/OCI-Auditor-Sandbox.json')
oci_auditor_production_policy_document = get_json_data(os.getcwd()+'/policies/OCI-Auditor/OCI-Auditor-Production.json')

oci_operator_environments_policy_document = get_json_data(os.getcwd()+'/policies/OCI-Operator/OCI-Operator-Environments.json')
oci_operator_sandbox_policy_document = get_json_data(os.getcwd()+'/policies/OCI-Operator/OCI-Operator-Sandbox.json')
oci_operator_production_policy_document = get_json_data(os.getcwd()+'/policies/OCI-Operator/OCI-Operator-Production.json')

print("\n**********************************************************************************")
print("Policy Schema Loaded Successfully From Json Schema Files")
print("**********************************************************************************\n")


is_valid, msg = validate_json(tenancy_administrator_policy_document, tenancy_policy_schema, "Tenancy OCI-Administrator Schema")
print(msg) 
is_valid, msg = validate_json(tenancy_billingadministrator_policy_document, tenancy_policy_schema, "Tenancy OCI-BillingAdministrator Schema")
print(msg)
is_valid, msg = validate_json(tenancy_monitoringadministrator_policy_document, tenancy_policy_schema, "Tenancy OCI-MonitoringAdministrator Schema")
print(msg)
is_valid, msg = validate_json(tenancy_network_administrator_global_policy_document, tenancy_policy_schema, "Tenancy Network-OCI-NetworkAdmin Schema")
print(msg)

is_valid, msg = validate_json(oci_auditor_environments_policy_document, compartment_policy_schema, "OCI-Auditor Environment Schema")
print(msg) 
is_valid, msg = validate_json(oci_auditor_sandbox_policy_document, compartment_policy_schema, "OCI-Auditor Sandbox Schema")
print(msg)
is_valid, msg = validate_json(oci_auditor_production_policy_document, compartment_policy_schema, "OCI-Auditor Production Schema")
print(msg)

is_valid, msg = validate_json(oci_operator_environments_policy_document, compartment_policy_schema, "OCI-Operator Environment Schema")
print(msg) 
is_valid, msg = validate_json(oci_operator_sandbox_policy_document, compartment_policy_schema, "OCI-Operator Sandbox Schema")
print(msg)
is_valid, msg = validate_json(oci_operator_production_policy_document, compartment_policy_schema, "OCI-Operator Production Schema")
print(msg)

print("\n**********************************************************************************")
print("Policy Validation Process Completed Successfully")
print("**********************************************************************************\n")


tenancy_administrator_policy_list = get_tenancy_policies(tenancy_administrator_policy_document, "oci-tenancy-based-policy-document")
tenancy_billingadministrator_policy_list = get_tenancy_policies(tenancy_billingadministrator_policy_document, "oci-tenancy-based-policy-document")
tenancy_monitoringadministrator_policy_list = get_tenancy_policies(tenancy_monitoringadministrator_policy_document, "oci-tenancy-based-policy-document")
tenancy_network_administrator_global_policy_list = get_tenancy_policies(tenancy_network_administrator_global_policy_document, "oci-tenancy-based-policy-document")

print("**********************************************************************************")
tenant_generic_policy_data = '[\n'+tenancy_administrator_policy_list.objtoString()+',\n'+tenancy_billingadministrator_policy_list.objtoString()+',\n'+tenancy_monitoringadministrator_policy_list.objtoString()+'\n]'
replace_policy_list_in_tftemplate(tenant_generic_policy_data, os.getcwd()+'/policies/Tenancy/tenancy-generic-policies.tfvars.template')
tenant_network_policy_data = '[\n'+tenancy_network_administrator_global_policy_list.objtoString()+'\n]'
replace_policy_list_in_tftemplate(tenant_network_policy_data, os.getcwd()+'/policies/Tenancy/tenancy-network-policies.tfvars.template')
print("**********************************************************************************")




'''oci_auditor_environments_policy_list = get_role_policies(oci_auditor_environments_policy_list, oci_auditor_environments_policy_document, domain, env)
print(oci_auditor_environments_policy_list)
print("**********************************************************************************")
oci_auditor_sandbox_policy_list = get_role_policies(oci_auditor_sandbox_policy_list, oci_auditor_sandbox_policy_document, domain, env)
print(oci_auditor_sandbox_policy_list)
print("**********************************************************************************")
oci_auditor_production_policy_list = get_role_policies(oci_auditor_production_policy_list, oci_auditor_production_policy_document, domain, env)
print(oci_auditor_production_policy_list)
print("**********************************************************************************")

oci_operator_environments_policy_list = get_role_policies(oci_operator_environments_policy_list, oci_operator_environments_policy_document, domain, env)
print(oci_operator_environments_policy_list)
print("**********************************************************************************")
oci_operator_sandbox_policy_list = get_role_policies(oci_operator_sandbox_policy_list, oci_operator_sandbox_policy_document, domain, env)
print(oci_operator_sandbox_policy_list)
print("**********************************************************************************")
oci_operator_production_policy_list = get_role_policies(oci_operator_production_policy_list, oci_operator_production_policy_document, domain, env)
print(oci_operator_production_policy_list)
print("**********************************************************************************")


print("**********************************************************************************")
print("Policy Build Process Completed Successfully")
print("**********************************************************************************\n")'''

'''existing_policy_count=0
new_policy_count = 0
new_policy_list = []
for i in range(len(policy_list)):
    if check_policy(policy_list[i], existing_policy_list):
        existing_policy_count = existing_policy_count+1
    else:
        new_policy_list.append(policy_list[i])
        new_policy_count = new_policy_count+1

remove_policy_list = []
policy_not_changed_count=0
policy_removed_updated_count = 0
for k in range(len(existing_policy_list)):
    if check_policy(existing_policy_list[k], policy_list):
        policy_not_changed_count = policy_not_changed_count+1
    else:
        remove_policy_list.append(existing_policy_list[k])
        policy_removed_updated_count = policy_removed_updated_count+1


write_new_policies(os.getcwd()+'/policies/new_policy_state.json', policy_list)
print("Policy Summary Report")
print("**********************************************************************************")
print(f"Current Policies Not Changed = {policy_not_changed_count}")
print(f"Current Policies Removed/Altered = {policy_removed_updated_count}")
print(f"New Policies Will Be Added  = {new_policy_count}")
print(f"Total Policies List = {existing_policy_count+new_policy_count}")
print(f"Total Policies List Recheck = {len(policy_list)}")
print("**********************************************************************************\n")
replace_policy_list_in_tftemplate(os.getcwd()+'/policies/new_policy_state.json')'''