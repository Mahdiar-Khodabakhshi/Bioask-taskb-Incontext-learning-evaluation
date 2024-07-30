import json
import os

# List of JSON file paths
json_files = [
    [
        'data/Task6BGoldenEnriched/Task6BGoldenEnriched/6B1_golden.json',
        'data/Task6BGoldenEnriched/Task6BGoldenEnriched/6B2_golden.json',
        'data/Task6BGoldenEnriched/Task6BGoldenEnriched/6B3_golden.json',
        'data/Task6BGoldenEnriched/Task6BGoldenEnriched/6B4_golden.json',
        'data/Task6BGoldenEnriched/Task6BGoldenEnriched/6B5_golden.json'
    ],
    [
        'data/Task7BGoldenEnriched/Task7BGoldenEnriched/7B1_golden.json',
        'data/Task7BGoldenEnriched/Task7BGoldenEnriched/7B2_golden.json',
        'data/Task7BGoldenEnriched/Task7BGoldenEnriched/7B3_golden.json',
        'data/Task7BGoldenEnriched/Task7BGoldenEnriched/7B4_golden.json',
        'data/Task7BGoldenEnriched/Task7BGoldenEnriched/7B5_golden.json'
    ],
    [
        'data/Task8BGoldenEnriched/Task8BGoldenEnriched/8B1_golden.json',
        'data/Task8BGoldenEnriched/Task8BGoldenEnriched/8B2_golden.json',
        'data/Task8BGoldenEnriched/Task8BGoldenEnriched/8B3_golden.json',
        'data/Task8BGoldenEnriched/Task8BGoldenEnriched/8B4_golden.json',
        'data/Task8BGoldenEnriched/Task8BGoldenEnriched/8B5_golden.json'
    ]
]

def extract_fields(data):
    extracted_questions = []
    questions = data.get('questions', [])
    for question in questions:
        if question.get('type') == 'factoid':
            filtered_snippets = [snippet.get('text') for snippet in question.get('snippets', [])]
            exact_answer = [answer for sublist in question.get('exact_answer', []) for answer in sublist]
            extracted_question = {
                'body': question.get('body'),
                'type': question.get('type'),
                'snippets': filtered_snippets,
                'exact_answer': exact_answer
            }
            extracted_questions.append(extracted_question)
    return extracted_questions

# Iterate over the list of JSON files
for index, sublist in enumerate(json_files):
    for json_file in sublist:
        if not os.path.exists(json_file):
            print(f"File not found: {json_file}")
            continue
        
        with open(json_file, 'r') as file:
            data = json.load(file)
            extracted_questions = extract_fields(data)
        
        if extracted_questions:
            # Define the output file path
            output_file_path = f'C:/Users/Mahdiar/Desktop/research_project/extracted_{os.path.basename(json_file)}'
            with open(output_file_path, 'w') as file:
                json.dump(extracted_questions, file, indent=4)
            print(f'Extracted data saved to {output_file_path}')
        else:
            print(f"No questions extracted from file {json_file}")
