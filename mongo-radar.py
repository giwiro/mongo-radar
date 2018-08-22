from mongo import Connection
import queue
from datetime import datetime
from writer import write_log

WORKERS = 6
ips = ["127.0.0.1", "127.0.0.2", "127.0.0.3", "127.0.0.4", "127.0.0.5"]

if __name__ == "__main__":
    write_log(f"=========== | {datetime.now():%Y-%m-%d %H:%M:%S} |  ===========\n");

    q = queue.Queue()

    for j in range(WORKERS):
        worker = Connection(q, j);
        worker.setDaemon(True)
        worker.start()

    for ip in ips:
        print(f"Enqueued ip: {ip}")
        q.put(ip)
   
    q.join()

    print("[(•̀ᴗ•́)و ̑̑\"] Done, now loot.")

