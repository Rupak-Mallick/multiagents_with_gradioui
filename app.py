import gradio as gr
import tempfile
from langchain.chat_models import init_chat_model
from agents.research_agent import get_research_agent
from agents.math_agent import get_math_agent
from agents.supervisor_agent import get_supervisor
from utils.display import pretty_print_messages
from config import GROQ_API_KEY, TAVILY_API_KEY

# Initialize LLM with a correct model name
llm = init_chat_model(groq_api_key=GROQ_API_KEY, model="openai/gpt-oss-120b", model_provider="groq")

# Get agents and their tools
research_agent, research_tools = get_research_agent(llm, TAVILY_API_KEY)
math_agent, math_tools = get_math_agent(llm)

# Combine all tools
all_tools = research_tools + math_tools

# Supervisor
supervisor = get_supervisor(llm, research_agent, math_agent, all_tools)

def process_query(query, show_graph):
    """Process the user query using the multi-agent system"""
    try:
        query_input = {
            "messages": [
                {
                    "role": "user",
                    "content": query
                }
            ]
        }
        
        result_text = ""
        chunk = None  # Initialize chunk to None
        for chunk in supervisor.stream(query_input):
            result_text += f"Processing step:\n"
            result_text += pretty_print_messages(chunk, last_message=True, return_string=True)
            result_text += "\n" + "-"*50 + "\n"
        
        # Get the final result, checking if a chunk was returned
        final_message_history = chunk["supervisor"]["messages"] if chunk and "supervisor" in chunk and "messages" in chunk["supervisor"] else []
        final_result = final_message_history[-1].content if final_message_history else "No result found"
        
        # Graph visualization (if requested)
        graph_output = None
        if show_graph:
            try:
                graph_bytes = supervisor.get_graph().draw_mermaid_png()
                # Save the bytes to a temporary file
                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
                    temp_file.write(graph_bytes)
                    graph_output = temp_file.name
            except Exception as e:
                graph_output = None
                result_text += f"\nNote: Could not generate graph visualization - {e}"
        
        # Return all three outputs as required by Gradio
        return result_text, final_result, graph_output
        
    except Exception as e:
        error_msg = f"Error processing query: {str(e)}"
        # Return error messages for the textboxes and None for the image
        return error_msg, error_msg, None

# Create Gradio interface
with gr.Blocks(title="Multi-Agent AI System", css="static/style.css") as demo:
    gr.Markdown("# Multi-Agent AI System")
    gr.Markdown("This system uses specialized agents for research and math tasks, coordinated by a supervisor.")
    
    with gr.Row():
        with gr.Column():
            query_input = gr.Textbox(
                label="Enter your query",
                placeholder="e.g., find US and New York state GDP in 2024. what % of US GDP was New York state?",
                lines=3
            )
            show_graph = gr.Checkbox(label="Show agent workflow graph", value=True)
            submit_btn = gr.Button("Process Query", variant="primary")
        
        with gr.Column():
            final_output = gr.Textbox(label="Final Result", lines=5)
            graph_output = gr.Image(label="Agent Workflow Graph", visible=True)
    
    with gr.Row():
        process_details = gr.Textbox(label="Processing Details", lines=15, max_lines=20)
    
    # Set up event handlers
    submit_btn.click(
        fn=process_query,
        inputs=[query_input, show_graph],
        outputs=[process_details, final_output, graph_output]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)