import gradio as gr

def search_repos(query, search_type):
    # Placeholder function for searching repositories
    return [["Repo 1", "Description 1"], ["Repo 2", "Description 2"]]

def visualize_custom_view(custom_input):
    # Placeholder function for visualizing custom input
    pass

def update_selected_repo(selected_row):
    # Placeholder function to update selected repo info
    content_relevance = "85%"
    overview_text = "This is an overview of the selected repository."
    # Simulate similarity scores
    context_similarity = "90%"
    features_similarity = "80%"
    keyword_similarity = "85%"
    semantic_similarity = "88%"
    purpose_similarity = "82%"
    working_similarity = "87%"
    requirement_match_similarity = "83%"
    # Repo details
    repo_url = "Repo URL: [Link](https://github.com/example/repo)"
    fork_repo = "Fork Repo: Yes"
    star_repo = "Star Repo: 150 Stars"
    licensing_details = "Licensing Details: MIT License"
    return (content_relevance, overview_text, context_similarity, features_similarity, keyword_similarity,
            semantic_similarity, purpose_similarity, working_similarity, requirement_match_similarity,
            repo_url, fork_repo, star_repo, licensing_details)

with gr.Blocks(title="SEFGH-AI", css="""
    /* Adjust button sizes */
    #search_button button, #visualize_button button {
        width: 80px !important;
        height: 40px !important;
    }
    /* Make dropdown and buttons fit into one column */
    #search_type {
        width: 100% !important;
    }
    #search_button button {
        width: 100% !important;
    }
    
        /* Hide Gradio's default footer */
    footer {
        display: none !important;
    }
""") as demo:
    # Header
    gr.Markdown("# SEFGH - AI")

    # Navigation Tabs
    with gr.Tabs():
        with gr.TabItem("Home"):
            with gr.Row():
                # Search Input
                with gr.Column(scale=2):
                    # Search Section
                    gr.Markdown("## Search for GitHub Repositories")
                    gr.Markdown("Use the search input below to find GitHub repositories.")
                    search_input = gr.Textbox(
                        placeholder="Search for GitHub Repositories ...",
                        lines=5,  # Allow multiple lines
                        max_lines=10,
                        elem_id="search_input"
                    )
                # Search Button and Search Type Dropdown stacked in one column
                # noinspection PyTypeChecker
                with gr.Column(scale=0.5):
                    search_button = gr.Button("Search", variant="primary", elem_id="search_button")
                    search_type = gr.Dropdown(
                        choices=["quick", "exhaustive"],
                        value="quick",
                        label="Choose between quick or exhaustive search.",
                        elem_id="search_type"
                    )

                # noinspection PyTypeChecker
                with gr.Column(scale=0.5):
                    visualize_button = gr.Button("Visualize", elem_id="visualize_button")
                    display_mode = gr.Dropdown(
                        choices=["LiveView", "CompleteView"],
                        value="LiveView",
                        label="Choose between LiveView or CompleteView.",
                        # elem_id="search_type" #need to change this line
                    )

                # Custom View Input and Visualize Button in one row within a column
                with gr.Column(scale=2):
                    gr.Markdown("## Custom viewer")
                    gr.Markdown("### Here You can customizer your view format ")
                    custom_view_input = gr.Textbox(
                        placeholder="CUSTOM VIEW",
                        lines=5,
                        max_lines=10,
                        elem_id="custom_view_input",
                        autoscroll=True
                    )

            # Search Results Section
            gr.Markdown("## Search Results")
            gr.Markdown("Below are the repositories found based on your search.")
            with gr.Row():
                # Left Column - Repositories Found
                with gr.Column(scale=1):
                    gr.Markdown("### Repo's Found:")
                    repo_table = gr.Dataframe(headers=["Repository", "Description"], datatype="str", interactive=True)
                # Right Column - Selected Repo Info
                with gr.Column():
                    gr.Markdown("### Selected Repo Info")
                    with gr.Tabs():
                        with gr.TabItem("Content Relevance"):
                            gr.Markdown("Content Relevance Score:")
                            content_relevance_score = gr.Markdown("85%")
                        with gr.TabItem("Overview"):
                            overview_text = gr.Markdown("Overview of the selected repository.")
                        with gr.TabItem("Similarity Analysis"):
                            with gr.Accordion("Similarity Metrics"):
                                context_similarity = gr.Markdown("Context Similarity: 90%")
                                features_similarity = gr.Markdown("Features Similarity: 80%")
                                keyword_similarity = gr.Markdown("Keyword Similarity: 85%")
                                semantic_similarity = gr.Markdown("Semantic Similarity: 88%")
                                purpose_similarity = gr.Markdown("Purpose Similarity: 82%")
                                working_similarity = gr.Markdown("Working Similarity: 87%")
                                requirement_match_similarity = gr.Markdown("Requirement Match Similarity: 83%")
                        with gr.TabItem("More"):
                            repo_url = gr.Markdown("Repo URL: [Link](https://github.com/example/repo)")
                            fork_repo = gr.Markdown("Fork Repo: Yes")
                            star_repo = gr.Markdown("Star Repo: 150 Stars")
                            licensing_details = gr.Markdown("Licensing Details: MIT License")
            # Footer Section
            gr.Markdown("Visitors Count: 1234")
            gr.Markdown("---")
            gr.Markdown("© 2024 SEFGH-AI Project")
        with gr.TabItem("Documentation"):
            gr.Markdown("# Documentation")
            gr.Markdown("Documentation content goes here.")
        with gr.TabItem("About Us"):
            gr.Markdown("# About Us")
            gr.Markdown("About us content goes here.")

    # Callbacks and Interactions
    search_button.click(
        search_repos,
        inputs=[search_input, search_type],
        outputs=repo_table
    )

    repo_table.select(
        update_selected_repo,
        inputs=None,
        outputs=[
            content_relevance_score,
            overview_text,
            context_similarity,
            features_similarity,
            keyword_similarity,
            semantic_similarity,
            purpose_similarity,
            working_similarity,
            requirement_match_similarity,
            repo_url,
            fork_repo,
            star_repo,
            licensing_details
        ]
    )

    visualize_button.click(
        visualize_custom_view,
        inputs=custom_view_input,
        outputs=None
    )

demo.launch(show_api=False)
