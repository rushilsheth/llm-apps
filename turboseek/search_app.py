# app.py
# Main Gradio application that ties everything together

import gradio as gr
import time

from toy_apps.turboseek.brave_search import BraveSearchClient
from toy_apps.turboseek.together_client import TogetherLLMClient

# Initialize clients
brave_client = BraveSearchClient()
llm_client = TogetherLLMClient()

def search_and_respond(query):
    """
    Main function that handles the search process and LLM response generation
    
    Args:
        query (str): The user's search query
        
    Returns:
        tuple: (sources_html, llm_response)
    """
    if not query.strip():
        return "Please enter a search query.", ""
    
    # Step 1: Get sources from Brave Search
    sources = brave_client.get_sources(query)
    
    # Format sources for display
    sources_html = format_sources_html(sources)
    
    # Step 2: Generate LLM response using Together.ai
    llm_response = llm_client.generate_response(query, sources)
    
    return sources_html, llm_response

def format_sources_html(sources):
    """
    Format sources as HTML for display
    
    Args:
        sources (list): List of source dictionaries
        
    Returns:
        str: HTML representation of sources
    """
    html = "<h3>Sources:</h3>"
    
    for i, source in enumerate(sources, 1):
        html += f"""
        <div style="margin-bottom: 15px; padding: 10px; border: 1px solid #ddd; border-radius: 5px;">
            <h4>{i}. {source['title']}</h4>
            <a href="{source['url']}" target="_blank">{source['url']}</a>
            <p>{source['description']}</p>
        </div>
        """
    
    return html

# Create the Gradio interface
with gr.Blocks(css="""
    .container {
        max-width: 900px;
        margin: 0 auto;
        padding-top: 30px;
    }
    .heading {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 30px;
    }
    #search-box {
        border-radius: 25px;
        border: 1px solid #dfe1e5;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        padding: 10px 15px;
        font-size: 16px;
    }
    .search-container {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
    }
    .search-button {
        border-radius: 0 25px 25px 0;
        margin-left: -10px;
        height: 42px;
        width: 42px;
        padding: 0;
        font-size: 20px;
    }
    .results-container {
        margin-top: 20px;
    }
    .tab-content {
        padding: 15px;
        border: 1px solid #ddd;
        border-top: none;
        border-radius: 0 0 5px 5px;
    }
""") as demo:
    with gr.Column(elem_classes="container"):
        gr.HTML(
            """<div class="heading">Search smarter & faster</div>"""
        )
        
        with gr.Row(elem_classes="search-container"):
            input_text = gr.Textbox(
                placeholder="Ask anything",
                elem_id="search-box",
                show_label=False
            )
            search_button = gr.Button("→", elem_classes="search-button")
        
        with gr.Row(elem_classes="results-container"):
            with gr.Tabs() as tabs:
                with gr.TabItem("AI Answer"):
                    llm_response = gr.Markdown()
                with gr.TabItem("Sources"):
                    sources_output = gr.HTML()
        
        # Show a loading message during processing
        search_button.click(
            fn=lambda: ("Searching...", "Generating answer..."),
            outputs=[sources_output, llm_response],
            queue=False
        ).then(
            fn=search_and_respond,
            inputs=input_text,
            outputs=[sources_output, llm_response]
        )
        
        # Also trigger search when pressing Enter
        input_text.submit(
            fn=lambda: ("Searching...", "Generating answer..."),
            outputs=[sources_output, llm_response],
            queue=False
        ).then(
            fn=search_and_respond,
            inputs=input_text,
            outputs=[sources_output, llm_response]
        )

# Run the app
if __name__ == "__main__":
    demo.launch()