import openai
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import copy
import re
import pandas as pd
import csv

deployment_name = "contract_search"
openai.api_type = "azure"
openai.api_key = "3a87ebf808cf4876b336ddbef5dd2528"
openai.api_base = "https://bpogenaiopenai.openai.azure.com/"
openai.api_version = "2023-05-15"




# Question Answer ChatBot
def documentChatBot(input_text, question='You are a Data Analyst. Can you please analyze the below data and generate insights'):
    prompt = (f"""{question}
    {input_text}
    """)

    response = openai.Completion.create(
        # engine="text-davinci-003",
        engine = deployment_name,
        prompt=prompt,
        max_tokens=300,
        n=1,
        stop=None,
        temperature=0.5,
    )
    document_chatbot = response.choices[0].text.strip()

    return {'document_chatbot': document_chatbot}

# Global ChatBot
def genericChatbot(question):
    messages=[{"role": "system", "content": question}]

    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )
    global_chatbot = response["choices"][0]["message"]["content"]

    return {'global_chatbot': global_chatbot}