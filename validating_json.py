import json
import re
import os

def transform_data(data):
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

def merge_json_files(file_paths):
    merged_data = []
    
    for file_path in file_paths:
        with open(file_path, 'r') as infile:
            data = json.load(infile)
            merged_data.extend(data)
    
    return merged_data

def process_files(input_file_paths, output_file_path):
    merged_data = merge_json_files(input_file_paths)
    
    transformed_data = transform_data(merged_data)
    
    with open(output_file_path, 'w') as outfile:
        json.dump(transformed_data, outfile, indent=4)

input_file_paths = ['generated_8B1.json', 'generated_8B2.json', 'generated_8B3.json', 'generated_8B4.json', 'generated_8B5.json']  # List all your JSON file paths here
output_file_path = 'valid_generated_8B.json'

process_files(input_file_paths, output_file_path)

print(f"Data has been merged, transformed, and saved to {output_file_path}")
