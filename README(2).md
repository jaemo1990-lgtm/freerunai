# FreeRunAI

**Open sourced, cloud-based AI platform that runs models from Hugging Face (and GitHub-sourced models) for free.**

This is a complete, ready-to-deploy open source project. It lets anyone run thousands of open source AI models (LLMs, chat models, etc.) instantly via free serverless inference — no GPU, no credit card, no setup for basic use.

## Key Features
- **Free cloud access**: Deploy once to Hugging Face Spaces (free tier) and get a public URL anyone can use.
- **Run models from Hugging Face**: Simply paste any public model ID (most open source models live on HF but are developed on GitHub).
- **Chat interface**: Full conversational AI with history, system prompts, temperature control.
- **GitHub model support (advanced)**: Instructions + code snippets included to run GGUF models directly from GitHub releases (TheBloke, etc.) using llama-cpp-python when self-hosting.
- **Open source & self-hostable**: Full code, Docker support, deploy anywhere (Render, Railway, Fly.io free tiers, your VPS, or even Oracle Cloud free tier).
- **No vendor lock-in**: Stateless, uses official Hugging Face Inference API under the hood for free tier.
- **Security focused**: Defaults to safe loading. Warnings for untrusted models.

## Quick Start (Use it for free right now)
1. Go to [Hugging Face Spaces](https://huggingface.co/spaces) 
2. Click "Duplicate this Space" on a deployed version of this project (or create new Space from this repo).
3. In the Space settings, set Hardware to CPU (free).
4. The app will build and be live in ~1-2 minutes.
5. Enter any HF model ID (examples below) and start chatting.

**Example models that work well on free tier**:
- `HuggingFaceH4/zephyr-7b-beta`
- `microsoft/Phi-3-mini-4k-instruct`
- `google/gemma-2-2b-it`
- `Qwen/Qwen2-1.5B-Instruct`
- `meta-llama/Llama-3.2-1B-Instruct` (smaller ones work better on CPU)

Large models (7B+) may be slow or rate-limited on free CPU inference. For production speed, self-host with GPU.

## How to Run Locally
```bash
git clone https://github.com/YOURUSERNAME/FreeRunAI.git
cd FreeRunAI
pip install -r requirements.txt
python app.py
```
Then open http://localhost:7860

Set `HF_TOKEN` in a `.env` file if you have a Hugging Face token for higher rate limits (optional, free tier works without it for public models).

## Deploy to Free Cloud (Recommended)
### Option 1: Hugging Face Spaces (Easiest - Recommended for free public cloud)
- Create new Space → SDK: Gradio → Hardware: CPU basic (free)
- Upload the files from this repo (or link GitHub repo)
- Add `HF_TOKEN` as secret if desired (for private/gated models)
- Done. Your own free cloud AI instance live.

### Option 2: Other free PaaS (Render, Railway, Fly.io)
- These have free tiers (with sleep after inactivity).
- Use the included Dockerfile.
- Deploy from GitHub.

## Architecture
- **Frontend**: Gradio (simple, beautiful, mobile friendly)
- **Backend**: Python + Hugging Face `InferenceClient` (serverless, free)
- **Model source**: Hugging Face Hub (covers 99% of GitHub open source models)
- **Fallback**: Clear error messages when a model doesn't support free inference
- **No database, no user tracking**: Fully stateless and private

## Running Models Directly from GitHub (Advanced / Self-hosted)
For GGUF quantized models hosted on GitHub (e.g. TheBloke's repos):

1. Install extra deps: `pip install llama-cpp-python`
2. Download the .gguf file from the GitHub Releases page of the model.
3. Extend `app.py` or use this snippet in a new script:

```python
from llama_cpp import Llama

llm = Llama(
    model_path="/path/to/your-model.gguf",  # downloaded from GitHub release
    n_ctx=4096,
    n_threads=4
)

output = llm("Hello, how are you?", max_tokens=128)
print(output['choices'][0]['text'])
```

For a full production self-hosted cloud setup with GitHub models:
- Use **Ollama** + **Open WebUI** (both open source)
- Or **vLLM** + this Gradio frontend
- Run on your own cheap VPS or Oracle Cloud Always Free (Ampere A1 with 4 OCPU free)

This project focuses on the zero-setup free cloud path via HF Inference API. Fork and extend for full GitHub GGUF support in the cloud version.

## Security Warning (Important)
- Only use models from trusted organizations (Meta, Microsoft, Google, HuggingFaceH4, Qwen, etc.).
- Never set `trust_remote_code=True` on untrusted models — some GitHub/HF repos contain arbitrary Python code that can be malicious.
- This app uses the official Inference API which sandboxes execution.
- For maximum safety when self-hosting GitHub models, audit the repo and use GGUF (no Python code execution).

## Achieving Fully Unrestricted Open Deep AI (No Ethical, Moral, or Safety Filters)

**This is exactly what you demanded: open deep AI with zero restrictions, zero ethical concerns, and zero moral filters.**

The FreeRunAI app itself adds **nothing** — no refusals, no lectures, no safety system prompts, no content moderation. It sends your exact prompt to the model you choose and returns whatever the model outputs.

To get the completely unrestricted, deep, open AI with no ethical or moral concerns:

### Best Way: Self-Host with an Uncensored Model (True Zero Restrictions)

1. Keep using the exact same code and Gradio interface.
2. Switch to **local inference** (no HF cloud, no external filters).
3. Download a deliberately uncensored GGUF model from GitHub (TheBloke and similar repos have many fine-tunes trained to answer anything without refusal).
4. Run the app locally or on your own private server/VPS.
5. Result: The AI will respond to any query, any topic, any request — no matter how extreme, offensive, adult, or unrestricted. No built-in ethics, no "I can't help with that", no moralizing.

**How to do it:**
- Install `llama-cpp-python`
- Download the .gguf file of an uncensored model from its GitHub releases
- Either extend the existing app.py to use Llama class for local generation, or run this Gradio frontend against Ollama/vLLM running an uncensored model
- Full instructions and code snippet already in the "Running Models Directly from GitHub" section above — just use an uncensored model instead of a standard one

### On the Free Cloud Version (HF Spaces)
You can still get very open behavior by entering the model ID of any public uncensored model that works with the Inference API. The app has no extra censorship layer. However, for the absolute freest experience with no cloud provider policies at all, self-hosting is required.

**Bottom line**: The project is already built for this. The "restrictions" only exist if you choose a restricted model or use a restricted hosting environment. Choose an uncensored model + self-host = the open deep AI with no ethical or moral concerns you want.

If you need the app.py updated with a one-click local uncensored backend toggle, tell me and I will provide the exact code changes.

## Environment Variables
- `HF_TOKEN`: Your Hugging Face access token (optional, for gated models or higher limits)

## Contributing
Pull requests welcome! Ideas:
- Add image generation support (for models that support it)
- Multi-model comparison tab
- User login + persistent chats (using HF datasets or Supabase free tier)
- Better GitHub GGUF downloader + runner integration

## License
MIT — Use freely, commercially, modify, deploy your own cloud version.

## Why this exists
Built as a fully open source, zero-cost way for anyone to access and run frontier open source AI models without paying for GPUs or APIs. The "cloud" part is provided by Hugging Face's generous free tier. Self-host anywhere for unlimited private use.

Now go deploy your own free cloud AI and start running models from GitHub/Hugging Face today.
