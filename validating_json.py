import json
import re
from pathlib import Path

def transform_data(data):
    """
    Transforms the data by extracting questions, exact answers, and parsed generated answers.
    """
    transformed_data = []
    for item in data:
        question = item['question']
        exact_answer = item['exact_answer']
        generated_answer_str = item['generated_answer']
        
        generated_answer_list = re.findall(r'"(.*?)"', generated_answer_str)
        
        transformed_item = {
            "question": question,
            "exact_answer": exact_answer,
            "generated_answer": generated_answer_list
        }
        transformed_data.append(transformed_item)
    return transformed_data

def process_file(input_file_path, output_file_path):
    """
    Processes a single input file, transforming its data and saving the output.
    """
    with open(input_file_path, 'r') as infile:
        data = json.load(infile)
    
    transformed_data = transform_data(data)
    
    with open(output_file_path, 'w') as outfile:
        json.dump(transformed_data, outfile, indent=4)
    print(f"Processed and saved: {output_file_path}")

input_dir = Path('llama3_chatqa_answers')
output_dir = input_dir / 'validated_llama3_chatqa_answers'
output_dir.mkdir(parents=True, exist_ok=True)

input_files = [
    input_dir / 'llama3_chatqa_answers_task6b_combined.json',
    input_dir / 'llama3_chatqa_answers_task7b_combined.json',
    input_dir / 'llama3_chatqa_answers_task8b_combined.json'
]

for input_file in input_files:
    output_file = output_dir / f'validated_{input_file.stem}.json'
    process_file(input_file, output_file)