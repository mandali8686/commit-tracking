import openai
import json

if __name__ == "__main__":
    API_KEY = "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"
    openai.api_key = API_KEY
    
    # Load prompts from your JSON file
    with open('prompts.json', 'r') as f:
        prompts_dict = json.load(f)
    
    message_results = {}
    mods_results = {}
    
    for row_key, row_data in prompts_dict.items():
        message_results[row_key] = {}
        mods_results[row_key] = {}
        
        # Sort keys to make sure the prompts are processed in order
        for prompt_key in sorted(row_data.keys()):
            prompt_data = row_data[prompt_key]
            
            # Prepare the prompt for message_query and message_change_query
            if 'message_query' in prompt_data or 'message_change_query' in prompt_data:
                query_type = 'message_query' if 'message_query' in prompt_data else 'message_change_query'
                prompt = prompt_data[query_type] + ' ' + prompt_data['message']
                print(f"<<<{query_type} Prompt Generated>>>")
                print(prompt)
                
                # Call GPT API
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                
                message_results[row_key][prompt_key] = {query_type: response['choices'][0]['message']['content']}
                print(f"{query_type} Result:", message_results[row_key][prompt_key])
            
            # Prepare the prompt for mods_query and mods_change_query
            if 'mods_query' in prompt_data or 'mods_change_query' in prompt_data:
                query_type = 'mods_query' if 'mods_query' in prompt_data else 'mods_change_query'
                mods_json = json.dumps(prompt_data['mods'])
                prompt = prompt_data[query_type] + ' ' + mods_json
                print(f"<<<{query_type} Prompt Generated>>>")
                print(prompt)
                
                # Call GPT API
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                
                mods_results[row_key][prompt_key] = {query_type: response['choices'][0]['message']['content']}
                print(f"{query_type} Result:", mods_results[row_key][prompt_key])
    
    # Save results to JSON files
    with open('message_results.json', 'w') as f:
        json.dump(message_results, f)

    with open('mods_results.json', 'w') as f:
        json.dump(mods_results, f)
