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
        combined_prompts = []
        for mod in mods:
            # Convert the mod dictionary to a string representation
            mod_str = json.dumps(mod)
            # Combine message with the current mod
            combined_prompt = message + " " + mod_str
            combined_prompts.append(combined_prompt)

        # Create the prompts
        prompts[f'Row_{i + 1}'] = {
            'prompt_1': {
                'message_query': 'What files are changed based on this message?',
                'message': message
            },
            'prompt_2': {
                'message_change_query': 'Given this message, what types of change occured, ADD, DELETE, or, MODIFY?',
                'message': message
            },
            'prompt_3':{
                'mods_query':"What files are changed based on this mods?",
                'mods': mods
            },
            'prompt_4':{
                'mods_change_query':'Given this mods message, what types of change occured, ADD, DELETE, or, MODIFY?',
                'mods': mods
            },
            'prompt_5':{
                'dependency_query': 'Based on the modifications, what are the file inclusion dependencies?',
                'mods':mods
            }
            }
            #rPESENTATION OF FILE CHANGE, WHAT FILES IS CHANGED
            #PARSE A LIST OF FILES, SHOW PART OF THE COMMIT, DON'T SHOW EVERYTHING
            #FEW SHOT EXAMPLES:3/4 MOD-1/4 MOD
            #Need to give examples to predict for next ones
        
    return prompts

prompts = create_prompts(data_prompt)
print(len(prompts))

# Save to a JSON file
with open('prompts.json', 'w') as f:
    json.dump(prompts, f, indent=4)


