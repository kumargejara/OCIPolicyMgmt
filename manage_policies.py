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

def get_role_policies(policy_document, policy_tag, domain, env):
    policy_list = []
    sub_policy_tag_list = ["group-based-policies", "dynamic-group-based-policies", "other-compartment-based-policies"]
    name = policy_document[policy_tag]['name'].replace("<ENVIRONMENT>", env)
    description = policy_document[policy_tag]['description'].replace("<ENVIRONMENT>", env)
    version = policy_document[policy_tag]['version']
    for i in range(len(sub_policy_tag_list)):
        for policy in policy_document[policy_tag][sub_policy_tag_list[i]]['policy']:
            policy = policy.replace("<DOMAIN>", domain)
            policy = policy.replace("<ENVIRONMENT>", env)
            policy_list.append(policy)
    
    policySet = PolicySetObj()
    policySet.policy_name = name
    policySet.policy_description = description + ', version=' + version
    policySet.policy_statements = policy_list
    return policySet

def check_policy(policy, policylist):
    for j in range(len(policylist)):
        if policylist[j].lower() == policy.lower():
            return True
    return False

def buildvalidation():

    tenancy_policy_schema = get_schema('./schema/tenancy_json_schema.json')
    compartment_policy_schema = get_schema('./schema/compartment_json_schema.json')
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
    print("Policy Data Loaded Successfully From Source Code")
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
    print("Policy Build & Validation Process Completed Successfully")
    print("**********************************************************************************\n")

def tenancy_deployment():
    tenancy_administrator_policy_document = get_json_data(os.getcwd()+'/policies/Tenancy/Tenancy-OCI-Administrator.json')
    tenancy_billingadministrator_policy_document = get_json_data(os.getcwd()+'/policies/Tenancy/Tenancy-OCI-BillingAdministrator.json')
    tenancy_monitoringadministrator_policy_document = get_json_data(os.getcwd()+'/policies/Tenancy/Tenancy-OCI-MonitoringAdministrator.json')
    tenancy_network_administrator_global_policy_document = get_json_data(os.getcwd()+'/policies/Tenancy/Network-OCI-NetworkAdminGlobal.json')
    tenancy_administrator_policy_list = get_tenancy_policies(tenancy_administrator_policy_document, "oci-tenancy-based-policy-document")
    tenancy_billingadministrator_policy_list = get_tenancy_policies(tenancy_billingadministrator_policy_document, "oci-tenancy-based-policy-document")
    tenancy_monitoringadministrator_policy_list = get_tenancy_policies(tenancy_monitoringadministrator_policy_document, "oci-tenancy-based-policy-document")
    tenancy_network_administrator_global_policy_list = get_tenancy_policies(tenancy_network_administrator_global_policy_document, "oci-tenancy-based-policy-document")
    tenant_generic_policy_data = '[\n'+tenancy_administrator_policy_list.objtoString()+',\n'+tenancy_billingadministrator_policy_list.objtoString()+',\n'+tenancy_monitoringadministrator_policy_list.objtoString()+'\n]'
    replace_policy_list_in_tftemplate(tenant_generic_policy_data, os.getcwd()+'/policies/Tenancy/tenancy-generic-policies.tfvars.template')
    tenant_network_policy_data = '[\n'+tenancy_network_administrator_global_policy_list.objtoString()+'\n]'
    replace_policy_list_in_tftemplate(tenant_network_policy_data, os.getcwd()+'/policies/Tenancy/tenancy-network-policies.tfvars.template')
    print("**********************************************************************************")

def non_production_deployment():
    oci_auditor_environments_policy_document = get_json_data(os.getcwd()+'/policies/OCI-Auditor/OCI-Auditor-Environments.json')
    oci_operator_environments_policy_document = get_json_data(os.getcwd()+'/policies/OCI-Operator/OCI-Operator-Environments.json')
    oci_auditor_environments_policy_list = get_role_policies(oci_auditor_environments_policy_document, "oci-role-based-policy-document", domain, env)
    oci_operator_environments_policy_list = get_role_policies(oci_operator_environments_policy_document, "oci-role-based-policy-document", domain, env)
    oci_environments_policy_data = '[\n'+oci_auditor_environments_policy_list.objtoString()+',\n'+oci_operator_environments_policy_list.objtoString()+'\n]'
    replace_policy_list_in_tftemplate(oci_environments_policy_data, os.getcwd()+'/policies/oci_environments_policies.tfvars.template')
    print("**********************************************************************************")

def sandbox_deployment():
    oci_auditor_sandbox_policy_document = get_json_data(os.getcwd()+'/policies/OCI-Auditor/OCI-Auditor-Sandbox.json')
    oci_operator_sandbox_policy_document = get_json_data(os.getcwd()+'/policies/OCI-Operator/OCI-Operator-Sandbox.json')
    oci_auditor_sandbox_policy_list = get_role_policies(oci_auditor_sandbox_policy_document,  "oci-role-based-policy-document", domain, env)
    oci_operator_sandbox_policy_list = get_role_policies(oci_operator_sandbox_policy_document, "oci-role-based-policy-document", domain, env)
    oci_sandbox_policy_data = '[\n'+oci_auditor_sandbox_policy_list.objtoString()+',\n'+oci_operator_sandbox_policy_list.objtoString()+'\n]'
    replace_policy_list_in_tftemplate(oci_sandbox_policy_data, os.getcwd()+'/policies/oci_environments_policies.tfvars.template')
    print("**********************************************************************************")

def production_deployment():
    oci_auditor_production_policy_document = get_json_data(os.getcwd()+'/policies/OCI-Auditor/OCI-Auditor-Production.json')
    oci_operator_production_policy_document = get_json_data(os.getcwd()+'/policies/OCI-Operator/OCI-Operator-Production.json')
    oci_auditor_production_policy_list = get_role_policies(oci_auditor_production_policy_document, "oci-role-based-policy-document", domain, env)
    oci_operator_production_policy_list = get_role_policies(oci_operator_production_policy_document, "oci-role-based-policy-document", domain, env)
    oci_production_policy_data = '[\n'+oci_auditor_production_policy_list.objtoString()+',\n'+oci_operator_production_policy_list.objtoString()+'\n]'
    replace_policy_list_in_tftemplate(oci_production_policy_data, os.getcwd()+'/policies/oci_environments_policies.tfvars.template')
    print("**********************************************************************************")

def replace_policy_list_in_tftemplate(policy_data, tf_var_template):
    with FileInput(tf_var_template, inplace=True, backup='.bak') as f:
        for line in f:
            print(line.replace("POLICIES_OBJECT_LIST", policy_data), end='')


print("**********************************************************************************")
print("Policy As Code Process Started......")
print("**********************************************************************************")

domain = sys.argv[1]
env = sys.argv[2]
operation = sys.argv[3]

if (operation.lower()=="build-validation"):
    buildvalidation()

if (operation.lower()=="tenancy-deployment"):
    tenancy_deployment()

if (operation.lower()=="non-production-deployment"):
    non_production_deployment()

if (operation.lower()=="sandbox-deployment"):
    sandbox_deployment()

if (operation.lower()=="production-deployment"):
    production_deployment()
