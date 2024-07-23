import os
# import openai
from dotenv import load_dotenv
from langchain.llms import AzureOpenAI

load_dotenv()
Open_API_KEY = os.environ.get("OPENAI_API_KEY")
# openai.api_key = Open_API_KEY


# response = openai.Completion.create(
#     engine="text-davinci-002-prod",
#     prompt="This is a test",
#     max_tokens=5
# )

# os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_VERSION"] = "2023-05-15"
# os.environ["OPENAI_API_BASE"] = "..."
# os.environ["OPENAI_API_KEY"] = "..."


llm = AzureOpenAI(
    deployment_name="td2",
    model_name="text-davinci-002",
)

llm("Tell me a joke")
print(llm)