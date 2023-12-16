import json
from Levenshtein import distance as levenshtein_distance

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def get_ground_truth_half_diff(ground_truth, key):
    # Extracting the second half of the diff message from the ground truth
    full_diff = ground_truth[key]['user']['mod']['diff']
    half_diff_index = len(full_diff.split('\n')) // 2
    return '\n'.join(full_diff.split('\n')[half_diff_index:])

def evaluate_diff_prediction(diff_prediction_results, ground_truth):
    total_levenshtein_distance = 0
    for key, predicted_diff in diff_prediction_results.items():
        # The key should already be in the correct format, so we use it directly
        if key in ground_truth:
            true_half_diff = get_ground_truth_half_diff(ground_truth, key)
            total_levenshtein_distance += levenshtein_distance(true_half_diff, predicted_diff)
        else:
            print(f"Ground truth key not found: {key}")

    # Calculate average Levenshtein Distance
    avg_levenshtein_distance = total_levenshtein_distance / len(diff_prediction_results) if diff_prediction_results else 0
    return avg_levenshtein_distance

# Load the result and ground truth data
diff_prediction_results = load_json('diff_prediction_results.json')
ground_truth = load_json('new_prompts.json')

# Evaluate diff prediction
avg_lev_dist = evaluate_diff_prediction(diff_prediction_results, ground_truth)
print(f"Average Levenshtein Distance: {avg_lev_dist}")
