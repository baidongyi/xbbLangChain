
import os

import torch

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from XT11_load_file import load_file
from XT99_Tool import torch_gc

DEVICE = "cuda"
DEVICE_ID = "0"
CUDA_DEVICE = f"{DEVICE}:{DEVICE_ID}" if DEVICE_ID else DEVICE

MY_FILE = None


def torch_gc():
    if torch.cuda.is_available():
        with torch.cuda.device(CUDA_DEVICE):
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()
            torch.cuda.reset_peak_memory_stats()


def get_search_data(question: str, file_path: str):
    text = load_file(file_path)

    splitter = RecursiveCharacterTextSplitter(chunk_size=128, chunk_overlap=5)
    documents = splitter.split_text(text[0].page_content)

    emb_model_path = r"C:\Users\baido\OneDrive\Work\AI\GDH\xbbLangChainChatGLM\bge"

    if not os.path.exists(emb_model_path):
        emb_model_path = r"C:\Users\administrator\xxtony\xbbLangChainChatGLM\bge"

    emb_model = HuggingFaceEmbeddings(model_name=emb_model_path)
    vector_db = FAISS.from_texts(texts=documents, embedding=emb_model)

    data = vector_db.similarity_search(question, include_metadata=True, k=3)

    del emb_model
    torch_gc()

    return data