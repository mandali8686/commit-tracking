import json
import re

def load_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def extract_ground_truth(prompts):
    change_types_gt = {}
    for key, value in prompts.items():
        mods = value['prompt_3']['mods']
        change_types_gt[key] = [mod['change_type'] for mod in mods]
    return change_types_gt

def parse_change_type(text):
    # Find all occurrences of ADD, MODIFY, or DELETE in all caps
    matches = re.findall(r'\b(ADD|MODIFY|DELETE)\b', text)
    return matches if matches else []

def extract_responses(results, prompt_key, query_key):
    extracted_responses = {}
    for row_key, prompts in results.items():
        prompt_data = prompts.get(prompt_key, {}).get(query_key)
        if prompt_data:
            extracted_change_type = parse_change_type(prompt_data)
            if extracted_change_type:
                extracted_responses[row_key] = extracted_change_type
    return extracted_responses

def calculate_accuracy(extracted, ground_truth):
    correct = 0
    total = 0
    for key, values in extracted.items():
        gt_values = ground_truth.get(key, [])
        total += len(gt_values)
        correct += sum(val.strip().upper() == gt_val.upper() for val, gt_val in zip(values, gt_values))
    accuracy = (correct / total) * 100 if total > 0 else 0
    return accuracy, correct
prompts = load_data('prompts.json')

message_results = load_data('message_results.json')
mods_results = load_data('mods_results.json')

change_types_gt = extract_ground_truth(prompts)

# Extract change type responses from message_results.json
message_change_responses = extract_responses(message_results, 'prompt_2', 'message_change_query')

# Calculate message change type accuracy
message_change_accuracy, message_correct = calculate_accuracy(message_change_responses, change_types_gt)

# Extract change type responses from mods_results.json
def extract_mods_responses(results, prompt_key, query_key_fragment):
    extracted_responses = {}
    for row_key, prompts in results.items():
        if prompt_key in prompts:
            for query in prompts[prompt_key]:
                for query_key, text in query.items():
                    if query_key_fragment in query_key:
                        change_types = parse_change_type(text)
                        if row_key not in extracted_responses:
                            extracted_responses[row_key] = []
                        extracted_responses[row_key].extend(change_types)
    return extracted_responses
# Extract mods change type responses from mods_results.json
mods_change_query_key_fragment = 'mods_change_query'
mods_change_responses = extract_mods_responses(mods_results, 'prompt_4', mods_change_query_key_fragment)

# Calculate mods change type accuracy
mods_change_accuracy, mods_correct = calculate_accuracy(mods_change_responses, change_types_gt)

# Debugging output
#print(f"Ground truth change types: {change_types_gt}")
#print(f"Extracted message change types: {message_change_responses}")
print(f"Correct message change types: {message_correct}")
#print(f"Extracted mods change types: {mods_change_responses}")
print(f"Correct mods change types: {mods_correct}")

print(f'Message Change Type Accuracy: {message_change_accuracy:.2f}%')
print(f'Mods Change Type Accuracy: {mods_change_accuracy:.2f}%')
