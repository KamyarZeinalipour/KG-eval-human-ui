# KG Annotation Tool

This project is an interactive text annotation tool built with Python and Gradio. It enables annotators to rate text examples on three different dimensions and also provides the ability to go back and edit previous annotations.

## Features

- Display and rate text samples using three different rating categories:
  - Content and Related Accuracy Rating (A, B, F, Skipping)
  - Structure, Grammar, and Fluency Rating (A, B, F, Skipping)
  - Originality, Engagement, and Creativity Rating (A, B, F, Skipping)
- Save annotations to a CSV file. If an annotation for a particular sample already exists (tracked by the sample's index), it updates the annotation instead of creating a new one.
- “Go Back” functionality lets annotators navigate to the preceding example and review or modify their ratings and comments.

## Requirements

The code requires the following Python packages:

- [gradio](https://pypi.org/project/gradio/)
- [pandas](https://pypi.org/project/pandas/)
- [fire](https://pypi.org/project/fire/)

You can install all dependencies by running the command below (assuming you have a `requirements.txt` file in your project):

    pip install -r requirements.txt

If you don't yet have a `requirements.txt`, you can create one with the following content:

    gradio
    pandas
    fire

## How to Run

1. Ensure you have installed the dependencies using:

       pip install -r requirements.txt

2. Place your example text batch CSV file (which should contain at least the columns `initial_text` and `input_text`) in a known folder.

3. Run the annotation tool from the command-line. For example:

       python annotation_tool.py --current_index=0 --annotator_name="YourName" --examples_batch_folder="/path/to/your/examples.csv"

   Replace:
   - `your_script.py` with the name of your Python script.
   - `YourName` with your annotator name.
   - `/path/to/your/examples.csv` with the path to your batch file.

Once running, a web interface will appear (usually in your default browser). In the interface you can:
- View the initial text and input text on the left.
- Rate each sample using the three radio buttons on the right.
- Submit the annotation using the **Save and Continue** button.
- Click the **Go Back** button to navigate to the previous annotation and edit ratings/comments if necessary.

## File Structure

- **your_script.py**  
  The main Python script that initializes the Gradio interface, handles saving annotations (and updates), and navigation back to previous examples.

- **annotations/**  
  A folder (created automatically) where the annotated CSV file is stored. The annotations file is automatically named based on the original dataset.

- **requirements.txt**  
  The list of dependencies needed to run the project.

## License

This project is released under the MIT License.  
Please see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues regarding the project, please contact:
kamyar.zeinalipour2@unisi.it
Kamyar Zeinalipour
