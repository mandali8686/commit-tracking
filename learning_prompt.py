import json
import random

# Assuming you have loaded your data from prompts.json into data_prompt
with open('prompts.json', 'r') as f:
    data_prompt = json.load(f)

# Split the data into training and testing sets
random.shuffle(data_prompt)  # Shuffle the data to ensure randomness
split_index = int(0.8 * len(data_prompt))
training_data = data_prompt[:split_index]
testing_data = data_prompt[split_index:]

# Function to construct the conversation format
def construct_conversation(data, for_training=True):
    conversations = []
    for row in data:
        message = row['row']['message']
        mods = row['row']['mods']
        for mod in mods:
            change_type = mod['change_type']
            old_path = mod['old_path']
            new_path = mod.get('new_path', '')  # For training, we provide the new_path
            diff = mod.get('diff', '')
            if for_training:
                user_prompt = f"User: Message: {message}, Change Type: {change_type}, Old Path: {old_path}\n"
                assistant_response = f"Assistant: New Path: {new_path}\n"
            else:
                # For testing, we simulate the User providing 3/4 of the diff
                diff_parts = diff.split('\n')
                provided_diff = '\n'.join(diff_parts[:-1])  # Take all but the last quarter
                remaining_diff = '\n'.join(diff_parts[-1:])  # The last quarter for the Assistant to predict
                user_prompt = f"User: Message: {message}, Change Type: {change_type}, Diff: {provided_diff}\n"
                assistant_response = f"Assistant: {remaining_diff}\n"
            conversation = user_prompt + assistant_response
            conversations.append(conversation)
    return conversations

# Construct training and testing conversations
training_conversations = construct_conversation(training_data)
testing_conversations = construct_conversation(testing_data, for_training=False)

# Save the conversations to files
with open('training_conversations.json', 'w') as f:
    json.dump(training_conversations, f, indent=4)

with open('testing_conversations.json', 'w') as f:
    json.dump(testing_conversations, f, indent=4)
