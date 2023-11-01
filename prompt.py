import json

def read_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data



data = read_json_file('record.json')
#print(type(data))
data_prompt=data["rows"]
print(len(data_prompt))

# Python function to create prompts based on the 'message' and 'mods' of each row in the data
def create_prompts(data_rows):
    prompts = {}
    for i, row in enumerate(data_rows):
        message = row.get('row', {}).get('message', '')
        
        mods = row.get('row', {}).get('mods', [])
        

        # Extract new paths from the 'mods' list
        mods_new_paths = [{'change_type': mod.get('change_type', ''), 'new_path': mod.get('new_path', '')} for mod in mods]

        # Create the prompts
        prompts[f'Row_{i + 1}'] = {
            'prompt_1': {
                'message_query': 'What file is changed based on this message?',
                'message': message
            },
            'prompt_2': {
                'message_change_query': 'Given this message, what type of change occured, ADD, DELETE, or, MODIFY?',
                'message': message
            },
            'prompt_3':{
                'mods_query':"What file is changed based on this mods?",
                'mods': mods
            },
            'prompt_4':{
                'mods_change_query':'Given this mods message, what type of change occured, ADD, DELETE, or, MODIFY?',
                'mods': mods
            }
        }
    return prompts

prompts = create_prompts(data_prompt)
print(len(prompts))

# Save to a JSON file
with open('prompts.json', 'w') as f:
    json.dump(prompts, f, indent=4)


