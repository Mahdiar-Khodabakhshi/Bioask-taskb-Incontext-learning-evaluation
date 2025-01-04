import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_file_paths(base_dir, task_ids, subtask_ids):
    """
    Generates file paths for the given task and subtask IDs.

    Args:
        base_dir (str): Base directory containing the data.
        task_ids (iterable): Task IDs to process.
        subtask_ids (iterable): Subtask IDs within each task.

    Yields:
        tuple: Task ID and a list of corresponding file paths.
    """
    for task_id in task_ids:
        paths = [
            Path(base_dir) / f'Task{task_id}BGoldenEnriched' / f'{task_id}B{subtask_id}_golden.json'
            for subtask_id in subtask_ids
        ]
        yield task_id, paths

def extract_fields(data):
    """
    Extracts only important parts of the dataset(body(which is the question), type, snippets, exact_answer).

    Args:
        data (dict): JSON data containing questions.

    """
    extracted_questions = []
    questions = data.get('questions', [])
    for question in questions:
        if question.get('type') == 'factoid':
            filtered_snippets = [snippet.get('text', '') for snippet in question.get('snippets', [])]
            exact_answer = [answer for sublist in question.get('exact_answer', []) for answer in sublist]
            extracted_questions.append({
                'body': question.get('body', ''),
                'type': question.get('type', ''),
                'snippets': filtered_snippets,
                'exact_answer': exact_answer
            })
    return extracted_questions

def main():
    base_directory = 'dataset'
    output_directory = Path('/mnt/c/Users/mahdi_0hy61ll/Desktop/Bioask-taskb-Incontext-learning-evaluation/cleaned_data/')
    output_directory.mkdir(parents=True, exist_ok=True)

    task_ids = range(6, 9)
    subtask_ids = range(1, 6)

    for task_id, file_paths in generate_file_paths(base_directory, task_ids, subtask_ids):
        combined_data = {"questions": []}
        for file_path in file_paths:
            if not file_path.exists():
                logging.warning(f"File not found: {file_path}")
                continue

            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    combined_data["questions"].extend(data.get("questions", []))
            except json.JSONDecodeError:
                logging.error(f"Failed to parse JSON file: {file_path}")
            except Exception as e:
                logging.error(f"Unexpected error while reading {file_path}: {e}")

        if "questions" in combined_data and combined_data["questions"]:
            extracted_questions = extract_fields(combined_data)
            output_file_path = output_directory / f'extracted_Task{task_id}B_combined.json'
            with open(output_file_path, 'w') as output_file:
                json.dump(extracted_questions, output_file, indent=4)
            logging.info(f"Extracted data saved to {output_file_path}")
        else:
            logging.info(f"No valid questions extracted for Task {task_id}B")

if __name__ == "__main__":
    main()