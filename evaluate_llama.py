import json
import re
import unicodedata
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def normalize_answer(answer):
    """Normalize answer by lowercasing, removing punctuation, stripping whitespace, and handling special characters."""
    answer = answer.lower()
    answer = unicodedata.normalize('NFKD', answer)
    answer = ''.join(c for c in answer if not unicodedata.combining(c))
    answer = re.sub(r'[^a-z0-9\s]', '', answer)
    answer = answer.strip()
    return answer

def strict_accuracy(data):
    """Calculate strict accuracy."""
    correct = 0
    total = len(data)
    for item in data:
        normalized_exact_answer = [normalize_answer(ans) for ans in item['exact_answer']]
        normalized_generated_answer = [normalize_answer(ans) for ans in item['generated_answer']]
        if normalized_generated_answer[:len(normalized_exact_answer)] == normalized_exact_answer:
            correct += 1
    return correct / total

def lenient_accuracy(data):
    """Calculate lenient accuracy."""
    correct = 0
    total = len(data)
    for item in data:
        normalized_exact_answer = [normalize_answer(ans) for ans in item['exact_answer']]
        normalized_generated_answer = [normalize_answer(ans) for ans in item['generated_answer']]
        if any(ans in normalized_exact_answer for ans in normalized_generated_answer):
            correct += 1
    return correct / total

def mean_reciprocal_rank(data, k):
    """Calculate Mean Reciprocal Rank (MRR)."""
    total_reciprocal_rank = 0
    total = len(data)
    for item in data:
        normalized_exact_answer = [normalize_answer(ans) for ans in item['exact_answer']]
        normalized_generated_answer = [normalize_answer(ans) for ans in item['generated_answer'][:k]]
        for rank, ans in enumerate(normalized_generated_answer, start=1):
            if ans in normalized_exact_answer:
                total_reciprocal_rank += 1 / rank
                break
    return total_reciprocal_rank / total

def evaluate_file(input_file_path, k=5):
    """Evaluate a single file and return the metrics."""
    try:
        with open(input_file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        logging.error(f"File not found: {input_file_path}")
        return None
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON file: {input_file_path}")
        return None

    strict_acc = strict_accuracy(data)
    lenient_acc = lenient_accuracy(data)
    mrr = mean_reciprocal_rank(data, k)

    return {
        "strict_accuracy": strict_acc,
        "lenient_accuracy": lenient_acc,
        "mrr": mrr
    }

def process_all_files(input_dir, output_file, k=5):
    """Evaluate all JSON files in a directory and save the results."""
    input_dir = Path(input_dir)
    results = {}

    for json_file in input_dir.glob("*.json"):
        logging.info(f"Processing file: {json_file}")
        metrics = evaluate_file(json_file, k)
        if metrics:
            results[json_file.stem] = metrics

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)
    logging.info(f"Results saved to {output_file}")

if __name__ == "__main__":
    # Input directory containing JSON files
    input_dir = "llama3_chatqa_answers/validated_llama3_chatqa_answers"
    # Output file for results
    output_file = "evaluation_results.json"
    # Set top-K for MRR
    K = 5

    process_all_files(input_dir, output_file, K)