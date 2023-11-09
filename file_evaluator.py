import json
import re

def load_data(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return {}

def extract_ground_truth_files(prompts):
    gt_files = {}
    for key, value in prompts.items():
        mods = value['prompt_3']['mods']
        gt_files[key] = [mod['new_path'] for mod in mods if mod['new_path'] is not None]
    return gt_files

def parse_files(text):
    return re.findall(r'\b[\w/]+\.\w+\b', text)

def extract_file_responses(results, prompt_key, query_key):
    extracted_responses = {}
    for row_key, prompts in results.items():
        if prompt_key in prompts:
            for query_item in prompts[prompt_key]:
                # Check if the item is a dictionary
                if isinstance(query_item, dict):
                    # Iterate through each dictionary
                    for query_key_item, text in query_item.items():
                        if query_key in query_key_item:
                            extracted_files = parse_files(text)
                            if row_key not in extracted_responses:
                                extracted_responses[row_key] = []
                            extracted_responses[row_key].extend(extracted_files)
                # If the item is a string
                elif isinstance(query_item, str):
                    if query_key in query_item:
                        extracted_files = parse_files(query_item)
                        if row_key not in extracted_responses:
                            extracted_responses[row_key] = []
                        extracted_responses[row_key].extend(extracted_files)
    return extracted_responses

def extract_mentioned_files(message_results, ground_truth_files):
    extracted_files = {}
    for row_key, prompts in message_results.items():
        # Initialize an empty list for each row in the output
        extracted_files[row_key] = []
        if row_key in ground_truth_files:
            # Get the list of files to check from the ground truth
            truth_files = ground_truth_files[row_key]
            # Iterate through each prompt in the row
            for prompt_key, prompt_data in prompts.items():
                # Focus on the 'message_query' content
                if 'message_query' in prompt_data:
                    message_text = prompt_data['message_query']
                    # Check each ground truth file against the message
                    for file in truth_files:
                        if file in message_text:
                            extracted_files[row_key].append(file)
    return extracted_files


def calculate_file_match_score(extracted_files, ground_truth_files):
    scores = []
    for key, extracted in extracted_files.items():
        gt_files = set(ground_truth_files.get(key, []))
        extracted_set = set(extracted)
        if gt_files:
            score = (len(extracted_set & gt_files) / len(gt_files)) * 100
        else:
            score = 0
        scores.append(score)
    return sum(scores) / len(scores) if scores else 0

# Load data
prompts = load_data('prompts.json')
message_results = load_data('message_results.json')
mods_results = load_data('mods_results.json')

# Process data
ground_truth_files = extract_ground_truth_files(prompts)
extracted_files = extract_mentioned_files(message_results, ground_truth_files)

#message_file_responses = extract_files_from_messages(message_results, 'prompt_1', 'message_query')
mods_file_responses = extract_file_responses(mods_results, 'prompt_3', 'mods_query')

# Calculate scores
message_file_score = calculate_file_match_score(extracted_files, ground_truth_files)
mods_file_score = calculate_file_match_score(mods_file_responses, ground_truth_files)

# Display results
#print(f"Ground truth files: {ground_truth_files}")
#print("Message_results:", message_results)
print(f"Extracted message files: {extracted_files}")
print(f"Extracted mods files: {mods_file_responses}")
print(f'Message File Match Score: {message_file_score:.2f}%')
print(f'Mods File Match Score: {mods_file_score:.2f}%')
