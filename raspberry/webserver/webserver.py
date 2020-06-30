import threading
import webserver.main as webserver

class Webserver(threading.Thread):
    ip_address = "0.0.0.0"
    webserver = None

    def __init__(self, ip_address: str):
        threading.Thread.__init__(self)
        self.ip_address = ip_address
        self.webserver = webserver

    def run(self):
        self.webserver.app.run(host=self.ip_address)

    def stop(self):
        self.join()
