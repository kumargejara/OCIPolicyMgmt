import json
import jsonschema
from jsonschema import validate

def get_schema(file_name):
    with open(file_name, 'r') as file:
        schema = json.load(file)
    return schema

def get_json_data(file_name):
    with open(file_name, 'r') as file:
        json_data = json.load(file)
    return json_data

def validate_json(json_data, json_schema):

    try:
        validate(instance=json_data, schema=json_schema)
    except jsonschema.exceptions.ValidationError as err:
        print(err)
        err = "Given JSON data is InValid"
        return False, err

    message = "Given JSON data is Valid"
    return True, message

def check_policy(policy, policydata):
    for existing_policy in policydata['policy']:
        if existing_policy.lower() == policy.lower():
            return True
    return False


tenancy_policy_schema = get_schema('tenancy_json_schema.json')
compartment_policy_schema = get_schema('compartment_json_schema.json')
tenancy_policy_document = get_json_data('tenancy.json')
compartment_policy_document = get_json_data('compartment.json')
existing_policy_document = get_json_data('current_policies_list.json')
print("schema successfully loaded")
print("**********************************************************************************")
print(tenancy_policy_schema)
print("**********************************************************************************")
print(compartment_policy_schema)
print("**********************************************************************************")
print(tenancy_policy_document)
print("**********************************************************************************")
print(compartment_policy_document)
print("**********************************************************************************")
print(existing_policy_document)
is_valid, msg = validate_json(tenancy_policy_document, tenancy_policy_schema)
print(msg) 
is_valid, msg = validate_json(compartment_policy_document, compartment_policy_schema)
print(msg)
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

existing_policy_count=0
new_policy_count = 0
new_policy_list = []
for i in range(len(policy_list)):
    if check_policy(policy_list[i], existing_policy_document):
        existing_policy_count = existing_policy_count+1
    else:
        new_policy_list.append(policy_list[i])
        new_policy_count = new_policy_count+1

print(len(policy_list))
print(existing_policy_count)
print(new_policy_count)