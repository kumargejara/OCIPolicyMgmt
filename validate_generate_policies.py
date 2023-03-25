import json
import jsonschema
from jsonschema import validate
import os
from fileinput import FileInput

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

def check_policy(policy, policylist):
    for j in range(len(policylist)):
        if policylist[j].lower() == policy.lower():
            return True
    return False

def prepare_current_policy_list(filename):
    print("\nCurrent Policy List")
    existing_policy_list = []
    read_file = open(filename, 'r')
    Lines = read_file.readlines()
    write_flag = 0
    data_flag = 0
    for line in Lines:
        line = line.strip()
        print(f'****** line: {line}')
        if "policy_list" in line:
            print("policy list tag found in tfplan")
            data_flag = 1

        if (data_flag == 1):
            if (write_flag == 0):
                if "statements" in line:
                    print("+ statements tag found in tfplan")
                    write_flag = 1
            else:
                if "]" in line:
                    write_flag = 0
                else:
                    line = line.replace("+", "")
                    line = line.replace('"', "")
                    line = line.replace(',', "")
                    line = line.strip()
                    existing_policy_list.append(line)
                    print(f'{ line } : policy found in tfplan')

    read_file.close()
    return existing_policy_list


def write_new_policies(filename, policy_list):
    file1 = open(filename, 'w')
    file1.write('[\n')
    print("\nNew Policy List")
    print("**********************************************************************************")
    total_new_policy_count = 0
    for i in range(len(policy_list)):
        if (i+1) == len(policy_list):
            file1.write('"'+policy_list[i]+'"\n')
            total_new_policy_count = total_new_policy_count + 1
        else:
            file1.write('"'+policy_list[i]+'",\n')
            total_new_policy_count = total_new_policy_count + 1
        print(policy_list[i])
    
    file1.write(']')
    file1.close()
    print(f'Total New Policies Count = {total_new_policy_count}')
    print("**********************************************************************************\n")

def replace_policy_list_in_tftemplate(filename):
    read_file = open(filename, 'r')
    Lines = read_file.readlines()
    policy_list_string=""
    for line in Lines:
        policy_list_string = policy_list_string + line
    read_file.close()
    print(policy_list_string)

    with FileInput(os.getcwd()+'/policies/vars.tf.template', inplace=True, backup='.bak') as f:
        for line in f:
            print(line.replace("REPLACE_POLICIES_LIST", policy_list_string), end='')



print("\n**********************************************************************************")
print("Policy Data Loaded Successfully From Source Code")
print("**********************************************************************************\n")
tenancy_policy_schema = get_schema('./schema/tenancy_json_schema.json')
compartment_policy_schema = get_schema('./schema/compartment_json_schema.json')
policy_state_schema = get_schema('./schema/policy_state_schema.json')
tenancy_policy_document = get_json_data(os.getcwd()+'/policies/tenancy/tenancy.json')
compartment_policy_document = get_json_data(os.getcwd()+'/policies/development/compartment.json')
existing_policy_list = prepare_current_policy_list(os.getcwd()+'/terraform/tfplan.txt')
print(existing_policy_list)


print("\n**********************************************************************************")
print("Policy Schema Loaded Successfully From Json Schema Files")
print("**********************************************************************************\n")


is_valid, msg = validate_json(tenancy_policy_document, tenancy_policy_schema, "Tenancy Schema")
print(msg) 
is_valid, msg = validate_json(compartment_policy_document, compartment_policy_schema, "Environment Schema")
print(msg)


print("\n**********************************************************************************")
print("Policy Validation Process Completed Successfully")
print("**********************************************************************************\n")
policy_list = []

for group in tenancy_policy_document['tenancy-policy-document']['group-based-policies']['group']:
    for policy in tenancy_policy_document['tenancy-policy-document']['group-based-policies']['policy']:
        stmt = policy.replace("TNET_GROUP", group)
        policy_list.append(stmt)
        print(stmt)

for group in tenancy_policy_document['tenancy-policy-document']['dynamic-group-based-policies']['group']:
    for policy in tenancy_policy_document['tenancy-policy-document']['dynamic-group-based-policies']['policy']:
        stmt = policy.replace("TNET_DGROUP", group)
        policy_list.append(stmt)
        print(stmt)

for policy in tenancy_policy_document['tenancy-policy-document']['general-tenancy-based-policies']['policy']:
    policy_list.append(policy)
    print(policy)

for group in compartment_policy_document['compartment-policy-document']['group-based-policies']['group']:
    for compartment in compartment_policy_document['compartment-policy-document']['group-based-policies']['compartment']:
        for policy in compartment_policy_document['compartment-policy-document']['group-based-policies']['policy']:
            stmt = policy.replace("TNET_GROUP", group)
            stmt = stmt.replace("TNET_COMPARTMENT", compartment)
            policy_list.append(stmt)
            print(stmt)

for group in compartment_policy_document['compartment-policy-document']['dynamic-group-based-policies']['group']:
    for compartment in compartment_policy_document['compartment-policy-document']['dynamic-group-based-policies']['compartment']:
        for policy in compartment_policy_document['compartment-policy-document']['dynamic-group-based-policies']['policy']:
            stmt = policy.replace("TNET_DGROUP", group)
            stmt = stmt.replace("TNET_COMPARTMENT", compartment)
            policy_list.append(stmt)
            print(stmt)

for policy in compartment_policy_document['compartment-policy-document']['general-compartment-based-policies']['policy']:
    policy_list.append(policy)
    print(policy)

print("**********************************************************************************")
print("Policy Build Process Completed Successfully")
print("**********************************************************************************\n")

existing_policy_count=0
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
replace_policy_list_in_tftemplate(os.getcwd()+'/policies/new_policy_state.json')
