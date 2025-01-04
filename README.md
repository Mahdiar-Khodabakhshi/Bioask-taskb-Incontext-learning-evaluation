# Biomedical Factoid Question Answering Evaluation

## **Overview**
This repository contains the code and instructions for evaluating a Llama-ChatQA fintuned by NVIDIA in the context of biomedical factoid question answering. The evaluation process involves data cleaning, answer generation, and model assessment using multiple metrics.

## **Technologies Used**
1. **Natural Language Processing (NLP)**:
   - Leveraging Llama3-ChatQA-8B, a cutting-edge LLM for question answering tasks.
   - Automated context processing and input formatting for factoid-based queries.

2. **Python Programming**:
   - Core implementation of data processing, answer validation, and evaluation scripts.
   - Libraries used:
     - `transformers`: For model and tokenizer handling.
     - `torch`: For GPU-accelerated computation.
     - `re`: For data normalization and regex-based transformations.
     - `json`: For managing structured data.
     - `unicodedata`: For text normalization.
     - `tqdm`: For progress tracking in iterative operations.

3. **Evaluation Metrics**:
   - **Mean Reciprocal Rank (MRR)**: Evaluates the ranking quality of generated answers.
   - **Strict Accuracy**: Assesses exact match performance.
   - **Lenient Accuracy**: Measures inclusion of correct answers in any position.

4. **Data Handling**:
   - Processing biomedical datasets with complex snippets and answers.
   - Automated JSON validation for ensuring structured outputs.

## **Project Workflow**
1. **Data Preparation**:
   - Cleaning raw datasets and structuring them for model input.

2. **Answer Generation**:
   - Generating predictions using a pre-trained model with fine-grained prompts.

3. **Validation**:
   - Ensuring generated outputs are in valid JSON format for reliable evaluation.

4. **Model Evaluation**:
   - Quantifying the model’s performance against exact answers using robust metrics.

---

## **Repository Structure**
### **1. `data_cleaning.py`**
Cleans and preprocesses raw datasets into a structured format for input to the LLM.

**Features**:
- Extracts the following fields:
  - **Body (Question)**: The question to be answered.
  - **Snippets (Context)**: Relevant snippets providing context for the question.
  - **Exact Answer**: The correct answer(s) to the question.
  - **Type**: Always set to "Factoid" for this project.
  
**Usage**:
```bash
python data_cleaning.py
```
### **2. `python answer_generator_llama.ipynb`**
Generates model predictions for biomedical questions using the **Llama3-ChatQA-8B** model.

**Features**:
- Formats input questions and snippets for the model.
- Produces a list of potential answers ordered by confidence.

**Note**:
- The LLM may occasionally generate invalid JSON, requiring further validation.

**Usage**:
```bash
python python answer_generator_llama.ipynb
```

### **3. `validate_json.py`**
Validates and normalizes JSON outputs from the LLM to ensure the data is well-structured and ready for evaluation.

**Features**:
- **Validation**: Ensures generated outputs conform to a valid JSON structure.
- **Normalization**: Processes and cleans the data to facilitate a reliable comparison with ground truth answers.
- **Regex Parsing**: Extracts relevant information from the generated answers for consistent formatting.

**Why It’s Needed**:
- The **Llama3-ChatQA-8B** model may produce outputs that are invalid or inconsistently formatted. This script addresses these issues by ensuring outputs adhere to a structured format.

**Usage**:
To run the script and validate JSON outputs:
```bash
python validate_json.py
```

### **4. `evaluate_model.py`**
Evaluates the performance of the LLM based on pre-defined metrics to assess its effectiveness in biomedical factoid question answering.

---

**Metrics**:
1. **Mean Reciprocal Rank (MRR)**:
   - Measures the ranking quality of the correct answer in the top 5 generated responses.
   - **Higher MRR** indicates better ranking performance.
   - Example: If the correct answer is the first response, the reciprocal rank is 1. If it’s the second, it’s 0.5.

2. **Strict Accuracy**:
   - Evaluates the percentage of questions where the model's **first generated response** matches the exact answer.
   - **Use Case**: Measures the model’s ability to provide precise answers.

3. **Lenient Accuracy**:
   - Evaluates the percentage of questions where the correct answer appears **anywhere in the top responses**.
   - **Use Case**: Tests the model’s ability to include the correct answer among its predictions, even if not ranked first.

---

**Features**:
- **Comprehensive Evaluation**:
  - Uses both strict and lenient scoring to provide a balanced view of the model’s performance.
- **Customizable Top-K**:
  - Evaluates MRR and lenient accuracy based on the top `K` responses.
- **Normalization**:
  - Handles variations in capitalization, punctuation, and special characters for fair comparisons.

---

**Usage**:
To run the evaluation script:
```bash
python evaluate_model.py
```

# How to Use

## Clone the Repository:
```bash
git clone https://github.com/Mahdiar-Khodabakhshi/Bioask-taskb-Incontext-learning-evaluation.git
cd Bioask-taskb-Incontext-learning-evaluation
```

## Install Dependencies:
```bash
pip install -r requirements.txt
```

## Run Scripts in Sequence:

### Step 1: Data Cleaning:
```bash
python data_cleaning.py
```

### Step 2: Generate Answers:
```bash
python answer_generator_llama.ipynb
```

### Step 3: Validate JSON:
```bash
python validate_json.py
```

### Step 4: Evaluate Model:
```bash
python evaluate_model.py
```
