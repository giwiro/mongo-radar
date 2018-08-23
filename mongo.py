from typing import NamedTuple, List
import threading
from queue import Queue
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError
from writer import write_log


class ConnectionWorkerOptions(NamedTuple):
    out: str
    file: str


class ConnectionWorker(threading.Thread):

    def __init__(self, queue: Queue, id: int,
                 options: ConnectionWorkerOptions):
        threading.Thread.__init__(self)
        self.queue = queue
        self.id = id
        self.options = options

    def close(self, client):
        client.close()

    def test_open_connection(self, client, ip: str):
        try:
            info = client.server_info()
            version = info.get("version", "")
            dbs = client.database_names()
            self.log_opened_connection(ip, version, dbs)
        except ConnectionFailure:
            print(f"[{ip}]: connection failed")

    def log_opened_connection(self, ip: str, version: str,
                              dbs: List[str]):
        write_log(f"{self.options.out}/{self.options.file}",
                  f"[{ip}]: opened connection.\n"
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
