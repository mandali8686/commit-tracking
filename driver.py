import openai
import json
import time
from requests.exceptions import ReadTimeout

def make_request_with_retry(prompt, model="gpt-4", max_retries=5):
    backoff_factor = 1
    for i in range(max_retries):
        try:
            # Call GPT API
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response
        except ReadTimeout:
            print(f"Request timed out (attempt {i+1}/{max_retries}). Retrying in {backoff_factor} seconds.")
            time.sleep(backoff_factor)
            backoff_factor *= 2  # Exponential backoff
        except openai.error.OpenAIError as e:
            print(f"An OpenAI API error occurred: {e}")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break
    return None

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
                
                # Call GPT API with retry logic
                response = make_request_with_retry(prompt)
                if response:
                    message_results[row_key][prompt_key] = {query_type: response['choices'][0]['message']['content']}
                    print(f"{query_type} Result:", message_results[row_key][prompt_key])
                else:
                    print(f"Failed to get a response for {query_type} after retries.")
            
            # Prepare the prompt for mods_query and mods_change_query
            if 'mods_query' in prompt_data or 'mods_change_query' in prompt_data:
                mods = prompt_data['mods']
                for i, mod in enumerate(mods):
                    query_type = 'mods_query' if 'mods_query' in prompt_data else 'mods_change_query'
                    mod_json = json.dumps(mod)
                    prompt = prompt_data[query_type] + ' ' + mod_json
                    print(f"<<<{query_type} Prompt {i+1} Generated>>>")
                    print(prompt)
                    
                    # Call GPT API with retry logic
                    response = make_request_with_retry(prompt)
                    if response:
                        mods_results[row_key].setdefault(prompt_key, []).append({f"{query_type}_{i+1}": response['choices'][0]['message']['content']})
                        print(f"{query_type} {i+1} Result:", mods_results[row_key][prompt_key][-1])
                    else:
                        print(f"Failed to get a response for {query_type} {i+1} after retries.")
    
    # Save results to JSON files
    with open('message_results.json', 'w') as f:
        json.dump(message_results, f, indent=4)

    with open('mods_results.json', 'w') as f:
        json.dump(mods_results, f, indent=4)
