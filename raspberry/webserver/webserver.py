import threading
import webserver.main as webserver

class Webserver(threading.Thread):
    ip_address = "127.0.0.1"

    def __init__(self, ip_address: str):
        threading.Thread.__init__(self)
        self.ip_address = ip_address

    def run(self):
        webserver.app.run(host=self.ip_address)

    def stop(self):
        self.join()
