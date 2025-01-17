import os.path
from zipfile import ZipFile

import gradio as gr


def chat(prompt, history, choice):

    return choice


if __name__ == "__main__":
    demo = gr.ChatInterface(chat, multimodal=True, additional_inputs=[gr.Dropdown(
            ["费用", "应付", "资金", "运维", "合并"], label="模块", info=" "
        )])
    demo.launch(inbrowser=True,server_name="0.0.0.0",server_port=7860,show_error=True)
