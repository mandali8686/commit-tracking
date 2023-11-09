import openai
import json
import time
from requests.exceptions import ReadTimeout

def make_request_with_retry(prompt, model="gpt-3.5-turbo", max_retries=5):
    backoff_factor = 1
    for i in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            #print("Response:", response)
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
    openai.api_key = "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"  # Replace with your actual API key
    
    # Load prompts from your JSON file
    with open('prompts.json', 'r') as f:
        prompts_dict = json.load(f)
    
    prompt_5_results = {}
    
    for row_key, row_data in prompts_dict.items():
        if "prompt_5" in row_data:
            prompt = row_data["prompt_5"]["dependency_query"] +" "+json.dumps(row_data["prompt_5"]["mods"])  # Assuming prompt_5 contains a 'content' key
            print(f"Processing {row_key} - prompt_5")
            print(prompt)
            
            response = make_request_with_retry(prompt)
            if response:
                prompt_5_results[row_key] = response['choices'][0]['message']['content']
                print(f"Response for {row_key} - prompt_5:", prompt_5_results[row_key])
            else:
                print(f"Failed to get a response for {row_key} - prompt_5 after retries.")
    
    # Save results to JSON file
    with open('prompt_5_results.json', 'w') as f:
        json.dump(prompt_5_results, f, indent=4)
