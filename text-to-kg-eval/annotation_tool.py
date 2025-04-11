#!/usr/bin/env python3
import gradio as gr
import pandas as pd
import time
import os

# ----- CONFIGURATION -----
CSV_PATH = input("Enter your file name: ")
PROGRESS_FILE = "progress.txt"  # File to store the next index

# ----- GLOBALS -----
# Load the CSV file.
if os.path.exists(CSV_PATH):
    df = pd.read_csv(CSV_PATH)
else:
    raise FileNotFoundError(f"CSV file not found at {CSV_PATH}")

# Ensure the annotation columns exist.
new_columns = {
    "rating_model_kg_mian": "",
    "rating_model_kg_lora": "",
    "preferred_kg": "",
    "annotator": "",
    "annotation_time": ""
}
for col, default in new_columns.items():
    if col not in df.columns:
        df[col] = default

TOTAL_EXAMPLES = len(df)

annotator = input("Enter your annotator name: ").strip()
while annotator == "":
    annotator = input("Please enter a valid annotator name: ").strip()

current_start_time = None

def find_resume_index():
    """Return the first row where either rating field is empty."""
    for i, row in df.iterrows():
        if (pd.isna(row['rating_model_kg_mian']) or row['rating_model_kg_mian'] == "") \
           or (pd.isna(row['rating_model_kg_lora']) or row['rating_model_kg_lora'] == ""):
            return i
    return len(df)-1

def load_progress():
    """Load the index from the progress file, if it exists and is valid."""
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r") as f:
                idx = int(f.read().strip())
            # If the stored index is out of range or already completed, fall back.
            if idx < 0 or idx >= len(df):
                return find_resume_index()
            # If this row is already complete, use find_resume_index()
            row = df.loc[idx]
            if (row["rating_model_kg_mian"] != "" and row["rating_model_kg_lora"] != ""):
                return find_resume_index()
            return idx
        except Exception as e:
            print("Error reading progress file:", e)
            return find_resume_index()
    else:
        return find_resume_index()

def save_progress(idx):
    """Save the next index to a file for persistence between runs."""
    with open(PROGRESS_FILE, "w") as f:
        f.write(str(idx))

def load_example(idx):
    global current_start_time
    # Check bounds.
    if idx < 0 or idx >= len(df):
        return "Index out of range", "", "", None, None, None
    row = df.loc[idx]
    current_start_time = time.time()
    
    context_text = row["input_text"]
    text_model1 = row["generated_text_base"]
    text_model2 = row["generated_text_lora"]
    rating1 = row["rating_model_kg_mian"] if row["rating_model_kg_mian"] != "" else None
    rating2 = row["rating_model_kg_lora"] if row["rating_model_kg_lora"] != "" else None

    if row["preferred_kg"] != "":
        try:
            preferred_value = str(int(float(row["preferred_kg"])))
        except Exception as e:
            preferred_value = row["preferred_kg"]
    else:
        preferred_value = None

    return context_text, text_model1, text_model2, rating1, rating2, preferred_value

def format_index_text(idx):
    return f"Example {idx+1} out of {TOTAL_EXAMPLES}"

def submit_annotation(idx, rating1, rating2, preferred):
    global current_start_time, df, annotator

    if (rating1 is None) or (rating2 is None) or (preferred is None):
        # If any rating is not selected show an error.
        context_text, text_model1, text_model2, saved_rating1, saved_rating2, saved_preferred = load_example(idx)
        error_message = "Error: Please select a value for all fields before submitting."
        return (idx, format_index_text(idx),
                context_text, text_model1, text_model2,
                saved_rating1, saved_rating2, saved_preferred, error_message)
    
    # Update annotation time.
    annotation_duration = time.time() - current_start_time if current_start_time else 0

    # Save annotations.
    df.at[idx, "rating_model_kg_mian"] = str(rating1)
    df.at[idx, "rating_model_kg_lora"] = str(rating2)
    df.at[idx, "preferred_kg"] = str(preferred)
    df.at[idx, "annotator"] = annotator
    df.at[idx, "annotation_time"] = annotation_duration
    df.to_csv(CSV_PATH, index=False)
    
    # Determine next index.
    next_idx = find_resume_index()
    save_progress(next_idx)

    context_text, text_model1, text_model2, saved_rating1, saved_rating2, saved_preferred = load_example(next_idx)
    message = f"Annotation took {annotation_duration:.2f} seconds."
    return (next_idx, format_index_text(next_idx),
            context_text, text_model1, text_model2,
            saved_rating1, saved_rating2, saved_preferred,
            message)

def go_previous(current_idx):
    new_idx = current_idx - 1 if current_idx > 0 else 0
    context_text, text_model1, text_model2, saved_rating1, saved_rating2, saved_preferred = load_example(new_idx)
    save_progress(new_idx)
    return (new_idx, format_index_text(new_idx),
            context_text, text_model1, text_model2,
            saved_rating1, saved_rating2, saved_preferred)

# ----- BUILD THE GRADIO INTERFACE -----
with gr.Blocks() as demo:
    
    # Initialize current index from progress file.
    current_index_state = gr.State(load_progress())
    
    gr.Markdown("## Annotation Tool")
    with gr.Column():
        gr.Markdown(f"Annotator: {annotator}")
        current_index_txt = gr.Textbox(label="Current Example Index", interactive=False)
        
        original_text = gr.Textbox(label="Context", interactive=False, lines=5)
        model1_text = gr.Textbox(label="Generated KG (Model 1)", interactive=False, lines=5)
        model2_text = gr.Textbox(label="Generated KG (Model 2)", interactive=False, lines=5)
        
        rating_options = ["A", "B", "C", "D", "E"]
        rating_model1 = gr.Radio(choices=rating_options, label="Rating for Model 1", value=None)
        rating_model2 = gr.Radio(choices=rating_options, label="Rating for Model 2", value=None)
        
        preferred_trans = gr.Radio(choices=["Model 1", "Model 2"], label="Preferred Generation", value=None)
        
        with gr.Row():
            submit_btn = gr.Button("Submit Annotation")
            prev_btn = gr.Button("Previous")
        
        annotation_message = gr.Markdown("")
    
    submit_btn.click(
        submit_annotation,
        inputs=[current_index_state, rating_model1, rating_model2, preferred_trans],
        outputs=[current_index_state, current_index_txt,
                 original_text, model1_text, model2_text,
                 rating_model1, rating_model2, preferred_trans, annotation_message]
    )
    
    prev_btn.click(
        go_previous,
        inputs=current_index_state,
        outputs=[current_index_state, current_index_txt,
                 original_text, model1_text, model2_text,
                 rating_model1, rating_model2, preferred_trans]
    )
    
    def load_initial():
        idx = load_progress()  # use the persisted progress
        context_text, text_model1, text_model2, saved_rating1, saved_rating2, saved_preferred = load_example(idx)
        return (idx, format_index_text(idx),
                context_text, text_model1, text_model2,
                saved_rating1, saved_rating2, saved_preferred, "")
    
    demo.load(load_initial, inputs=[], outputs=[current_index_state, current_index_txt,
                                                 original_text, model1_text, model2_text,
                                                 rating_model1, rating_model2, preferred_trans, annotation_message])
    
demo.launch()
