import pathlib
from langchain_community.document_loaders import TextLoader, Docx2txtLoader, PyPDFLoader, UnstructuredExcelLoader

def load_file_to_document_for_txt(file_path: str):
    loader = TextLoader(file_path)
    loader.encoding = "utf-8"
    return loader.load()

def load_file_to_document_for_pdf(file_path: str):
    loader = PyPDFLoader(file_path)
    return loader.load()

def load_file_to_document_for_doc(file_path: str):
    loader = Docx2txtLoader(file_path)
    return loader.load()


def load_file(file_path:str):
    file_extension = pathlib.Path(file_path).suffix
    doc_result = None

    if file_extension == '.txt':
        doc_result =  load_file_to_document_for_txt(file_path)
    elif file_extension == '.pdf':
        doc_result =  load_file_to_document_for_pdf(file_path)
    elif file_extension == '.docx':
        doc_result =  load_file_to_document_for_doc(file_path)

    return doc_result

if __name__ == '__main__':
    doc = load_file("files/doc5.xlsx")
    print(doc)
