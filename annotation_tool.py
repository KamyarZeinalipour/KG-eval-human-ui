import os
import time
import gradio as gr
import pandas as pd
import fire

def get_start_index(anns_filepath, start_index):
    anns_df = pd.read_csv(anns_filepath)
    return max([start_index] + anns_df.index.tolist()) + 1

def main(current_index: int = 0, annotator_name: str = "", examples_batch_folder: str = ''):
    css = """
    body, input, textarea, button { 
        font-family: Arial, sans-serif; 
    }
    """

    assert annotator_name, "Annotator name MISSING. Set it when you launch the script"
    assert examples_batch_folder, "Examples' batch MISSING. Set it when you launch the script"

    _, dataset_filename = os.path.split(examples_batch_folder)
    chunk_df = pd.read_csv(examples_batch_folder)
    
    # Ensure required columns exist and fill NaN with '[empty]'
    for col in ['oreginal triple', 'generated text', 'generated triple']:
        if col not in chunk_df.columns:
            chunk_df[col] = '[empty]'
        else:
            chunk_df[col] = chunk_df[col].fillna('[empty]')
    
    annotations_folder = os.path.join(os.getcwd(), "annotations")
    anns_filepath = os.path.join(annotations_folder, f"annotations_{dataset_filename}")

    if os.path.exists(anns_filepath):
        current_index = get_start_index(anns_filepath, current_index)
    else:
        os.makedirs(annotations_folder, exist_ok=True)

    print(f"Resume annotations process from {current_index}")
    df_row = chunk_df.iloc[current_index]

    # Function to store annotations and get the next data entry
    def store_annotation_and_get_next(
        curr_idx, comments,
        content_accuracy_rating,
        structure_grammar_fluency_rating,
        originality_engagement_creativity_rating,
        generated_triple_rating
    ):
        # Check if any rating is missing
        ratings = [
            content_accuracy_rating,
            structure_grammar_fluency_rating,
            originality_engagement_creativity_rating,
            generated_triple_rating
        ]
        if any(rating is None or rating == '' or rating == [] for rating in ratings):
            # Keep the Validate button disabled if ratings are missing
            return [
                curr_idx, gr.update(interactive=False),
                df_row['oreginal triple'],
                df_row['generated text'],
                content_accuracy_rating,
                structure_grammar_fluency_rating,
                originality_engagement_creativity_rating,
                comments,
                df_row['generated triple'], generated_triple_rating
            ]

        if not comments:
            comments = "No Comments"    

        if os.path.exists(anns_filepath):
            anns_df = pd.read_csv(anns_filepath)
        else:
            cols = chunk_df.columns.tolist()
            additional_cols = [
                "timestamp", "annotator", "comments",
                "Content and Related Accuracy Rating",
                "Structure, Grammar, and Fluency Rating",
                "Originality, Engagement, and Creativity Rating",
                "Generated Triple Rating"
            ]
            cols.extend(additional_cols)
            anns_df = pd.DataFrame(columns=cols)

        row = chunk_df.iloc[curr_idx].to_dict()
        row["timestamp"] = time.time()
        row["annotator"] = annotator_name
        row["comments"] = comments
        row["Content and Related Accuracy Rating"] = content_accuracy_rating
        row["Structure, Grammar, and Fluency Rating"] = structure_grammar_fluency_rating
        row["Originality, Engagement, and Creativity Rating"] = originality_engagement_creativity_rating
        row["Generated Triple Rating"] = generated_triple_rating

        anns_df = pd.concat((anns_df, pd.DataFrame(row, index=[0])), ignore_index=True)
        anns_df.to_csv(anns_filepath, index=False)

        next_idx = curr_idx + 1
        if next_idx < len(chunk_df):
            next_df_row = chunk_df.iloc[next_idx]
            return [
                next_idx, gr.update(interactive=False),
                next_df_row['oreginal triple'],
                next_df_row['generated text'],
                None, None, None, '',  # Reset ratings and comments
                next_df_row['generated triple'], None
            ]
        else:
            return [
                curr_idx, gr.update(interactive=False),
                "End of dataset", "End of dataset", None, None, None,
                "End of dataset",
                "End of dataset", None
            ]

    # Function to enable or disable the Validate button based on ratings
    def enable_button(
        content_accuracy_rating_value,
        structure_grammar_fluency_rating_value,
        originality_engagement_creativity_rating_value,
        generated_triple_rating_value
    ):
        ratings = [
            content_accuracy_rating_value,
            structure_grammar_fluency_rating_value,
            originality_engagement_creativity_rating_value,
            generated_triple_rating_value
        ]
        if all(ratings):
            return gr.update(interactive=True)
        else:
            return gr.update(interactive=False)

    with gr.Blocks(theme=gr.themes.Soft(), css=css) as demo:
        index = gr.Number(value=current_index, visible=False, precision=0)

        gr.Markdown(f"#### Annotating: {dataset_filename}\n")
        with gr.Row():
            with gr.Column():
                # Display the 'oreginal triple' field
                oreginal_triple = gr.Textbox(
                    label="Original Triple", interactive=False, value=df_row['oreginal triple']
                )
                # Display the 'generated text' field
                generated_text = gr.Textbox(
                    label="Generated Text", interactive=False, value=df_row['generated text']
                )

                # Radio buttons for 'Content and Related Accuracy Rating'
                content_accuracy_rating = gr.Radio(
                    ["A", "B", "F", "Skipping"], 
                    label="Content and Related Accuracy Rating"
                )

                # Definitions for 'Content and Related Accuracy Rating'
                gr.Markdown("**Definitions for Content and Related Accuracy Rating:**")
                gr.Markdown("""
                - **Rating-A**: *Gold Standard* - The content is fully accurate and completely aligns with the original data.
                - **Rating-B**: *Silver Standard* - The content is mostly accurate with minor deviations from the original data.
                - **Rating-F**: *Insufficient* - The content is inaccurate or does not align with the original data.
                - **Skipping**: Skip this entry if you cannot provide a rating.
                """)

                # Radio buttons for 'Structure, Grammar, and Fluency Rating'
                structure_grammar_fluency_rating = gr.Radio(
                    ["A", "B", "F", "Skipping"], 
                    label="Structure, Grammar, and Fluency Rating"
                )

                # Definitions for 'Structure, Grammar, and Fluency Rating'
                gr.Markdown("**Definitions for Structure, Grammar, and Fluency Rating:**")
                gr.Markdown("""
                - **Rating-A**: *Gold Standard* - The text is well-structured, grammatically correct, and reads fluently.
                - **Rating-B**: *Silver Standard* - The text has minor structural or grammatical errors but remains understandable.
                - **Rating-F**: *Insufficient* - The text has significant grammatical or structural issues that hinder understanding.
                - **Skipping**: Skip this entry if you cannot provide a rating.
                """)

                # Radio buttons for 'Originality, Engagement, and Creativity Rating'
                originality_engagement_creativity_rating = gr.Radio(
                    ["A", "B", "F", "Skipping"], 
                    label="Originality, Engagement, and Creativity Rating"
                )

                # Definitions for 'Originality, Engagement, and Creativity Rating'
                gr.Markdown("**Definitions for Originality, Engagement, and Creativity Rating:**")
                gr.Markdown("""
                - **Rating-A**: *Gold Standard* - The content is highly original, engaging, and creatively presented.
                - **Rating-B**: *Silver Standard* - The content shows some originality and is moderately engaging.
                - **Rating-F**: *Insufficient* - The content lacks originality and fails to engage the reader.
                - **Skipping**: Skip this entry if you cannot provide a rating.
                """)

                # Comments box
                comments = gr.Textbox(label="Comments")

                # Validate button (will be enabled based on ratings)
                eval_btn = gr.Button("Save and Continue", interactive=False)

            with gr.Column():
                # Display the 'generated triple' field
                generated_triple = gr.Textbox(
                    label="Generated Triple", interactive=False, value=df_row['generated triple']
                )

                # Radio buttons for 'Generated Triple Rating'
                generated_triple_rating = gr.Radio(
                    ["A", "B", "F", "Skipping"], 
                    label="Generated Triple Rating"
                )

                # Definitions for 'Generated Triple Rating'
                gr.Markdown("**Definitions for Generated Triple Rating:**")
                gr.Markdown("""
                - **Rating-A**: *Gold Standard* - The generated triple accurately represents the information from the generated text.
                - **Rating-B**: *Silver Standard* - The generated triple mostly represents the information with minor inaccuracies.
                - **Rating-F**: *Insufficient* - The generated triple is inaccurate or does not represent the generated text.
                - **Skipping**: Skip this entry if you cannot provide a rating.
                """)

            # Function to update the Validate button based on ratings
            def update_validate_button(
                content_accuracy_rating_value,
                structure_grammar_fluency_rating_value,
                originality_engagement_creativity_rating_value,
                generated_triple_rating_value
            ):
                return enable_button(
                    content_accuracy_rating_value,
                    structure_grammar_fluency_rating_value,
                    originality_engagement_creativity_rating_value,
                    generated_triple_rating_value
                )

            # Attach change events to ratings
            content_accuracy_rating.change(
                update_validate_button,
                inputs=[
                    content_accuracy_rating,
                    structure_grammar_fluency_rating,
                    originality_engagement_creativity_rating,
                    generated_triple_rating
                ],
                outputs=eval_btn
            )
            structure_grammar_fluency_rating.change(
                update_validate_button,
                inputs=[
                    content_accuracy_rating,
                    structure_grammar_fluency_rating,
                    originality_engagement_creativity_rating,
                    generated_triple_rating
                ],
                outputs=eval_btn
            )
            originality_engagement_creativity_rating.change(
                update_validate_button,
                inputs=[
                    content_accuracy_rating,
                    structure_grammar_fluency_rating,
                    originality_engagement_creativity_rating,
                    generated_triple_rating
                ],
                outputs=eval_btn
            )
            generated_triple_rating.change(
                update_validate_button,
                inputs=[
                    content_accuracy_rating,
                    structure_grammar_fluency_rating,
                    originality_engagement_creativity_rating,
                    generated_triple_rating
                ],
                outputs=eval_btn
            )

            # Click event for the Validate button
            eval_btn.click(
                store_annotation_and_get_next,
                inputs=[
                    index, comments,
                    content_accuracy_rating,
                    structure_grammar_fluency_rating,
                    originality_engagement_creativity_rating,
                    generated_triple_rating
                ],
                outputs=[
                    index, eval_btn,
                    oreginal_triple,
                    generated_text,
                    content_accuracy_rating,
                    structure_grammar_fluency_rating,
                    originality_engagement_creativity_rating,
                    comments,
                    generated_triple, generated_triple_rating
                ]
            )

        demo.launch()

if __name__ == "__main__":
    fire.Fire(main)
