import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os


@st.cache_resource(show_spinner=False)
def load_model():
    """Load the DialoGPT-small model and tokenizer once and cache them."""
    model_name = os.getenv("MODEL_REPO", "afscomercial/streamlit-chatbot-aviation")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return tokenizer, model


tokenizer, model = load_model()

# Initialise session state to keep track of the conversation
if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
if "chat_history_ids" not in st.session_state:
    st.session_state["chat_history_ids"] = None

st.title("🗨️ Simple LLM Chatbot")
st.write("Chat with an open-source language model powered by Hugging Face Transformers")

# Display the conversation so far
for i in range(len(st.session_state["generated"])):
    st.chat_message("user").markdown(st.session_state["past"][i])
    st.chat_message("assistant").markdown(st.session_state["generated"][i])

# Prompt for user input
user_input = st.chat_input("Type your message and press Enter…")

if user_input:
    # Add user message to history
    st.session_state["past"].append(user_input)

    # Encode the user input and append the EOS token
    new_user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt")

    # Append the new user input to the chat history (if it exists)
    if st.session_state["chat_history_ids"] is not None:
        bot_input_ids = torch.cat([st.session_state["chat_history_ids"], new_user_input_ids], dim=-1)
    else:
        bot_input_ids = new_user_input_ids

    # Generate a response
    st.spinner("Generating reply…")
    output_ids = model.generate(
        bot_input_ids,
        max_length=bot_input_ids.shape[-1] + 100,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        top_p=0.92,
        temperature=0.75,
    )

    # Extract the generated tokens excluding the input tokens
    response_ids = output_ids[:, bot_input_ids.shape[-1]:]
    response = tokenizer.decode(response_ids[0], skip_special_tokens=True)

    # Add the model's response to the chat history
    st.session_state["generated"].append(response)
    st.session_state["chat_history_ids"] = output_ids

    # Display the latest user & assistant messages immediately
    st.chat_message("user").markdown(user_input)
    st.chat_message("assistant").markdown(response) 