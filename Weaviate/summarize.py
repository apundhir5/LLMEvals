import os
import streamlit as st
import pdfplumber 
import weaviate
import const
from openai import OpenAI

client = OpenAI(api_key=Open_API_KEY)
from dotenv import load_dotenv
from content_retreival import ContractSummaryRetriever

load_dotenv()
Open_API_KEY = os.environ.get("OPENAI_API_KEY")

weaviate_client = weaviate.Client(url=const.WEAVIATE_URL)

def clean_text(text):
    text = text.replace('\n', ' ').replace('\r', ' ')
    # Remove bullet
    # return re.sub(r'\w[.)]\s*', '', text).strip()
    return text.strip()

def summaryExists(fileName):
    wclient  = ContractSummaryRetriever(const.WEAVIATE_URL)
    contents = wclient.retrieve(fileName)
    if len(contents) > 0:
        return True, contents[0].passage
    else:
        return False, ""
    
def save_summary(filename, summaryDesc):
    with weaviate_client.batch as batch:
        batch.batch_size = 20
        page_object = {"filename": filename, 
                       "text": summaryDesc
                       }
        weaviate_client.batch.add_data_object(page_object, const.WEAVIATE_CONTRACT_SUMMARY_CLASS)

def save_page(weaviate_client, filename, pageContent, pageNumber):
    page_object = {"filename": filename,
                    "text": clean_text(pageContent),
                    "pagenumber": pageNumber
                    }
    weaviate_client.batch.add_data_object(page_object, const.WEAVIATE_CONTRACT_CLASS)

def import_file(feed):
    #check if file summary exists. If it does, used it. Else create summary and save it
    file_exists, summary = summaryExists(feed.name)
    if file_exists:
        return summary
    
    output_chunks = []
    file_added = False
    
    with pdfplumber.open(feed) as pdf:
        for page in pdf.pages:
            with weaviate_client.batch as batch:
                batch.batch_size = 20
                page_text = page.extract_text()

                if not file_added:
                    save_page(weaviate_client, feed.name, page_text, page.page_number)
                    file_added = True
                
                output_chunks.append(generate_summary(page_text))
    
    summary = " ".join(output_chunks)
    save_summary(feed.name, summary)
    return summary

def generate_summary(text):
    message_list = [
            {"role": "system", "content": "Summarize content you are provided."},
            {"role": "user", "content": text},
        ]
    response = client.chat.completions.create(model=const.MODEL4,
    messages=message_list,
    temperature=0,
    max_tokens=1024)
    return(response.choices[0].message.content.strip())

st.title("Summarize Document")

summary = ""
with st.sidebar:
    uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")
    if uploaded_file is not None:
        summary = import_file(uploaded_file)
        
st.markdown(summary)