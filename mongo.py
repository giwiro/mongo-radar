import time
import threading
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError
from writer import write_log

class ConnectionWorker(threading.Thread):

    def __init__(self, queue, id):
        threading.Thread.__init__(self)
        self.queue = queue
        self.id = id

    def close(self, client):
        client.close()
    
    def test_open_connection(self, client, ip):
        try:
            info = client.server_info()
            version = info.get("version", "")
            dbs = client.database_names()
            self.log_opened_connection(ip, version, dbs)
        except ConnectionFailure:
            print(f"[{ip}]: connection failed")


    def log_opened_connection(self, ip, version, dbs):
        write_log(f"[{ip}]: opened connection.\n"
                f"\t├─ Version: {version}\n"
                f"\t└─ Databases: {dbs}\n")

    def run(self):
        while True:
            ip = self.queue.get()
            try:
                client = MongoClient(ip,
                                     serverSelectionTimeoutMS=3000)
                self.test_open_connection(client, ip)
                self.close(client)
                self.queue.task_done()
            except ConfigurationError:
                self.queue.task_done()


