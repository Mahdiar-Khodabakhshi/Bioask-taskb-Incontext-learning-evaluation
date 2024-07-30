# Biomedical Factoid Question Answering Evaluation

## Overview

This repository contains the code and instructions for evaluating a Large Language Model (LLM) in the context of biomedical factoid question answering. The evaluation process involves data cleaning, answer generation, and model assessment using multiple metrics.

## Files and Instructions

### 1. `data_cleaning.py`

This script processes the raw data and outputs a cleaned dataset. The cleaned dataset includes:
- **Body (Question):** The question to be answered.
- **Snippets (Context):** Relevant context for answering the question.
- **Exact Answer:** The correct answer to the question.
- **Type of Data:** Always "Factoid" in this project.

**Usage:**
Run this script to obtain the cleaned dataset required for the subsequent evaluation steps.

```bash
python data_cleaning.py
```
### 2. `generate_answers.py`

Use this script to generate answers based on the provided context using the Llama3-ChatQA-8 model. Note that this model may produce invalid JSON outputs.

**Usage:**
```bash
python generate_answers.py
```
### 3. `validate_json.py`

Since the Llama3-ChatQA-8 model can generate invalid JSON, use this script to:

- Validate the JSON output.
- Normalize the data to prepare it for comparison with the exact answers.

**Usage:**
```bash
python validate_json.py
```

### 4. `evaluate_llama.py`

This script evaluates the performance of the model using the following metrics:

- **Mean Reciprocal Rank (MRR):** Measures the average rank of the first correct answer among the top 5 responses.
- **Strict Accuracy:** The percentage of questions where the correct answer is the very first response generated.
- **Lenient Accuracy:** The percentage of questions where at least one correct answer is included among the responses, regardless of order.

**Usage:**
```bash
python evaluate_llama.py
```
