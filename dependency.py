import openai
import json
import time
from requests.exceptions import ReadTimeout
import argparse

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
    parser = argparse.ArgumentParser(description='Run GPT model queries.')
    parser.add_argument('--API', type=str, help='API Key for OpenAI')
    parser.add_argument('--model', type=str, default='gpt-3.5-turbo', help='Model type (default: gpt-3.5-turbo)')
    
    # Parse arguments
    args = parser.parse_args()

    openai.api_key = args.API 
    # Load prompts from your JSON file
    with open('prompts.json', 'r') as f:
        prompts_dict = json.load(f)
    
    prompt_5_results = {}
    
    for row_key, row_data in prompts_dict.items():
        if "prompt_5" in row_data:
            prompt = row_data["prompt_5"]["dependency_query"] +" "+json.dumps(row_data["prompt_5"]["mods"])  # Assuming prompt_5 contains a 'content' key
            print(f"Processing {row_key} - prompt_5")
            print(prompt)
            
            response = make_request_with_retry(prompt, model=args.model)
            if response:
                prompt_5_results[row_key] = response['choices'][0]['message']['content']
                print(f"Response for {row_key} - prompt_5:", prompt_5_results[row_key])
            else:
                print(f"Failed to get a response for {row_key} - prompt_5 after retries.")
    
    # Save results to JSON file
    with open('prompt_5_results.json', 'w') as f:
        json.dump(prompt_5_results, f, indent=4)
