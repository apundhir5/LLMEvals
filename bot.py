import os
import streamlit as st
import const
from openai import OpenAI

client = OpenAI(api_key=Open_API_KEY)
from dotenv import load_dotenv
from content_retreival import ContractRetriever, ContractSummaryRetriever
from streamlit_feedback import streamlit_feedback

load_dotenv()
Open_API_KEY = os.environ.get("OPENAI_API_KEY")


def clean_text(text):
    text = text.replace('\n', ' ').replace('\r', ' ')
    # Remove bullet
    # return re.sub(r'\w[.)]\s*', '', text).strip()
    return text.strip()

def make_prompt(context: str):
    prompt = (
            "You are an expert in reviewing Contracts.\n"
            "Answer the following question using the provided context.\n"
            "Do not include any information in your response that is not in the provided context but you can answer questions from your training.\n"
            "Do not mention the existence of the context to the user.\n"
            "Keep your answer concise and be precise with numbers; Use 3 sentences at most.\n"
            "Context-\n"
            f"{context}\n"
        )
    return prompt

def getDocumentContext(query: str) -> str:
    wclient  = ContractRetriever(const.WEAVIATE_URL)
    contents = wclient.retrieve(query)
    if len(contents) > 0:
        return contents[0].passage

def getDocumentSummary(fileName):
    wclient  = ContractSummaryRetriever(const.WEAVIATE_URL)
    contents = wclient.retrieve(fileName)
    if len(contents) > 0:
        return contents[0].passage
    
def get_assistant_prompt(query: str, searchSummary: bool) -> str:
    assistant_prompt = make_prompt(getDocumentContext(query))

    if searchSummary:
        #If using Summary append it to the context
        summary = getDocumentSummary(query)
        assistant_prompt = f"{assistant_prompt} \n {summary}"
    
    return assistant_prompt

def get_answer(query: str, temperature=0.7, max_tokens=256, top_p=0.9, n=2, stop=None, frequency_penalty=0.9, presence_penalty=0.9, searchSummary=False): # -> str:
    # return 10, "Test response"

    message_list = [{"role": "assistant", "content": get_assistant_prompt(query, searchSummary)}]

    if "messages" in st.session_state:
        for m in st.session_state.messages:
            message_list.append({"role": m["role"], "content": m["content"]})
    
    response = client.chat.completions.create(model=const.MODEL4,
    messages=message_list,
    max_tokens=max_tokens,
    temperature=temperature,
    top_p=top_p,
    # stop=stop,
    presence_penalty=presence_penalty,
    frequency_penalty=frequency_penalty)
    
    answer = response.choices[0].message.content
    tokens = response.usage.total_tokens
    
    return tokens, answer


st.title("Chat with your data!")

st.sidebar.markdown("# Model Parameters")
with st.sidebar:
    temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
    max_tokens = st.sidebar.number_input("Max Tokens", 50, 1024, 256, step=48)
    top_p = st.sidebar.slider("Top P", 0.1, 1.0, 0.9, 0.1)
    n = st.sidebar.number_input("N", 1, 5, 2, step=1)
    # stop = st.sidebar.text_input("Stop", "")
    frequency_penalty = st.sidebar.slider("Frequency Penalty", 0.0, 1.0, 0.9, 0.1)
    presence_penalty = st.sidebar.slider("Presence Penalty", 0.0, 1.0, 0.9, 0.1)
    # usepii = st.radio("Use PII?", ["Yes", "No"], horizontal=True)
    searchSummary = st.radio("Search Summary", ["Yes", "No"], horizontal=True)
    if st.button("Reset"):
        for key in st.session_state.keys():
            del st.session_state[key]
    

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me about Contracts.."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        tokens, response = get_answer(query=prompt, 
                                      temperature=temperature, 
                                      max_tokens=max_tokens, 
                                      top_p=top_p, 
                                      n=n, 
                                      frequency_penalty=frequency_penalty, 
                                      presence_penalty = presence_penalty, 
                                      searchSummary=(searchSummary=="Yes"))
        message_placeholder.markdown(response)
        

    # col1,col2,col3,col4 = st.columns([3,3,0.5,0.5])
    # with col1:
    #     st.write(f"Total Tokens: {tokens}")
    # with col3:
    #     if st.button(":thumbsup:"):
    #         print("Like")
    # with col4:
    #     if st.button(":thumbsdown:"):
    #         print("Dislike")
        
    st.session_state.messages.append({"role": "assistant", "content": response})
    
feedback = streamlit_feedback(
    feedback_type="thumbs"
)
if feedback != None:
    print(feedback.get('score'))

