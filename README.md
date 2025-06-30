---
title: Streamlit Chatbot
emoji: "🗨️"
colorFrom: indigo
colorTo: purple
sdk: docker
app_file: app.py
pinned: false
---

# Streamlit Chatbot ✨

A lightweight chatbot built with [Streamlit](https://streamlit.io/) and the open-source `microsoft/DialoGPT-small` language model from [Hugging Face](https://huggingface.co/). This repository is ready to be deployed to [Hugging Face Spaces](https://huggingface.co/spaces) automatically through GitHub Actions.

## Features

* 📜 **Open-source LLM** – Uses a small conversational model that runs comfortably on the free GPU or CPU hardware offered by Spaces.
* 💬 **Chat interface** – Powered by Streamlit 1.30+ `st.chat_*` components.
* 🔄 **Persistent history** – Session-state keeps the discussion context on the client side.
* 🚀 **1-click deploy** – Push to the `main` branch and GitHub Actions mirrors the repository to your Space.

---

## Quick start (local)

```bash
# 1. Install dependencies
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Launch the app
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## Quick start (Docker)

If you prefer to run the chatbot in a container instead of a local virtual-env, use the provided `Dockerfile`.

```bash
# 1. Build the image (tagged "streamlit-chatbot")
docker build -t streamlit-chatbot .

# 2. Run the container and expose the app on http://localhost:8501
docker run --rm -it -e PORT=8501 -p 8501:8501 streamlit-chatbot
```

The container entrypoint launches Streamlit on the port given by the `PORT` environment variable (the same variable Hugging Face uses). By passing `-e PORT=8501` and mapping `-p 8501:8501`, you can access the interface in your browser at `http://localhost:8501`.

---

## Deploy to Hugging Face Spaces

1. **Create a new Space** (type: *Streamlit*) at `https://huggingface.co/new-space` or let the Action do it for you automatically.
2. **Generate a write token** in your Hugging Face account settings and add it to the repository secrets as `HF_TOKEN`.
3. Optionally add another secret called `SPACE_REPO` with the full name of the Space (e.g. `your-username/streamlit-chatbot`).

On each push to the `main` branch the GitHub workflow located at `.github/workflows/deploy-to-spaces.yml` will:

* Check out the code.
* Install the `huggingface_hub` CLI.
* Create the Space (if it doesn't exist).
* Force-push the contents of the repository to the Space, triggering a rebuild and redeploy.

---

## Repository layout

```
.
├── app.py                  # Streamlit application
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── config.toml         # UI & server settings
├── .github/
│   └── workflows/
│       └── deploy-to-spaces.yml  # CI/CD pipeline
├── Dockerfile              # Container definition for Docker/HF Spaces
└── README.md
```