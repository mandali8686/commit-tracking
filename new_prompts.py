import json

def read_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def create_gpt_prompts(data_rows):
    prompts = {}
    for i, row in enumerate(data_rows):
        # Accessing the nested 'message' and 'mods'
        message = row['row'].get('message', '')
        mods = row['row'].get('mods', [])

        # Create a list of file names from "new_path" and "diff"
        file_names = [mod.get('new_path', '') for mod in mods if mod.get('new_path')]
        file_names += [mod.get('diff', '').split('\n')[0] for mod in mods if mod.get('diff')]

        # Prompt 1: Select files changed based on commit message
        prompts[f'Row_{i + 1}_File_Selection'] = {
            'commit_message': message,
            'file_list': file_names,
            'query': 'Based on the commit message, which files were changed?'
        }

        # Prompt 2: Predict the next half of "diff"
        for j, mod in enumerate(mods):
            half_diff_length = len(mod.get('diff', '').split('\n')) // 2
            half_diff = '\n'.join(mod.get('diff', '').split('\n')[:half_diff_length])

            prompts[f'Row_{i + 1}_Diff_Prediction_{j}'] = {
                'user': {
                    'mod': mod,
                    'half_diff': half_diff
                },
                'response_query': 'Predict the next half of the diff.'
            }

    return prompts

data = read_json_file('record.json')
data_prompt = data["rows"]
print(data_prompt[0])

prompts = create_gpt_prompts(data_prompt)
#print(prompts[0])

# Save to a JSON file
with open('new_prompts.json', 'w') as f:
    json.dump(prompts, f, indent=4)
