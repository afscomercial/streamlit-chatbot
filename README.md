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

## Manual deploy to Hugging Face Spaces (CLI)

If you'd rather push the repository yourself (skipping GitHub Actions):

```bash
# 1. Authenticate once (stores your token locally)
huggingface-cli login   # paste your HF_TOKEN when prompted

# 2. (First time only) create the Space as a Docker Space
huggingface-cli repo create afscomercial/streamlit-chatbot \
  --repo-type space --space-sdk docker -y  # change the name accordingly

# 3. Add the new remote and push
cd path/to/streamlit_chatbot

git lfs install                 # enables Large-File Storage just in case
git remote add hf \
  https://huggingface.co/spaces/afscomercial/streamlit-chatbot

git push hf main --force        # overwrite contents of the Space
```

After the push the Space will rebuild the Docker image and redeploy automatically.

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