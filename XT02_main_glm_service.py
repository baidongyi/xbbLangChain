import gradio as gr
import requests

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from XT11_load_file import load_file
from XT31_call_API import chatGLM


def get_search_data(question: str):
    text = load_file("files/doc1.txt")

    splitter = RecursiveCharacterTextSplitter(chunk_size=256, chunk_overlap=20)
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




def get_query_result(question: str):
    prompt = "请基于以下资料，回答问题。如果不知道，则回答不知道，不要编造。\n下面是资料:" + combine_data(get_search_data(question))
    prompt += f"\n下面是问题:\n{question}"

    print(f"prompt={prompt}")

    history = []
    res = chatGLM(prompt, history=history)

    return res


def chat(question: str, history):
    res = get_query_result(question)
    return res


if __name__ == '__main__':
    ui = gr.ChatInterface(chat, type="messages")
    ui.launch(inbrowser=True)
