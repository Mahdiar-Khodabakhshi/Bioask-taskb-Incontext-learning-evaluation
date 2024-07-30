import json
import re
import unicodedata

with open('valid_generated_llama_6B.json', 'r') as f:
    data = json.load(f)

def normalize_answer(answer):
    """Normalize answer by lowercasing, removing punctuation, stripping whitespace, and handling special characters."""
    answer = answer.lower()
    answer = unicodedata.normalize('NFKD', answer)
    answer = ''.join(c for c in answer if not unicodedata.combining(c))
    answer = re.sub(r'[^a-z0-9\s]', '', answer)
    answer = answer.strip()
    return answer

def strict_accuracy(data):
    correct = 0
    total = len(data)
    for item in data:
        normalized_exact_answer = [normalize_answer(ans) for ans in item['exact_answer']]
        normalized_generated_answer = [normalize_answer(ans) for ans in item['generated_answer']]
        if normalized_generated_answer[:len(normalized_exact_answer)] == normalized_exact_answer:
            correct += 1
    return correct / total

def lenient_accuracy(data):
    correct = 0
    total = len(data)
    for item in data:
        normalized_exact_answer = [normalize_answer(ans) for ans in item['exact_answer']]
        normalized_generated_answer = [normalize_answer(ans) for ans in item['generated_answer']]
        if any(ans in normalized_exact_answer for ans in normalized_generated_answer):
            correct += 1
    return correct / total

def mean_reciprocal_rank(data, k):
    total_reciprocal_rank = 0
    total = len(data)
    for item in data:
        normalized_exact_answer = [normalize_answer(ans) for ans in item['exact_answer']]
        normalized_generated_answer = [normalize_answer(ans) for ans in item['generated_answer'][:k]]
        
        found = False
        for rank, ans in enumerate(normalized_generated_answer, start=1):
            if ans in normalized_exact_answer:
                total_reciprocal_rank += 1 / rank
                found = True
                break
        if not found:
            total_reciprocal_rank += 0 
    return total_reciprocal_rank / total

K = 5

strict_acc = strict_accuracy(data)
lenient_acc = lenient_accuracy(data)
mrr = mean_reciprocal_rank(data, K)

print(f"Strict Accuracy at K={K}: {strict_acc:.2%}")
print(f"Lenient Accuracy: {lenient_acc:.2%}")
print(f"Mean Reciprocal Rank (MRR) at K={K}: {mrr:.2f}")
