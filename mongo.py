from subprocess import Popen, check_call
from typing import NamedTuple, List
import threading
import os
import time
from queue import Queue
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError
from writer import write_log

DEFAULT_TIMEOUT = 10000


class ConnectionWorkerOptions(NamedTuple):
    out: str
    file: str
    dump: bool


class ConnectionWorker(threading.Thread):

    def __init__(self, queue: Queue, id: int,
                 options: ConnectionWorkerOptions):
        threading.Thread.__init__(self)
        self.queue = queue
        self.id = id
        self.options = options

    def close(self, client):
        client.close()

    def test_open_connection(self, client, ip: str) -> (List[str], str):
        try:
            info = client.server_info()
            version = info.get("version", "")
            dbs = client.database_names()
            return dbs, version
        except ConnectionFailure:
            print(f"[{ip}]: connection failed")
            return None, None

    def dump_databases(self, ip: str, dbs: List[str]) -> List[str]:
        base_ip_dir = f"{self.options.out}/{ip}"
        timestr = time.strftime("%Y-%m-%d-%H%M%S")
        dumped = []

        if dbs is None or len(dbs) == 0:
            return

        try:
            # Create ip dir if not exists
            if not os.path.exists(base_ip_dir):
                os.makedirs(base_ip_dir)
        except FileExistsError:
            print(f"[{ip}]: File exists error, check if you got the same ip in yer input")

        for db in dbs:
            cmd = f"mongodump --quiet --host {ip} -d {db} -o {base_ip_dir}/{db}-{timestr}"
            # why check_call instead os Popen ?
            # We want to wait until it exits, we don't wanna spawn a new sh
            # cos it complicates things up. check_call will wait until the command
            # finishes and gives back the return code
            retcall = check_call(cmd.split())
            if retcall == 0:
                dumped.append(db)

        return dumped

    def log_opened_connection(self, ip: str, version: str,
                              dbs: List[str], dumped_dbs: List[str]):
        dumped_str = ""
        if len(dumped_dbs) > 1:
            dumped_str = "\n".join([f"[{ip}]: Dumped '{d_db}'" for d_db in dumped_dbs]) + "\n"

        write_log(f"{self.options.out}/{self.options.file}",
                  f"------------------------------------------------\n"
                  f"[{ip}]: opened connection.\n"
                  f"\t├─ Version: {version}\n"
                  f"\t└─ Databases: {dbs}\n" +
                  dumped_str)

    def run(self):
        while True:
            ip = self.queue.get()
            print(f"[Worker {self.id}] => Started {ip}")
            try:
                client = MongoClient(ip, serverSelectionTimeoutMS=DEFAULT_TIMEOUT)
                dbs, version = self.test_open_connection(client, ip)
                if dbs is not None and version is not None:
                    dumped_dbs = []
                    if self.options.dump:
                        dumped_dbs = self.dump_databases(ip, dbs)

                    self.log_opened_connection(ip, version, dbs, dumped_dbs)
                self.close(client)
                self.queue.task_done()
            except ConfigurationError:
                self.queue.task_done()
