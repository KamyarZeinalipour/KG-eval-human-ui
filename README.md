# Annotation Tool for Evaluating Generated Text and Regenerated Triples from KG Triples

This tool provides an interactive interface for annotators to evaluate generated text from Knowledge Graph (KG) triples and the regenerated triples from that text using Large Language Models (LLMs). It streamlines the annotation process, allowing annotators to provide ratings and comments on the quality and accuracy of the generated content.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the Annotation Tool](#running-the-annotation-tool)
  - [Annotation Interface](#annotation-interface)
- [Sample Data](#sample-data)
- [Output](#output)
- [Customization](#customization)
- [Notes](#notes)
- [License](#license)

## Overview

In the realm of Knowledge Graphs, transforming triples into natural language text and then back into triples using LLMs is a common task. Evaluating the quality of this process is crucial for improving the performance of LLMs and ensuring the accuracy of the regenerated triples.

This annotation tool facilitates this evaluation by presenting annotators with original KG triples, generated text from those triples, and regenerated triples from the generated text. Annotators can assess the quality of the generated text and the regenerated triples, providing ratings and comments to guide improvements.

## Features

- **Interactive Annotation Interface**: Utilizes Gradio to create a user-friendly web interface.
- **Rating System**: Allows annotators to rate both the generated text and the regenerated triples using predefined criteria.
- **Comments Section**: Annotators can provide additional feedback or notes.
- **Progress Tracking**: Remembers the current position in the dataset, allowing annotators to resume where they left off.
- **Data Persistence**: Saves annotations to a CSV file for further analysis.

## Prerequisites

- **Python 3.6 or later**
- **Pip package manager**

## Installation

1. **Clone the Repository (if applicable)**:

   ```bash
   git clone https://github.com/yourusername/annotation-tool.git
   cd annotation-tool
   ```

2. **Install Required Python Libraries**:

   Install the necessary Python packages using `pip`:

   ```bash
   pip install gradio pandas fire
   ```

   If you encounter any permissions issues, you might need to use `pip3` or add `--user`:

   ```bash
   pip3 install gradio pandas fire --user
   ```

## Usage

### Running the Annotation Tool

To start the annotation tool, run the script `annotation_tool.py` with the required arguments:

```bash
python annotation_tool.py --annotator_name="Your Name" --examples_batch_folder="path_to_your_csv.csv"
```

- **Arguments**:
  - `--annotator_name`: *(Required)* Your name or identifier as an annotator.
  - `--examples_batch_folder`: *(Required)* Path to the CSV file containing the data to annotate.
  - `--current_index`: *(Optional)* The index to start annotation from (useful for resuming).

**Example**:

```bash
python annotation_tool.py --annotator_name="Alice" --examples_batch_folder="sample_data.csv"
```

### Annotation Interface

Upon running the script, a Gradio interface will launch in your default web browser. If it doesn't open automatically, look for a URL in the terminal output (e.g., `http://127.0.0.1:7860`) and open it in your browser.

**Interface Overview**:

- **Left Side**:
  - **Original Triple**: Displays the original KG triple.
  - **Generated Text**: Displays the text generated from the original triple.
  - **Generated Text Rating**: A radio button group where you can rate the quality of the generated text.
  - **Comments**: A textbox to add any comments or observations.

- **Right Side**:
  - **Generated Triple**: Shows the triple regenerated from the generated text by an LLM.
  - **Generated Triple Rating**: A radio button group where you can rate the quality of the regenerated triple.
  - **Ratings Definitions**: Describes the meaning of each rating for reference.

**Rating Options**:

- **A**: *Gold Standard* - The content is fully relevant and helpful.
- **B**: *Silver Standard* - The content is somewhat relevant and partially helpful.
- **F**: *Insufficient* - The content is not relevant or not helpful.
- **Skipping**: Skip this entry if you cannot provide a rating.

**Annotation Steps**:

1. **Review the Original Triple and Generated Text**:
   - Read the original KG triple.
   - Read the text generated from the triple.

2. **Provide Ratings**:
   - Select a rating for "Generated Text Rating".
   - Review the "Generated Triple" regenerated by the LLM.
   - Select a rating for "Generated Triple Rating".

3. **Add Comments** (Optional):
   - Provide any additional feedback or notes in the "Comments" box.

4. **Validate**:
   - The "Validate" button will become active once both ratings are selected.
   - Click "Validate" to save your annotations and proceed to the next entry.

5. **Proceed to Next Entry**:
   - The interface will automatically load the next entry.
   - Repeat the steps until all entries are annotated.

6. **Completion**:
   - Upon reaching the end of the dataset, an "End of dataset" message will appear.

**Notes**:

- If you need to pause, you can exit the interface, and the progress will be saved. When you restart the tool with the same `annotator_name` and `examples_batch_folder`, it will resume from where you left off.
- Ensure you do not close the terminal while annotating, as the interface relies on the running script.

## Sample Data

### Generating a Sample CSV File

For testing purposes, you can generate a sample CSV file using the provided script:

```python
import pandas as pd

# Sample data
data = {
    'oreginal triple': [
        'Person_A;works_at;Company_X',
        'Person_B;born_in;City_Y',
        'Person_C;married_to;Person_D'
    ],
    'generated text': [
        'Person A works at Company X.',
        'Person B was born in City Y.',
        'Person C is married to Person D.'
    ],
    'generated triple': [
        'Person_A;employed_by;Company_X',
        'Person_B;originates_from;City_Y',
        'Person_C;spouse;Person_D'
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('sample_data.csv', index=False)

print("Sample CSV file 'sample_data.csv' has been created.")
```

**Instructions**:

1. Save the above code to a file, e.g., `generate_sample_data.py`.
2. Run the script:

   ```bash
   python generate_sample_data.py
   ```

3. This will create a `sample_data.csv` file in the current directory.

**Sample CSV Structure**:

```csv
oreginal triple,generated text,generated triple
Person_A;works_at;Company_X,Person A works at Company X.,Person_A;employed_by;Company_X
Person_B;born_in;City_Y,Person B was born in City Y.,Person_B;originates_from;City_Y
Person_C;married_to;Person_D,Person C is married to Person D.,Person_C;spouse;Person_D
```

You can use this sample data to test the annotation tool:

```bash
python annotation_tool.py --annotator_name="Test Annotator" --examples_batch_folder="sample_data.csv"
```

## Output

- **Annotations File**:
  - Annotations are saved in a CSV file within an `annotations` folder in the current working directory.
  - The filename is prefixed with `annotations_` followed by the original dataset filename (e.g., `annotations_sample_data.csv`).

- **Content of the Annotations File**:
  - Includes all original data columns.
  - Adds additional columns:
    - `timestamp`: Unix timestamp when the annotation was made.
    - `annotator`: The annotator's name.
    - `comments`: The annotator's comments.
    - `Generated Text Rating`: The rating given to the generated text.
    - `Generated Triple Rating`: The rating given to the regenerated triple.

**Example of Annotations CSV**:

```csv
oreginal triple,generated text,generated triple,timestamp,annotator,comments,Generated Text Rating,Generated Triple Rating
Person_A;works_at;Company_X,Person A works at Company X.,Person_A;employed_by;Company_X,1697065800.123456,"Test Annotator","No Comments","A","B"
...
```

## Customization

- **Column Names**:
  - The script expects specific column names: `'oreginal triple'`, `'generated text'`, and `'generated triple'`.
  - If your dataset uses different column names, you can adjust the column names in the script accordingly.

- **Ratings Definitions**:
  - The definitions for ratings "A", "B", and "F" can be modified in the interface by editing the markdown sections in the script.

- **Annotation Fields**:
  - Additional fields or ratings can be added to the interface and saved in the annotations file by updating the script's UI components and the `store_annotation_and_get_next` function.

## Notes

- **Spelling**:
  - The term "oreginal triple" is used as per the original requirements.

- **Data Integrity**:
  - Ensure that the input CSV file is properly formatted and contains the required columns to prevent runtime errors.

- **Resuming Annotation**:
  - The tool tracks progress by checking the existing annotations file. If you need to restart annotations from a specific index, you can use the `--current_index` argument.

- **Dependencies**:
  - The tool relies on Gradio for the web interface and Pandas for data manipulation. These should be installed as per the instructions.

- **Port Configuration**:
  - By default, Gradio runs on port 7860. If this port is in use or you need to change it, you can modify the `demo.launch()` line in the script to specify a different port:

    ```python
    demo.launch(server_port=7861)
    ```

- **Security**:
  - The interface is intended for local use. If deploying over a network, consider the security implications and protect the interface appropriately.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

*For any issues or questions, please contact the project maintainer.*