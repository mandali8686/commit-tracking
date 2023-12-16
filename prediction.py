import openai
import json
import time
from requests.exceptions import ReadTimeout

def make_request_with_retry(prompt, model="gpt-3.5-turbo", max_retries=5):
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

def query_gpt_with_new_prompts(prompts):
    file_selection_results = {}
    diff_prediction_results = {}

    for key, prompt_data in prompts.items():
        if 'File_Selection' in key:
            # Construct the prompt for file selection
            prompt = f"{prompt_data['commit_message']} \nFiles: {', '.join(prompt_data['file_list'])}\n{prompt_data['query']}"
            response = make_request_with_retry(prompt)
            if response:
                file_selection_results[key] = response['choices'][0]['message']['content']
            else:
                print(f"Failed to get a response for {key}.")

        elif 'Diff_Prediction' in key:
            # Construct the prompt for diff prediction
            mod = prompt_data['user']['mod']
            prompt = f"Change Type: {mod['change_type']}\nOld Path: {mod.get('old_path', 'None')}\nNew Path: {mod['new_path']}\nDiff: {prompt_data['user']['half_diff']}\n{prompt_data['response_query']}"
            response = make_request_with_retry(prompt)
            if response:
                diff_prediction_results[key] = response['choices'][0]['message']['content']
            else:
                print(f"Failed to get a response for {key}.")

    return file_selection_results, diff_prediction_results

if __name__ == "__main__":
    API_KEY = "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"
    openai.api_key = API_KEY

    # Load new prompts from JSON
    with open('new_prompts.json', 'r') as f:
        new_prompts = json.load(f)

    # Query GPT with new prompts
    file_selection_results, diff_prediction_results = query_gpt_with_new_prompts(new_prompts)

    # Save the results to separate JSON files
    with open('file_selection_results.json', 'w') as f:
        json.dump(file_selection_results, f, indent=4)

    with open('diff_prediction_results.json', 'w') as f:
        json.dump(diff_prediction_results, f, indent=4)
