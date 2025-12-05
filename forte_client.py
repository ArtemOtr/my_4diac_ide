import socket
import time

class ForteClient:
    def __init__(self, host="127.0.0.1", port=61499):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.sock.settimeout(2.0)   # даём время на ответ
        print("[IDE] Connected to forte")

    def send_cmd(self, cmd):
        # обязательно \n — FORTE без этого не обрабатывает команду
        message = (cmd + "\n").encode()
        self.sock.sendall(message)

        # важно: дать FORTE время обработать команду
        time.sleep(0.05)

        # читаем ответ, если он есть
        try:
            data = self.sock.recv(4096)
            if data:
                resp = data.decode(errors='ignore').strip()
                print("[FORTE]", resp)
                return resp
            else:
                print("[FORTE] (empty response)")
                return None

        except socket.timeout:
            print("[FORTE] (no response)")
            return None

    def close(self):
        if self.sock:
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
            except:
                pass
            self.sock.close()
            print("[IDE] Connection closed")
            self.sock = None
