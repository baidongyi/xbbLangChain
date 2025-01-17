import os.path
from zipfile import ZipFile

import gradio as gr


def chat(prompt, history):
    print(prompt)
    file_path = prompt['files'][0]
    msg = prompt['text']
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            f.close()
        return "识别到文件，内容为[" + lines[0] +f"]\n指令为[{msg}]"


if __name__ == "__main__":
    demo = gr.ChatInterface(chat, multimodal=True)
    demo.launch(inbrowser=True)
