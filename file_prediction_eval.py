import json

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def evaluate_file_selection(file_selection_results, ground_truth):
    correct = 0
    for key, result in file_selection_results.items():
        gt_key = key.split('_File_Selection')[0] + "_Diff_Prediction_0"
        gt_mods = ground_truth[gt_key]['user']['mod']
        new_path = gt_mods['new_path']

        # Check if new_path is not None and is in the result file list
        if new_path and new_path in result:
            correct += 1

    accuracy = correct / len(file_selection_results) if file_selection_results else 0
    return accuracy

# Rest of your code remains the same

# Load the result and ground truth data
file_selection_results = load_json('file_selection_results.json')
ground_truth = load_json('new_prompts.json')

# Evaluate file selection
file_selection_accuracy = evaluate_file_selection(file_selection_results, ground_truth)
print(f"File Selection Accuracy: {file_selection_accuracy}")
