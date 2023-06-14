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

def getOCIIDForGroup(name):
        os.system('oci iam group list --name "'+name+'" >'+os.getcwd()+'/policies/OCI-Privilege/'+name+'.json')
        oci_group_json = get_json_data(os.getcwd()+'/policies/OCI-Privilege/'+name+'.json')
        group_oci_id = oci_group_json["data"][0]
        return group_oci_id["id"]

def getOCIID(name):
    os.system('oci iam user list --all > '+os.getcwd()+'/policies/OCI-Privilege/all_users.json')
    oci_user_json = get_json_data(os.getcwd()+'/policies/OCI-Privilege/all_users.json')
    for k in range(len(oci_user_json["data"])):
        user_record = oci_user_json["data"][k]
        if (user_record["email"]==name):
            return user_record["id"]
    return "null"

def getOCIIDforUserIds(userid_list):
    data = '['
    for i in range(0, len(userid_list)):    
        data = data +'"'+getOCIID(userid_list[i])+'",'
    data = data + ']'
    return data.replace(',]', "]")


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

def replace_user_group_ids_in_tf(group_id, user_id_list, policy_group_id, tf_template_file, new_tf_file):
    new_tf_file = new_tf_file.replace(".tf", policy_group_id+".tf")
    print(new_tf_file)
    os.system('cp '+tf_template_file+' '+new_tf_file)
    with FileInput(new_tf_file, inplace=True) as f:
        for line in f:
            print(line.replace("OCI_IDENTITY_GROUP_ID", '"'+getOCIIDForGroup(group_id)+'"').replace("<INDEX>", policy_group_id).replace("OCI_IDENTITY_USER_ID_LIST", getOCIIDforUserIds(user_id_list)), end='')

def get_privilege_role_policies(oci_privilege_policy_inputs, policy_document, policy_tag, domain, env):
    sub_policy_tag_list = ["group-based-policies"]
    policySetList = '[\n'
    for k in range(len(oci_privilege_policy_inputs["policy_deployment_list"])):
        policy_input = oci_privilege_policy_inputs["policy_deployment_list"][k]
        policy_list = []
        if (policy_input["start-time-utc"]!="not_active"):
            start_time_utc = policy_input["start-time-utc"]
            end_time_utc = policy_input["end-time-utc"]
            policy_group_id = policy_input["policy_group_id"]
            purpose = policy_input["purpose"]
            user_list = policy_input["user_email_id"]
            group = policy_document[policy_tag]['role'].replace("<DOMAIN>", domain).replace("<GROUP_ID>", policy_group_id)
            name = policy_document[policy_tag]['name'].replace("<ENVIRONMENT>", env).replace("<GROUP_ID>", policy_group_id).replace("<DOMAIN>", domain).replace("<END-TIME-UTC>", end_time_utc.lower()).replace(":", "-")
            description = policy_document[policy_tag]['description'].replace("<ENVIRONMENT>", env).replace("<PURPOSE>", purpose)
            version = policy_document[policy_tag]['version']
            oci_user_group_tf_template = os.getcwd()+'/policies/OCI-Privilege/user_group_membership.tf.template'
            oci_user_group_tf_file = os.getcwd()+'/terraform/user_group_membership.tf'
            replace_user_group_ids_in_tf(group, user_list, policy_group_id, oci_user_group_tf_template, oci_user_group_tf_file)
            for i in range(len(sub_policy_tag_list)):
                for policy in policy_document[policy_tag][sub_policy_tag_list[i]]['policy']:
                    policy = policy.replace("<DOMAIN>", domain).replace("<GROUP_ID>", policy_group_id).replace("<ENVIRONMENT>", env).replace("<START_TIME_UTC>", start_time_utc).replace("<END_TIME_UTC>", end_time_utc)
                    policy_list.append(policy)
    
            policySet = PolicySetObj()
            policySet.policy_name = name
            policySet.policy_description = description + ', version=' + version
            policySet.policy_statements = policy_list
            policySetList = policySetList+policySet.objtoString()+','

    policySetList = policySetList+'\n]'
    return policySetList.replace(",\n]", "\n]")

def get_policy_name(policy_document, policy_tag, env):
    name = policy_document[policy_tag]['name'].replace("<ENVIRONMENT>", env)
    return name

def get_privilege_policy_name(policy_document, policy_tag, env, end_time_utc):
    name = policy_document[policy_tag]['name'].replace("<DOMAIN>", domain).replace("<ENVIRONMENT>", env).replace("-<GROUP_ID>", "").replace("-<END-TIME-UTC>", "")
    return name

def check_policy(policy, policylist):
    for j in range(len(policylist)):
        if policylist[j].lower() == policy.lower():
            return True
    return False

def tenancy_build_validation():

    tenancy_policy_schema = get_schema(os.getcwd()+'/schema/tenancy_json_schema.json')
    tenancy_administrator_policy_document = get_json_data(os.getcwd()+'/policies/Tenancy/Tenancy-OCI-Administrator.json')
    tenancy_billingadministrator_policy_document = get_json_data(os.getcwd()+'/policies/Tenancy/Tenancy-OCI-BillingAdministrator.json')
    tenancy_monitoringadministrator_policy_document = get_json_data(os.getcwd()+'/policies/Tenancy/Tenancy-OCI-MonitoringAdministrator.json')
    tenancy_network_administrator_global_policy_document = get_json_data(os.getcwd()+'/policies/Tenancy/Network-OCI-NetworkAdminGlobal.json')
    
    print("\n**********************************************************************************")
    print("Tenancy Policy Data Loaded Successfully From Source Code")
    print("**********************************************************************************\n")
    is_valid, msg = validate_json(tenancy_administrator_policy_document, tenancy_policy_schema, "Tenancy OCI-Administrator Schema")
    print(msg) 
    is_valid, msg = validate_json(tenancy_billingadministrator_policy_document, tenancy_policy_schema, "Tenancy OCI-BillingAdministrator Schema")
    print(msg)
    is_valid, msg = validate_json(tenancy_monitoringadministrator_policy_document, tenancy_policy_schema, "Tenancy OCI-MonitoringAdministrator Schema")
    print(msg)
    is_valid, msg = validate_json(tenancy_network_administrator_global_policy_document, tenancy_policy_schema, "Tenancy Network-OCI-NetworkAdmin Schema")
    print(msg)

    print("\n**********************************************************************************")
    print("Tenancy Policy Build & Validation Process Completed Successfully")
    print("**********************************************************************************\n")

def auditor_build_validation():

    compartment_policy_schema = get_schema(os.getcwd()+'/schema/compartment_json_schema.json')
    oci_auditor_environments_policy_document = get_json_data(os.getcwd()+'/policies/OCI-Auditor/OCI-Auditor-Environments.json')
    oci_auditor_sandbox_policy_document = get_json_data(os.getcwd()+'/policies/OCI-Auditor/OCI-Auditor-Sandbox.json')
    oci_auditor_production_policy_document = get_json_data(os.getcwd()+'/policies/OCI-Auditor/OCI-Auditor-Production.json')
   
    print("\n**********************************************************************************")
    print("Auditor Policy Data Loaded Successfully From Source Code")
    print("**********************************************************************************\n")
    
    is_valid, msg = validate_json(oci_auditor_environments_policy_document, compartment_policy_schema, "OCI-Auditor Environment Schema")
    print(msg) 
    is_valid, msg = validate_json(oci_auditor_sandbox_policy_document, compartment_policy_schema, "OCI-Auditor Sandbox Schema")
    print(msg)
    is_valid, msg = validate_json(oci_auditor_production_policy_document, compartment_policy_schema, "OCI-Auditor Production Schema")
    print(msg)

    print("\n**********************************************************************************")
    print("Auditor Policy Build & Validation Process Completed Successfully")
    print("**********************************************************************************\n")

def operator_build_validation():

    compartment_policy_schema = get_schema(os.getcwd()+'/schema/compartment_json_schema.json')
    oci_operator_environments_policy_document = get_json_data(os.getcwd()+'/policies/OCI-Operator/OCI-Operator-Environments.json')
    oci_operator_sandbox_policy_document = get_json_data(os.getcwd()+'/policies/OCI-Operator/OCI-Operator-Sandbox.json')
    oci_operator_production_policy_document = get_json_data(os.getcwd()+'/policies/OCI-Operator/OCI-Operator-Production.json')

    print("\n**********************************************************************************")
    print("Operator Policy Data Loaded Successfully From Source Code")
    print("**********************************************************************************\n")
    
    is_valid, msg = validate_json(oci_operator_environments_policy_document, compartment_policy_schema, "OCI-Operator Environment Schema")
    print(msg) 
    is_valid, msg = validate_json(oci_operator_sandbox_policy_document, compartment_policy_schema, "OCI-Operator Sandbox Schema")
    print(msg)
    is_valid, msg = validate_json(oci_operator_production_policy_document, compartment_policy_schema, "OCI-Operator Production Schema")
    print(msg)

    print("\n**********************************************************************************")
    print("Operator Policy Build & Validation Process Completed Successfully")
    print("**********************************************************************************\n")

def privilege_build_validation():

    privilege_policy_schema = get_schema(os.getcwd()+'/schema/privilege_json_schema.json')
    oci_privilege_environments_policy_document = get_json_data(os.getcwd()+'/policies/OCI-Privilege/OCI-Privilege-Administrator-Environment.json')

    print("\n**********************************************************************************")
    print("Privilege Policy Data Loaded Successfully From Source Code")
    print("**********************************************************************************\n")
    
    is_valid, msg = validate_json(oci_privilege_environments_policy_document, privilege_policy_schema, "OCI-Privilege Environment Schema")
    print(msg) 

    print("\n**********************************************************************************")
    print("Privilege Policy Build & Validation Process Completed Successfully")
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

def non_production_auditor_deployment():
    oci_auditor_environments_policy_document = get_json_data(os.getcwd()+'/policies/OCI-Auditor/OCI-Auditor-Environments.json')
    oci_auditor_environments_policy_list = get_role_policies(oci_auditor_environments_policy_document, "oci-role-based-policy-document", domain, env)
    oci_auditor_environments_policy_data = '[\n'+oci_auditor_environments_policy_list.objtoString()+'\n]'
    replace_policy_list_in_tftemplate(oci_auditor_environments_policy_data, os.getcwd()+'/policies/oci_environments_policies.tfvars.template')
    name = get_policy_name(oci_auditor_environments_policy_document, "oci-role-based-policy-document", env)
    replace_policy_name_in_tf(name, os.getcwd()+'/terraform/oci_policies.tf')
    print("**********************************************************************************")

def non_production_operator_deployment():
    oci_operator_environments_policy_document = get_json_data(os.getcwd()+'/policies/OCI-Operator/OCI-Operator-Environments.json')
    oci_operator_environments_policy_list = get_role_policies(oci_operator_environments_policy_document, "oci-role-based-policy-document", domain, env)
    oci_operator_environments_policy_data = '[\n'+oci_operator_environments_policy_list.objtoString()+'\n]'
    replace_policy_list_in_tftemplate(oci_operator_environments_policy_data, os.getcwd()+'/policies/oci_environments_policies.tfvars.template')
    name = get_policy_name(oci_operator_environments_policy_document, "oci-role-based-policy-document", env)
    replace_policy_name_in_tf(name, os.getcwd()+'/terraform/oci_policies.tf')
    print("**********************************************************************************")

def non_production_privilege_deployment():
    oci_privilege_policy_inputs = get_json_data(os.getcwd()+'/policies/OCI-Privilege/OCI-Privilege-Administrator-Environment-Inputs.json')
    oci_privilege_environments_policy_document = get_json_data(os.getcwd()+'/policies/OCI-Privilege/OCI-Privilege-Administrator-Environment.json')
    oci_privilege_environments_policy_list = get_privilege_role_policies(oci_privilege_policy_inputs, oci_privilege_environments_policy_document, "oci-role-based-policy-document", domain, env)
    replace_policy_list_in_tftemplate(oci_privilege_environments_policy_list, os.getcwd()+'/policies/oci_environments_policies.tfvars.template')
    print("**********************************************************************************")

def sandbox_auditor_deployment():
    oci_auditor_sandbox_policy_document = get_json_data(os.getcwd()+'/policies/OCI-Auditor/OCI-Auditor-Sandbox.json')
    oci_auditor_sandbox_policy_list = get_role_policies(oci_auditor_sandbox_policy_document,  "oci-role-based-policy-document", domain, env)
    oci_auditor_sandbox_policy_data = '[\n'+oci_auditor_sandbox_policy_list.objtoString()+'\n]'
    replace_policy_list_in_tftemplate(oci_auditor_sandbox_policy_data, os.getcwd()+'/policies/oci_environments_policies.tfvars.template')
    print("**********************************************************************************")

def sandbox_operator_deployment():
    oci_operator_sandbox_policy_document = get_json_data(os.getcwd()+'/policies/OCI-Operator/OCI-Operator-Sandbox.json')
    oci_operator_sandbox_policy_list = get_role_policies(oci_operator_sandbox_policy_document, "oci-role-based-policy-document", domain, env)
    oci_operator_sandbox_policy_data = '[\n'+oci_operator_sandbox_policy_list.objtoString()+'\n]'
    replace_policy_list_in_tftemplate(oci_operator_sandbox_policy_data, os.getcwd()+'/policies/oci_environments_policies.tfvars.template')
    print("**********************************************************************************")

def sandbox_privilege_deployment():
    oci_elevated_sandbox_policy_document = get_json_data(os.getcwd()+'/policies/OCI-Auditor/OCI-Auditor-Sandbox.json')
    oci_elevated_sandbox_policy_list = get_role_policies(oci_elevated_sandbox_policy_document,  "oci-role-based-policy-document", domain, env)
    oci_elevated_sandbox_policy_data = '[\n'+oci_elevated_sandbox_policy_list.objtoString()+'\n]'
    replace_policy_list_in_tftemplate(oci_elevated_sandbox_policy_data, os.getcwd()+'/policies/oci_environments_policies.tfvars.template')
    print("**********************************************************************************")

def production_auditor_deployment():
    oci_auditor_production_policy_document = get_json_data(os.getcwd()+'/policies/OCI-Auditor/OCI-Auditor-Production.json')
    oci_auditor_production_policy_list = get_role_policies(oci_auditor_production_policy_document, "oci-role-based-policy-document", domain, env)
    oci_auditor_production_policy_data = '[\n'+oci_auditor_production_policy_list.objtoString()+'\n]'
    replace_policy_list_in_tftemplate(oci_auditor_production_policy_data, os.getcwd()+'/policies/oci_environments_policies.tfvars.template')
    print("**********************************************************************************")

def production_operator_deployment():
    oci_operator_production_policy_document = get_json_data(os.getcwd()+'/policies/OCI-Operator/OCI-Operator-Production.json')
    oci_operator_production_policy_list = get_role_policies(oci_operator_production_policy_document, "oci-role-based-policy-document", domain, env)
    oci_operator_production_policy_data = '[\n'+oci_operator_production_policy_list.objtoString()+'\n]'
    replace_policy_list_in_tftemplate(oci_operator_production_policy_data, os.getcwd()+'/policies/oci_environments_policies.tfvars.template')
    print("**********************************************************************************")

def replace_policy_list_in_tftemplate(policy_data, tf_var_template):
    with FileInput(tf_var_template, inplace=True, backup='.bak') as f:
        for line in f:
            print(line.replace("POLICIES_OBJECT_LIST", policy_data), end='')

def replace_policy_name_in_tf(name, tf_file):
    with FileInput(tf_file, inplace=True) as f:
        for line in f:
            print(line.replace("TF_POLICY_NAME", name), end='')


print("**********************************************************************************")
print("Policy As Code Process Started......")
print("**********************************************************************************")

domain = sys.argv[1]
env = sys.argv[2]
operation = sys.argv[3]

if (operation.lower()=="tenancy-build-validation"):
    tenancy_build_validation()

if (operation.lower()=="auditor-build-validation"):
    auditor_build_validation()

if (operation.lower()=="operator-build-validation"):
    operator_build_validation()

if (operation.lower()=="privilege_build-validation"):
    privilege_build_validation()

if (operation.lower()=="tenancy-deployment"):
    tenancy_deployment()

if (operation.lower()=="non-production-auditor-deployment"):
    non_production_auditor_deployment()

if (operation.lower()=="non-production-operator-deployment"):
    non_production_operator_deployment()

if (operation.lower()=="non-production-privilege-deployment"):
    non_production_privilege_deployment()

if (operation.lower()=="sandbox-auditor-deployment"):
    sandbox_auditor_deployment()

if (operation.lower()=="sandbox-operator-deployment"):
    sandbox_operator_deployment()

if (operation.lower()=="sandbox-privilege-deployment"):
    sandbox_privilege_deployment()

if (operation.lower()=="production-auditor-deployment"):
    production_auditor_deployment()

if (operation.lower()=="production-operator-deployment"):
    production_operator_deployment()
