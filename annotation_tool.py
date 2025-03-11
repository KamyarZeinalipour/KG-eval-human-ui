#!/usr/bin/env python3
import os
import time
import gradio as gr
import pandas as pd
import fire

def get_start_index(anns_filepath, start_index):
    # When resuming, we set the new index as one greater than the maximum annotated source_index.
    if os.path.exists(anns_filepath):
        anns_df = pd.read_csv(anns_filepath)
        if "source_index" in anns_df.columns and len(anns_df) > 0:
            return max([start_index] + anns_df["source_index"].tolist()) + 1
    return start_index

def main(current_index: int = 0, annotator_name: str = "", examples_batch_folder: str = ''):
    css = """
    body, input, textarea, button { 
        font-family: Arial, sans-serif; 
    }
    """

    assert annotator_name, "Annotator name MISSING. Set it when you launch the script"
    assert examples_batch_folder, "Examples' batch MISSING. Set it when you launch the script"

    # Get the dataset filename.
    _, dataset_filename = os.path.split(examples_batch_folder)
    chunk_df = pd.read_csv(examples_batch_folder)

    # Ensure the required columns exist (we now use 'initial_text' and 'input_text' only)
    for col in ['initial_text', 'input_text']:
        if col not in chunk_df.columns:
            chunk_df[col] = '[empty]'
        else:
            chunk_df[col] = chunk_df[col].fillna('[empty]')

    annotations_folder = os.path.join(os.getcwd(), "annotations")
    anns_filepath = os.path.join(annotations_folder, f"annotations_{dataset_filename}")

    os.makedirs(annotations_folder, exist_ok=True)

    # When resuming, check for existing annotations.
    current_index = get_start_index(anns_filepath, current_index)
    print(f"Resuming annotations process from index {current_index}")
    df_row = chunk_df.iloc[current_index]

    # This function now checks if an annotation already exists (using "source_index")
    # and updates it; otherwise, it appends a new row.
    def store_annotation_and_get_next(
        curr_idx, comments,
        content_accuracy_rating,
        structure_grammar_fluency_rating,
        originality_engagement_creativity_rating,
        prev_time  # hidden state: timestamp of previous click
    ):
        ratings = [content_accuracy_rating, structure_grammar_fluency_rating, originality_engagement_creativity_rating]
        # If any rating is missing, do not update or change the UI.
        if any(r is None or r == '' or r == [] for r in ratings):
            return [
                curr_idx, gr.update(interactive=False),
                df_row['initial_text'],
                df_row['input_text'],
                content_accuracy_rating,
                structure_grammar_fluency_rating,
                originality_engagement_creativity_rating,
                comments,
                prev_time 
            ]

        if not comments:
            comments = "No Comments"
            
        now = time.time()
        annotation_time = now - prev_time  # time difference

        # Load or create the annotations DataFrame.
        if os.path.exists(anns_filepath):
            anns_df = pd.read_csv(anns_filepath)
        else:
            cols = chunk_df.columns.tolist()
            additional_cols = [
                "timestamp", "annotator", "comments",
                "Content and Related Accuracy Rating",
                "Structure, Grammar, and Fluency Rating",
                "Originality, Engagement, and Creativity Rating",
                "annotation_time",
                "source_index"
            ]
            cols.extend(additional_cols)
            anns_df = pd.DataFrame(columns=cols)
        
        row = chunk_df.iloc[curr_idx].to_dict()
        # Remove any unwanted fields (if any)
        row.pop("generated triple", None)

        # Add annotation metadata.
        row["timestamp"] = now
        row["annotator"] = annotator_name
        row["comments"] = comments
        row["Content and Related Accuracy Rating"] = content_accuracy_rating
        row["Structure, Grammar, and Fluency Rating"] = structure_grammar_fluency_rating
        row["Originality, Engagement, and Creativity Rating"] = originality_engagement_creativity_rating
        row["annotation_time"] = annotation_time
        # Store the source index so we can update if the annotation is later edited.
        row["source_index"] = curr_idx

        # Update if an annotation with this source_index already exists.
        if "source_index" in anns_df.columns and (anns_df['source_index'] == curr_idx).any():
            idx_to_update = anns_df.index[anns_df['source_index'] == curr_idx][0]
            for key, value in row.items():
                anns_df.at[idx_to_update, key] = value
        else:
            # Append a new row.
            anns_df = pd.concat((anns_df, pd.DataFrame(row, index=[0])), ignore_index=True)
        
        anns_df.to_csv(anns_filepath, index=False)

        # Decide what the next index should be.
        next_idx = curr_idx + 1
        if next_idx < len(chunk_df):
            next_df_row = chunk_df.iloc[next_idx]
            # Reset all interactive selections when moving forward.
            return [
                next_idx, gr.update(interactive=False),
                next_df_row['initial_text'],
                next_df_row['input_text'],
                None, None, None, '',  # reset ratings and comments
                now  # update hidden state
            ]
        else:
            return [
                curr_idx, gr.update(interactive=False),
                "End of dataset", "End of dataset", None, None, None,
                "End of dataset",
                prev_time
            ]
        
    # This new function is called when the user clicks the "Go Back" button.
    # It decrements the index (if possible) and loads any already-saved ratings and comments.
    def load_prev_annotation(curr_idx, prev_time):
        # Do not go back if we're already at the first example.
        if curr_idx <= 0:
            return [curr_idx, gr.update(interactive=False),
                    chunk_df.iloc[curr_idx]['initial_text'],
                    chunk_df.iloc[curr_idx]['input_text'],
                    None, None, None, "", time.time()]
        new_idx = curr_idx - 1
        row = chunk_df.iloc[new_idx]

        # Try to load saved annotation from file.
        if os.path.exists(anns_filepath):
            anns_df = pd.read_csv(anns_filepath)
            if "source_index" in anns_df.columns and (anns_df['source_index'] == new_idx).any():
                saved_ann = anns_df.loc[anns_df['source_index'] == new_idx].iloc[-1]
                ca = saved_ann["Content and Related Accuracy Rating"]
                sg = saved_ann["Structure, Grammar, and Fluency Rating"]
                oe = saved_ann["Originality, Engagement, and Creativity Rating"]
                comm = saved_ann["comments"]
            else:
                ca, sg, oe, comm = None, None, None, ""
        else:
            ca, sg, oe, comm = None, None, None, ""
        now = time.time()
        return [new_idx, gr.update(interactive=False),
                row['initial_text'],
                row['input_text'],
                ca, sg, oe, comm,
                now]

    # Function to enable or disable the Validate button based on the three ratings.
    def enable_button(content_accuracy_rating_value, structure_grammar_fluency_rating_value, originality_engagement_creativity_rating_value):
        ratings = [content_accuracy_rating_value, structure_grammar_fluency_rating_value, originality_engagement_creativity_rating_value]
        if all(ratings):
            return gr.update(interactive=True)
        else:
            return gr.update(interactive=False)
    
    with gr.Blocks(theme=gr.themes.Soft(), css=css) as demo:
        # Hidden state for previous click time. Initialized to the current time.
        prev_time = gr.State(value=time.time())
        index = gr.Number(value=current_index, visible=False, precision=0)

        gr.Markdown(f"#### Annotating: {dataset_filename}\n")

        # Define a two-column layout.
        with gr.Row():
            # LEFT COLUMN: The rating radio buttons, definitions and comments.
            with gr.Column():
                initial_text_box = gr.Textbox(label="Initial Text", interactive=False, value=df_row['initial_text'])
                input_text_box = gr.Textbox(label="Input Text", interactive=False, value=df_row['input_text'])
                comments = gr.Textbox(label="Comments")
            # RIGHT COLUMN: The rating radio buttons.
            with gr.Column():
                content_accuracy_rating = gr.Radio(
                    ["A", "B", "F", "Skipping"],
                    label="Content and Related Accuracy Rating"
                )
                gr.Markdown("**Definitions for Content and Related Accuracy Rating:**")
                gr.Markdown("""
                - **Rating-A**: *Gold Standard* – The content is fully accurate and completely aligns with the original data.
                - **Rating-B**: *Silver Standard* – The content is mostly accurate with minor deviations.
                - **Rating-F**: *Insufficient* – The content is inaccurate or misaligned.
                - **Skipping**: Skip this entry if you cannot provide a rating.
                """)
                structure_grammar_fluency_rating = gr.Radio(
                    ["A", "B", "F", "Skipping"],
                    label="Structure, Grammar, and Fluency Rating"
                )
                gr.Markdown("**Definitions for Structure, Grammar, and Fluency Rating:**")
                gr.Markdown("""
                - **Rating-A**: *Gold Standard* – Well-structured, grammatically correct, and reads fluently.
                - **Rating-B**: *Silver Standard* – Minor grammatical or structural errors.
                - **Rating-F**: *Insufficient* – Significant grammatical or structural issues.
                - **Skipping**: Skip this entry if you cannot provide a rating.
                """)
                originality_engagement_creativity_rating = gr.Radio(
                    ["A", "B", "F", "Skipping"],
                    label="Originality, Engagement, and Creativity Rating"
                )
                gr.Markdown("**Definitions for Originality, Engagement, and Creativity Rating:**")
                gr.Markdown("""
                - **Rating-A**: *Gold Standard* – Highly original, engaging, and creatively presented.
                - **Rating-B**: *Silver Standard* – Some originality and moderate engagement.
                - **Rating-F**: *Insufficient* – Lacks originality and fails to engage.
                - **Skipping**: Skip this entry if you cannot provide a rating.
                """)
                
                # The main button to save the annotation and continue.
                eval_btn = gr.Button("Save and Continue", interactive=False)
                # New button to go back and edit a previous annotation.
                back_btn = gr.Button("Go Back", interactive=True)
        
        # Update the Validate button state when any radio selection changes.
        def update_validate_button(content_acc, structure_gram, originality_eng):
            return enable_button(content_acc, structure_gram, originality_eng)
        
        content_accuracy_rating.change(
            update_validate_button,
            inputs=[content_accuracy_rating, structure_grammar_fluency_rating, originality_engagement_creativity_rating],
            outputs=eval_btn
        )
        structure_grammar_fluency_rating.change(
            update_validate_button,
            inputs=[content_accuracy_rating, structure_grammar_fluency_rating, originality_engagement_creativity_rating],
            outputs=eval_btn
        )
        originality_engagement_creativity_rating.change(
            update_validate_button,
            inputs=[content_accuracy_rating, structure_grammar_fluency_rating, originality_engagement_creativity_rating],
            outputs=eval_btn
        )
        
        # When clicking Save and Continue, store (or update) the annotation and move forward.
        eval_btn.click(
            store_annotation_and_get_next,
            inputs=[index, comments,
                    content_accuracy_rating,
                    structure_grammar_fluency_rating,
                    originality_engagement_creativity_rating,
                    prev_time],
            outputs=[index, eval_btn,
                     initial_text_box,
                     input_text_box,
                     content_accuracy_rating,
                     structure_grammar_fluency_rating,
                     originality_engagement_creativity_rating,
                     comments,
                     prev_time]
        )
        
        # When clicking the Go Back button, load the previous annotation (if any).
        back_btn.click(
            load_prev_annotation,
            inputs=[index, prev_time],
            outputs=[index, eval_btn,
                     initial_text_box,
                     input_text_box,
                     content_accuracy_rating,
                     structure_grammar_fluency_rating,
                     originality_engagement_creativity_rating,
                     comments,
                     prev_time]
        )

        demo.launch()

if __name__ == "__main__":
    fire.Fire(main)
