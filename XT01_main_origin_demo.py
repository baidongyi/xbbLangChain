import gradio as gr


from langchain_community.llms.chatglm import ChatGLM
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter


from XT11_load_file import load_file

def get_query_result(question: str):

    text = load_file("files/doc1.txt")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    documents = splitter.split_text(text[0].page_content)

    emb_model_path = r"C:\Users\baido\OneDrive\Work\AI\xbbLangChainChatGLM\bge"
    if not os.path.exists(emb_model_path):
        emb_model_path = r"C:\Users\baido\OneDrive\Work\AI\xbbLangChainChatGLM\bge"


    emb_model = HuggingFaceEmbeddings(model_name=emb_model_path)
    vector_db = FAISS.from_texts(texts=documents, embedding=emb_model)
    retriever = vector_db.as_retriever()

    qa_chain = RetrievalQA.from_chain_type(llm=ChatGLM(), chain_type="stuff", retriever=retriever)
    rs = qa_chain.run(question)

    return str(rs)

def run_query(question:str):
    return get_query_result(question)

def chat(question:str, history):
    res = get_query_result(question)
    return res

if __name__ == '__main__':
    ui = gr.ChatInterface(chat)
    ui.launch(inbrowser=True)

