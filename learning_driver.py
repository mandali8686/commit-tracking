import openai
import json
from requests.exceptions import ReadTimeout

def make_request_with_retry(prompt, model="gpt-3.5-turbo", max_retries=5):
    backoff_factor = 1
    for i in range(max_retries):
        try:
            # Call GPT API
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": prompt}
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

def query_gpt_with_conversation(conversations, for_training=True):
    results = {}
    for i, conversation in enumerate(conversations):
        # For training, we send the entire conversation; for testing, we omit the last part for the model to predict
        prompt = conversation if for_training else conversation.split('Assistant:')[0]
        response = make_request_with_retry(prompt)
        if response:
            # If training, we don't expect a prediction, we are just training the model
            if for_training:
                continue
            # If testing, we store the prediction
            else:
                results[i] = response['choices'][0]['message']['content']
        else:
            print(f"Failed to get a response for conversation {i} after retries.")
    return results

if __name__ == "__main__":
    API_KEY = "your-api-key"
    openai.api_key = API_KEY

    # Load training and testing conversations
    with open('training_conversations.json', 'r') as f:
        training_conversations = json.load(f)
    
    with open('testing_conversations.json', 'r') as f:
        testing_conversations = json.load(f)

    # Query GPT with training conversations
    query_gpt_with_conversation(training_conversations, for_training=True)

    # Query GPT with testing conversations and collect predictions
    predictions = query_gpt_with_conversation(testing_conversations, for_training=False)

    # Save the predictions to a JSON file
    with open('predictions.json', 'w') as f:
        json.dump(predictions, f, indent=4)
