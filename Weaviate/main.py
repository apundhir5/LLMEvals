import os
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=Open_API_KEY)
import time
load_dotenv()
Open_API_KEY = os.environ.get("OPENAI_API_KEY")

 
# Streamlit app title
st.title("Text Summarizer App")

# Input text box for user input
input_text = st.text_area("Enter the text you want to summarize:")

# Function to summarize the text using OpenAI API
def summarize_text(text):
    # Initialize progress bar
    progress_bar = st.progress(0)

    # Make API call to summarize the text
    response = client.completions.create(engine="text-davinci-002",
    prompt=f"Summarize the following text:\n{text}",
    max_tokens=50)

    # Show the progress bar incrementally
    for i in range(100):
        time.sleep(0.03)  # Simulate work being done
        progress_bar.progress(i + 1)

    # Display the summary
    return response.choices[0].text.strip()

if st.button("Summarize"):
    if input_text:
        st.subheader("Summary:")
        summary = summarize_text(input_text)
        st.write(summary)
    else:
        st.warning("Please enter some text to summarize.")
