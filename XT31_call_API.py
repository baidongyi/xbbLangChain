
import requests



def get_url():
    return r"http://10.1.24.2:19980/glm/"


def chatGLM(prompt, history):
    resp = requests.post(
        url=get_url(),
        json={"prompt": prompt, "history": history},
        headers={"Content-Type": "application/json;charset=utf-8"}
    )
    return resp.json()['response'], resp.json()['history']

if __name__ == '__main__':
    history = []
    question = "hi"
    response, history = chatGLM(question, history)
    print('Answer:', response)
