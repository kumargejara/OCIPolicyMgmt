import json
import jsonschema
from jsonschema import validate
import os

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

def check_policy(policy, policydata):
    for existing_policy in policydata['data']['statements']:
        if existing_policy.lower() == policy.lower():
            return True
    return False

def prepareJsonForCurrentPolicies(filename):
    print("\nCurrent Policy List")
    read_file = open(filename, 'r')
    Lines = read_file.readlines()
    write_file = open(os.getcwd()+'/policies/policy_state.json', 'w')
    write_flag = 0
    for line in Lines:
        if (write_flag == 0):
            if "header: Content-Length:" in line:
                write_flag = 1
        else:
            write_file.write(line)
    read_file.close()
    write_file.close()


def write_new_policies(filename, policy_list):
    try:
        os.remove(filename)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

    file1 = open(filename, 'w')
    file1.write('[\n')
    print("\nCurrent Policy List")
    print("**********************************************************************************")
    for existing_policy in existing_policy_document['data']['statements']:
        file1.write('"'+existing_policy+'",\n')
        print(existing_policy)
    print("**********************************************************************************\n")
    print("\nNew Policy List")
    print("**********************************************************************************")
    for i in range(len(policy_list)):
        if (i+1) == len(policy_list):
            file1.write('"'+policy_list[i]+'"\n')
        else:
            file1.write('"'+policy_list[i]+'",\n')
        print(policy_list[i])
    file1.write(']')
    file1.close()
    print("**********************************************************************************\n")

print("\n**********************************************************************************")
print("Policy Data Loaded Successfully From Source Code")
print("**********************************************************************************\n")
tenancy_policy_schema = get_schema('./schema/tenancy_json_schema.json')
compartment_policy_schema = get_schema('./schema/compartment_json_schema.json')
policy_state_schema = get_schema('./schema/policy_state_schema.json')
tenancy_policy_document = get_json_data(os.getcwd()+'/policies/tenancy/tenancy.json')
compartment_policy_document = get_json_data(os.getcwd()+'/policies/development/compartment.json')
prepareJsonForCurrentPolicies(os.getcwd()+'/policies/policy_state_data.txt')
existing_policy_document = get_json_data(os.getcwd()+'/policies/policy_state.json')

print("\n**********************************************************************************")
print("Policy Schema Loaded Successfully From Json Schema Files")
print("**********************************************************************************\n")


is_valid, msg = validate_json(tenancy_policy_document, tenancy_policy_schema, "Tenancy Schema")
print(msg) 
is_valid, msg = validate_json(compartment_policy_document, compartment_policy_schema, "Environment Schema")
print(msg)
is_valid, msg = validate_json(existing_policy_document, policy_state_schema, "Policy State Schema")
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
    if check_policy(policy_list[i], existing_policy_document):
        existing_policy_count = existing_policy_count+1
    else:
        new_policy_list.append(policy_list[i])
        new_policy_count = new_policy_count+1


write_new_policies(os.getcwd()+'/policies/new_policy_state.json', new_policy_list)
print("Policy Summary Report")
print("**********************************************************************************")
print(f"Existing Policies List = {existing_policy_count-1}")
print(f"New Policies Will Be Added  = {new_policy_count}")
print(f"Total Policies List = {existing_policy_count-1+new_policy_count}")
print("**********************************************************************************\n")

