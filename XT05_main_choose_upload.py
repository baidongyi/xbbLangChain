import os

import gradio as gr
import torch

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from XT11_load_file import load_file
from XT31_call_API import chatGLM
from XT99_Tool import torch_gc

from XT13_search_file import get_search_data

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


def combine_data(data):
    torch_gc()
    result = " "
    for idx, line in enumerate(data):
        one_line = f"\n{idx + 1}.{line.page_content}"
        result += one_line
    return result


def get_file_path_by_module_name(module_name: str):
    if module_name == '合并':
        result = r"doc_database/hfm.docx"
    elif module_name == '运维':
        result = r"doc_database/mt.docx"
    elif module_name == '费用':
        result = r"doc_database/ex.docx"
    elif module_name == '资金':
        result = r"doc_database/bt.docx"
    elif module_name == '应收':
        result = r"doc_database/ar.docx"
    elif module_name == '资产':
        result = r"doc_database/fa.docx"
    elif module_name == '总账':
        result = r"doc_database/gl.docx"
    elif module_name == '应付':
        result = r"doc_database/ap.docx"
    elif module_name == '其他':
        result = r"doc_database/others.docx"
    else:
        result = r"doc_database/fssc.docx"
    return result


def query_by_file(question: str, file_path: str, history):
    print("query by file = " + file_path)

    data = combine_data(get_search_data(question, file_path))

    prompt = f"请基于以下资料，回答问题。如果不知道，则回答不知道，不要编造。\n下面是资料:{data}"
    prompt += f"\n下面是问题:\n{question}"

    print(f"prompt={prompt}")

    res = chatGLM(prompt, history=history)
    return res


def chat(prompt, history, choice):
    torch_gc()

    print(prompt)

    question = prompt['text']

    global MY_FILE

    if len(prompt['files']) > 0:
        MY_FILE = str(prompt['files'][0])

    if choice == '其他' and MY_FILE is not None:
        print("S1 query file = " + MY_FILE)

        MAX_SIZE_IN_MB = 4

        file_size = round(os.path.getsize(MY_FILE) / 1024 ** 2, 2)
        print(f"file size = {file_size}")
        if file_size <= MAX_SIZE_IN_MB:
            res = query_by_file(question, MY_FILE, history)
        else:
            res = f"上传的文件太大[{file_size}]M,超过限制{MAX_SIZE_IN_MB}M，无法处理"

    else:
        file_path = get_file_path_by_module_name(choice)

        if choice == '其他' or not os.path.exists(file_path):
            print(f"S2 query live choice = {choice}")
            res = chatGLM(question, history=history)
        else:
            print("S3 query file = " + file_path)
            res = query_by_file(question, file_path, history)

    return res


if __name__ == "__main__":
    choice_list = ["其他", "共享", "运维", "费用", "应付", "资金", "应收", "资产", "总账", "合并"]

    demo = gr.ChatInterface(chat, multimodal=True, additional_inputs=[
        gr.Dropdown(choice_list, value=choice_list[0], label="模块", info=" ")],
                            title="智能问答助手小白白", description="可以选择不同模块的知识库，进行查询和询问。")
    demo.launch(inbrowser=True, server_name="0.0.0.0", server_port=7860, show_error=True)
