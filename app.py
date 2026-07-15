import gradio as gr
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN", None)

def respond(message: str, history: list, model_id: str, system_prompt: str, max_tokens: int, temperature: float):
    if not model_id or not model_id.strip():
        return "Please enter a valid Hugging Face model ID (e.g. HuggingFaceH4/zephyr-7b-beta)"
    
    model_id = model_id.strip()
    
    try:
        client = InferenceClient(model=model_id, token=HF_TOKEN)
        
        # Build messages for chat models
        messages = []
        if system_prompt and system_prompt.strip():
            messages.append({"role": "system", "content": system_prompt.strip()})
        
        for user_msg, assistant_msg in history:
            if user_msg:
                messages.append({"role": "user", "content": user_msg})
            if assistant_msg:
                messages.append({"role": "assistant", "content": assistant_msg})
        
        messages.append({"role": "user", "content": message})
        
        # Try modern chat_completion first (works for most instruct/chat models)
        try:
            response = client.chat_completion(
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=0.95,
            )
            reply = response.choices[0].message.content.strip()
            return reply
        except Exception as chat_err:
            # Fallback to raw text_generation for older/base models
            # Format a simple prompt
            prompt_parts = []
            if system_prompt and system_prompt.strip():
                prompt_parts.append(system_prompt.strip())
            for user_msg, assistant_msg in history:
                if user_msg:
                    prompt_parts.append(f"User: {user_msg}")
                if assistant_msg:
                    prompt_parts.append(f"Assistant: {assistant_msg}")
            prompt_parts.append(f"User: {message}")
            prompt_parts.append("Assistant:")
            
            full_prompt = "\n".join(prompt_parts)
            
            response = client.text_generation(
                full_prompt,
                max_new_tokens=max_tokens,
                temperature=temperature,
                top_p=0.95,
                repetition_penalty=1.1,
            )
            reply = response.strip()
            # Clean up common artifacts
            if reply.lower().startswith("assistant:"):
                reply = reply[10:].strip()
            return reply
            
    except Exception as e:
        error_msg = str(e)
        if "model" in error_msg.lower() and "does not exist" in error_msg.lower():
            return f"Model '{model_id}' not found on Hugging Face. Check the exact model ID on huggingface.co"
        elif "Inference API" in error_msg or "not supported" in error_msg.lower() or "503" in error_msg:
            return (f"Model '{model_id}' does not support the free serverless Inference API yet, "
                    "is too large for free tier, or is temporarily unavailable. "
                    "Try smaller models like 'gpt2', 'distilgpt2', 'HuggingFaceH4/zephyr-7b-beta', or 'microsoft/Phi-3-mini-4k-instruct'. "
                    "For large models, deploy this app yourself with GPU hardware on HF Spaces or self-host with vLLM/Ollama.")
        else:
            return f"Error running model: {error_msg}\n\nTip: Make sure the model ID is correct and the model supports text-generation or chat on the Hugging Face Hub."

def user_message(user_message, history):
    if not user_message.strip():
        return "", history
    return "", history + [[user_message, None]]

def bot_message(history, model_id, system_prompt, max_tokens, temperature):
    if not history:
        return history
    # Get the last user message
    last_user_msg = history[-1][0]
    # Previous history (without the last pending assistant)
    prev_history = history[:-1] if len(history) > 1 else []
    
    reply = respond(last_user_msg, prev_history, model_id, system_prompt, max_tokens, temperature)
    history[-1][1] = reply
    return history

with gr.Blocks(title="FreeRunAI - Open Source Cloud AI", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # 🚀 FreeRunAI
        **Open source cloud-based AI — run any model from Hugging Face (GitHub models) for free**
        
        Paste any public Hugging Face model ID below and chat instantly. No GPU needed. Powered by Hugging Face's free serverless Inference API.
        """
    )
    
    with gr.Row():
        with gr.Column(scale=3):
            model_id = gr.Textbox(
                label="Hugging Face Model ID",
                value="HuggingFaceH4/zephyr-7b-beta",
                placeholder="e.g. meta-llama/Llama-3.2-1B-Instruct, Qwen/Qwen2-1.5B-Instruct, microsoft/Phi-3-mini-4k-instruct",
                info="Find models at huggingface.co/models. Most open source models from GitHub are available here."
            )
        with gr.Column(scale=1):
            max_tokens = gr.Slider(64, 1024, value=256, step=32, label="Max new tokens")
            temperature = gr.Slider(0.1, 1.5, value=0.7, step=0.1, label="Temperature (creativity)")
    
    system_prompt = gr.Textbox(
        label="System Prompt (optional)",
        placeholder="You are a helpful, friendly AI assistant.",
        value="You are a helpful, friendly AI assistant that answers questions accurately and concisely.",
        lines=2
    )
    
    chatbot = gr.Chatbot(
        label="Chat with the AI",
        height=450,
        show_copy_button=True,
        avatar_images=(None, "https://api.dicebear.com/7.x/bottts/svg?seed=FreeRunAI")
    )
    
    with gr.Row():
        msg = gr.Textbox(
            label="Your message",
            placeholder="Type your question here and press Enter...",
            scale=4
        )
        send_btn = gr.Button("Send", variant="primary", scale=1)
    
    with gr.Row():
        clear_btn = gr.Button("Clear Chat", variant="secondary")
        examples_btn = gr.Button("Load Example Models", variant="secondary")
    
    gr.Examples(
        examples=[
            ["HuggingFaceH4/zephyr-7b-beta", "Explain quantum computing in simple terms."],
            ["microsoft/Phi-3-mini-4k-instruct", "Write a short poem about Melbourne, Australia."],
            ["Qwen/Qwen2-1.5B-Instruct", "What are the benefits of open source AI?"],
            ["google/gemma-2-2b-it", "How do I deploy a Python app for free?"],
        ],
        inputs=[model_id, msg],
        label="Quick Examples (click to load)"
    )
    
    gr.Markdown(
        """
        ### How it works
        - Uses the **free** Hugging Face Inference API (serverless).
        - Models come from the Hugging Face Hub (vast majority of GitHub open source AI models are hosted here).
        - For **GitHub GGUF models** (TheBloke etc.): See the README for self-hosting instructions with llama-cpp-python.
        - Free tier has limits and works best with smaller models (<3B parameters recommended on CPU).
        
        **Deploy your own free cloud instance**: Duplicate this Space on Hugging Face (free) or deploy via the Dockerfile on Render/Railway.
        
        **Security**: Only use models from trusted sources. This app does not execute custom model code.
        """
    )
    
    # Wire up events
    msg.submit(
        user_message, 
        inputs=[msg, chatbot], 
        outputs=[msg, chatbot]
    ).then(
        bot_message, 
        inputs=[chatbot, model_id, system_prompt, max_tokens, temperature], 
        outputs=chatbot
    )
    
    send_btn.click(
        user_message, 
        inputs=[msg, chatbot], 
        outputs=[msg, chatbot]
    ).then(
        bot_message, 
        inputs=[chatbot, model_id, system_prompt, max_tokens, temperature], 
        outputs=chatbot
    )
    
    clear_btn.click(lambda: [], outputs=chatbot)
    
    def load_examples():
        return "HuggingFaceH4/zephyr-7b-beta"
    
    examples_btn.click(load_examples, outputs=model_id)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)