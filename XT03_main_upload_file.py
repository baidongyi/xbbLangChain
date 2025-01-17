import os

import gradio as gr

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from XT11_load_file import load_file
from XT31_call_API import chatGLM

MY_FILE = None

def get_search_data(question: str, file_path: str):
    text = load_file(file_path)

    splitter = RecursiveCharacterTextSplitter(chunk_size=256, chunk_overlap=40)
    documents = splitter.split_text(text[0].page_content)

    emb_model_path = r"C:\Users\baido\OneDrive\Work\AI\xbbLangChainChatGLM\bge"

    if not os.path.exists(emb_model_path):
        emb_model_path = r"C:\Users\baido\OneDrive\Work\AI\xbbLangChainChatGLM\bge"

    emb_model = HuggingFaceEmbeddings(model_name=emb_model_path)
    vector_db = FAISS.from_texts(texts=documents, embedding=emb_model)

    data = vector_db.similarity_search(question, include_metadata=True, k=5)

    return data


def combine_data(data):
    result = " "
    for idx, line in enumerate(data):
        one_line = f"\n{idx + 1}.{line.page_content}"
        result += one_line
    return result


def query_by_file(question: str, file_path: str, history):
    print("query by file = " + file_path)

    data = combine_data(get_search_data(question, file_path))

    prompt = f"请基于以下资料，回答问题。如果不知道，则回答不知道，不要编造。\n下面是资料:{data}"
    prompt += f"\n下面是问题:\n{question}"

    print(f"prompt={prompt}")

    res = chatGLM(prompt, history=history)
    return res


def chat(prompt: str, history):
    print(prompt)
    question = prompt['text']

    global MY_FILE

    if len(prompt['files']) > 0:
        MY_FILE = prompt['files'][0]
        res = query_by_file(question, MY_FILE)
    elif MY_FILE is not None:
        res = query_by_file(question, MY_FILE)
    else:
        res = chatGLM(question, history=history)

    return res


if __name__ == '__main__':
    MY_FILE = None
    ui = gr.ChatInterface(chat, type="messages", multimodal=True)
    ui.launch(server_name="0.0.0.0", server_port=7860, inbrowser=True)
