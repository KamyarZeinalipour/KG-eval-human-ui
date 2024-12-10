# README

## Annotator Evaluation Tool for KG Triples and Generated Text

This tool provides an interactive interface for annotators to evaluate generated text from Knowledge Graph (KG) triples and the regenerated triples from that text using Large Language Models (LLMs). It streamlines the annotation process, allowing annotators to provide ratings and comments on the quality and accuracy of the generated content.

The tool is built using Python, Gradio for the web interface, and Pandas for data handling. It collects annotations and saves them to a CSV file for further analysis.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Command-Line Arguments](#command-line-arguments)
  - [Running the Tool](#running-the-tool)
- [Interface Overview](#interface-overview)
  - [Input Fields](#input-fields)
  - [Rating Categories](#rating-categories)
  - [Ratings Definitions](#ratings-definitions)
- [Annotation Process](#annotation-process)
- [Output](#output)
- [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Interactive Annotation Interface**: Provides a user-friendly interface for annotators to evaluate generated text and triples.
- **Customizable Ratings**: Allows for detailed ratings across multiple categories with clear definitions.
- **Data Persistence**: Saves annotations to CSV files for later analysis.
- **Progress Tracking**: Remembers the last annotated entry and resumes from there.
- **Error Handling**: Ensures that incomplete annotations are not saved and prompts annotators to complete all fields.

---

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/KamyarZeinalipour/KG-eval-human-ui.git
   cd KG-eval-human-ui
   ```

2. **Create a Virtual Environment** (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   **Dependencies**:

   - Python 3.x
   - Gradio
   - Pandas
   - Fire

---

## Usage

### Command-Line Arguments

- `current_index` (optional): The index to start annotation from (default is `0`).
- `annotator_name`: **(Required)** Name or identifier for the annotator.
- `examples_batch_folder`: **(Required)** Path to the CSV file containing the batch of examples to annotate.

### Running the Tool

Run the script using the command line:

```bash
python annotation_tool.py --annotator_name="YourName" --examples_batch_folder="path/to/your/dataset.csv"
```

**Example**:

```bash
python annotation_tool.py --annotator_name="Alice" --examples_batch_folder="./data/kg_triples.csv"
```

---

## Interface Overview

When you run the script, a local Gradio web interface will launch in your default web browser.

### Input Fields

- **Original Triple**: Displays the original Knowledge Graph triple(s).
- **Generated Text**: Shows the text generated from the original triple(s).
- **Generated Triple**: Presents the triple(s) regenerated from the generated text.

### Rating Categories

Annotators are required to provide ratings in the following categories:

1. **Content and Related Accuracy Rating**
2. **Structure, Grammar, and Fluency Rating**
3. **Originality, Engagement, and Creativity Rating**
4. **Generated Triple Rating**

Each rating category has four options:

- **Rating-A**
- **Rating-B**
- **Rating-F**
- **Skipping**

### Rating Definitions

#### 1. Content and Related Accuracy Rating

- **Rating-A**: *Gold Standard* - The content is fully accurate and completely aligns with the original data.
- **Rating-B**: *Silver Standard* - The content is mostly accurate with minor deviations from the original data.
- **Rating-F**: *Insufficient* - The content is inaccurate or does not align with the original data.
- **Skipping**: Skip this entry if you cannot provide a rating.

#### 2. Structure, Grammar, and Fluency Rating

- **Rating-A**: *Gold Standard* - The text is well-structured, grammatically correct, and reads fluently.
- **Rating-B**: *Silver Standard* - The text has minor structural or grammatical errors but remains understandable.
- **Rating-F**: *Insufficient* - The text has significant grammatical or structural issues that hinder understanding.
- **Skipping**: Skip this entry if you cannot provide a rating.

#### 3. Originality, Engagement, and Creativity Rating

- **Rating-A**: *Gold Standard* - The content is highly original, engaging, and creatively presented.
- **Rating-B**: *Silver Standard* - The content shows some originality and is moderately engaging.
- **Rating-F**: *Insufficient* - The content lacks originality and fails to engage the reader.
- **Skipping**: Skip this entry if you cannot provide a rating.

#### 4. Generated Triple Rating

- **Rating-A**: *Gold Standard* - The generated triple accurately represents the information from the generated text.
- **Rating-B**: *Silver Standard* - The generated triple mostly represents the information with minor inaccuracies.
- **Rating-F**: *Insufficient* - The generated triple is inaccurate or does not represent the generated text.
- **Skipping**: Skip this entry if you cannot provide a rating.

---

## Annotation Process

1. **Review the Original Triple**: Read the original Knowledge Graph triple(s) provided.
2. **Examine the Generated Text**: Read the text generated from the original triple(s).
3. **Assess the Generated Triple**: Look at the triple(s) regenerated from the generated text.
4. **Provide Ratings**: For each of the four categories, select a rating based on the definitions provided.
   - **Content and Related Accuracy Rating**
   - **Structure, Grammar, and Fluency Rating**
   - **Originality, Engagement, and Creativity Rating**
   - **Generated Triple Rating**
5. **Add Comments** (Optional but encouraged): Provide any additional insights or notes about the annotation.
6. **Validate**: Once all ratings are selected, the "Validate" button becomes enabled. Click it to submit your annotation.
7. **Proceed to Next Entry**: The tool will automatically load the next entry. Repeat the process.

**Note**: If any rating is missing, the "Validate" button will remain disabled to prevent incomplete submissions.

---

## Output

Annotated data is saved in a CSV file located in the `annotations` folder, named `annotations_{dataset_filename}`.

**Saved Information Includes**:

- Original data from the input CSV (e.g., `original triple`, `generated text`, `generated triple`).
- Timestamp of the annotation.
- Annotator's name.
- Comments.
- Ratings for each category:
  - `Content and Related Accuracy Rating`
  - `Structure, Grammar, and Fluency Rating`
  - `Originality, Engagement, and Creativity Rating`
  - `Generated Triple Rating`

**Example Output Row**:

| timestamp    | annotator | comments      | Content and Related Accuracy Rating | Structure, Grammar, and Fluency Rating | Originality, Engagement, and Creativity Rating | Generated Triple Rating | original triple                   | generated text                                                                                  | generated triple                 |
|--------------|-----------|---------------|-------------------------------------|----------------------------------------|-----------------------------------------------|-------------------------|-----------------------------------|------------------------------------------------------------------------------------------------|-----------------------------------|
| 1631234567.8 | Alice     | Well written. | A                                   | A                                      | B                                             | A                       | (Paris, capital of, France)       | "Paris is the capital city of France, known for its art, fashion, and culture."                | (Paris, capital of, France)       |

---

## Customization

You can modify the tool to suit your specific needs. Here are some ways to customize it:

- **Adjust Rating Options**: Modify the rating scales or categories in the code if your evaluation criteria change.
- **Change Definitions**: Update the rating definitions to match your project's guidelines.
- **Add New Fields**: Include additional input or output fields in the interface and CSV file.
- **Interface Design**: Customize the interface's appearance using Gradio's theming options or by modifying the CSS.

---

## Contributing

Contributions are welcome! If you have suggestions for improvements, please submit an issue or a pull request on the GitHub repository.

**To Contribute**:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes.
4. Submit a pull request explaining your changes.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

# Additional Details

## Dependencies

- **Python 3.x**: Ensure you have Python 3 installed.
- **Gradio**: Used for building the web interface. Install via `pip install gradio`.
- **Pandas**: For data manipulation and CSV handling. Install via `pip install pandas`.
- **Fire**: A library for creating command-line interfaces. Install via `pip install fire`.

## File Structure

- **`annotation_tool.py`**: The main script that runs the annotation tool.
- **`data/`**: Folder where your input CSV files are stored.
- **`annotations/`**: Folder where the output annotated CSV files are saved.
- **`requirements.txt`**: Lists all Python dependencies.

## Input Data Format

The input CSV file should contain at least the following columns:

- `origial triple` (or `original triple`)
- `generated text`
- `generated triple`

**Note**: The script ensures that these columns exist and fills any missing values with `[empty]`.

## Error Handling and Continuity

- The tool automatically resumes from the last annotated index if the annotation process is interrupted.
- It prevents incomplete annotations by disabling the "Validate" button until all ratings are provided.
- If the end of the dataset is reached, the tool displays a message indicating completion.

## Example Command

```bash
python annotation_tool.py --annotator_name="Bob" --examples_batch_folder="./data/sample_triples.csv"
```

## Contact

For any questions or support, please contact me by Kamyar.zeinalipour@unisi2.it.

---

# Rating Categories Detailed Descriptions

Below are the detailed descriptions for each rating in all categories to guide annotators in their evaluations.

---

## 1. Content and Related Accuracy Rating

**Purpose**: Assesses the factual correctness and alignment of the generated text with the original Knowledge Graph triples.

- **Rating-A**: *Gold Standard*
  - The generated text is completely accurate.
  - All information aligns perfectly with the original triples.
  - No factual errors or misinterpretations.
- **Rating-B**: *Silver Standard*
  - The text is mostly accurate.
  - Minor deviations or omissions that do not significantly affect the overall understanding.
  - Small inaccuracies that are acceptable but noticeable.
- **Rating-F**: *Insufficient*
  - Significant inaccuracies in the text.
  - Misrepresentation of the information from the triples.
  - Contains factual errors that could mislead the reader.
- **Skipping**:
  - Use if you cannot provide a rating due to ambiguity or lack of understanding.

## 2. Structure, Grammar, and Fluency Rating

**Purpose**: Evaluates the readability and technical writing quality of the generated text.

- **Rating-A**: *Gold Standard*
  - The text is well-structured and flows logically.
  - Free of grammatical errors.
  - Sentences are clear and concise.
- **Rating-B**: *Silver Standard*
  - Minor grammatical or structural errors.
  - The text remains understandable.
  - Minor issues that do not impede comprehension.
- **Rating-F**: *Insufficient*
  - Significant grammatical errors.
  - Poor sentence structure.
  - Difficult to read or understand due to errors.
- **Skipping**:
  - Use if you cannot provide a rating due to ambiguity or lack of understanding.

## 3. Originality, Engagement, and Creativity Rating

**Purpose**: Measures how engaging and creatively the information is presented in the generated text.

- **Rating-A**: *Gold Standard*
  - Highly original and engaging content.
  - Creative presentation that captures the reader's interest.
  - Uses compelling language and examples.
- **Rating-B**: *Silver Standard*
  - Shows some originality and engagement.
  - Moderately interesting to read.
  - Could be more creative or engaging but still acceptable.
- **Rating-F**: *Insufficient*
  - Lacks originality.
  - The text is dull or uninteresting.
  - Fails to engage the reader.
- **Skipping**:
  - Use if you cannot provide a rating due to ambiguity or lack of understanding.

## 4. Generated Triple Rating

**Purpose**: Evaluate the accuracy and completeness of the triple(s) generated from the generated text.

- **Rating-A**: *Gold Standard*
  - The generated triple accurately reflects the information in the text.
  - No missing elements or inaccuracies.
  - Properly formatted and complete.
- **Rating-B**: *Silver Standard*
  - Mostly accurate with minor inaccuracies or omissions.
  - The main information is captured but could be improved.
- **Rating-F**: *Insufficient*
  - Inaccurate or incomplete triple.
  - Does not represent the information from the text correctly.
- **Skipping**:
  - Use if you cannot provide a rating due to ambiguity or lack of understanding.

---

By adhering to these detailed descriptions, annotators can provide consistent and objective evaluations of the generated content, contributing to the overall quality and reliability of the dataset.

Feel free to copy and paste these sections into your own README or documentation as needed.

---

# Example Evaluation

Here's an example of how to use the tool and apply the ratings.

**Original Triple**:

- `(The Eiffel Tower, located in, Paris)`
- `(The Eiffel Tower, height, 324 meters)`
- `(The Eiffel Tower, built in, 1889)`

**Generated Text**:

> "Standing tall in the heart of Paris, the Eiffel Tower was constructed in 1889 and reached a height of 324 meters."

**Generated Triple**:

- `(The Eiffel Tower, constructed in, 1889)`
- `(The Eiffel Tower, has height, 324 meters)`
- `(The Eiffel Tower, located in, Paris)`

**Annotations**:

1. **Content and Related Accuracy Rating**: **Rating-A**
   - The generated text accurately reflects all the information from the original triples.
2. **Structure, Grammar, and Fluency Rating**: **Rating-A**
   - The text is well-written, grammatically correct, and flows naturally.
3. **Originality, Engagement, and Creativity Rating**: **Rating-A**
   - The text is engaging and presents the information creatively.
4. **Generated Triple Rating**: **Rating-A**
   - The regenerated triples accurately represent the information from the generated text.

**Comments**:

- "Excellent representation and presentation of the original data. The text is engaging and accurate."

---

# Frequently Asked Questions (FAQ)

**Q1**: What if I disagree with the previous annotations?

**A1**: This tool operates on a per-annotator basis. If you encounter previously annotated entries, provide your own evaluations based on your judgment.

**Q2**: Can I pause and resume the annotation process?

**A2**: Yes. The tool saves your progress, and you can resume from where you left off by running the script again with the same parameters.

**Q3**: How are the annotations stored?

**A3**: Annotations are saved in a CSV file within the `annotations` folder. Each submission appends a new row to this file.

**Q4**: What does the "Skipping" option do?

**A4**: Selecting "Skipping" allows you to move past an entry you cannot evaluate. The tool records that the entry was skipped.

**Q5**: Can I modify the rating scales or categories?

**A5**: Yes. You can adjust the code to change rating options or add new categories as needed.

---

# Contact Information

For any inquiries or support regarding this tool, please contact:

- **Name**: Kamyar Zeinalipour
- **Email**: Kamyar.zeinalipour@unisi2.it
- **GitHub**: [KamyarZeinalipour](https://github.com/KamyarZeinalipour/)

---


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.


