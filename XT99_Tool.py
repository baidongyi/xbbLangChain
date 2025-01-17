import socket
import torch

def check_port_is_on(host, port, timeout=1):
    sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sck.settimeout(timeout)
    try:
        sck.connect((host, int(port)))
        sck.shutdown(socket.SHUT_RDWR)
        return True
    except:
        return False
    finally:
        sck.close()


def torch_gc():
    if torch.cuda.is_available():
        with torch.cuda.device(0):
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()

if __name__=='__main__':
    print(check_port_is_on("10.1.24.2",19980))