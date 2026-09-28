import streamlit as st
import requests

# Page Configuration
st.set_page_config(page_title="AI Agent Chat Portal", page_icon="🤖", layout="centered")

st.title("🤖 Venkata Krishna Prasad Kurella's AI Agent Portal")
st.write("Communicate directly with your FastAPI backend and autonomous agent.")

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior chat messages from history when app redraws
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input via chat box at the bottom
if prompt := st.chat_input("Ask your agent to perform a task (e.g., Run a security check)..."):
    # Add user message to state and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Send the goal to your FastAPI backend endpoint
    with st.chat_message("assistant"):
        with st.spinner("Agent is reasoning and executing tools..."):
            try:
                # Make POST request to your FastAPI server running on port 8000
                response = requests.post(
                    "http://127.0.0.1:8000/run-agent",
                    json={"goal": prompt}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    agent_output = data.get("output", "No response returned.")
                    st.markdown(agent_output)
                    # Save assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": agent_output})
                else:
                    error_msg = f"Server Error ({response.status_code}): {response.text}"
                    st.error(error_msg)
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the FastAPI backend. Make sure your server is running on port 8000!")