from typing import List
from mongo import ConnectionWorker, ConnectionWorkerOptions
from queue import Queue
import os
import argparse
from datetime import datetime
from writer import write_log

DEFAULT_WORKERS = 4
DEFAULT_OUT_DIR = "out"
DEFAULT_OUT_FILE = "loot.log"
DEFAULT_IPS = ["127.0.0.1"]

# Create argument parser
parser = argparse.ArgumentParser(prog="mongo-radar",
                                 description="Script to scan and do some operations over default unauthorized public \
                                 mongo databases.")

parser.add_argument("--out", dest="input_out", type=str, default=DEFAULT_OUT_DIR,
                    help="Define the ouput folder location.")

parser.add_argument("--ips", dest="input_ips", type=str,
                    help="Define list of ips or range of ips to scan. Ex: 127.0.0.1,127.0.0.2-255")

parser.add_argument("--workers", dest="input_workers", type=int,
                    help="Define the number of worker threads (> 4) that will be doing the jobs simultaneously.")

parser.add_argument("--dump", dest="input_dump", action="store_true",
                    help="Dumps all the databases found and saves it into out directory.")


# parser.add_argument("--kidnap", dest="input_account", type=str,
#                    help="Monero account to show in the ransom after kidnap the database (including local and admin).")

def print_banner():
    print("""

         ,-.                                                                       
        / \\  `.  __..-,O    88888b.d88b.  .d88b. 88888b.  .d88b.  .d88b.          
       :   \\ --''_..-'.'    888 "888 "88bd88""88b888 "88bd88P"88bd88""88b         
       |    . .-' `. '.     888  888  888888  888888  888888  888888  888          
       :     .     .`.'     888  888  888Y88..88P888  888Y88b 888Y88..88P          
        \\     `.  /  ..     888  888  888 "Y88P" 888  888 "Y88888 "Y88P"          
         \\      `.   ' .                                      888                 
          `,       `.   \\                       888      Y8b d88P                 
         ,|,`.        `-.\\                      888       "Y88P"                  
        '.||  ``-...__..-`                      888                                
         |  |               888d888 8888b.  .d88888 8888b.  888d888                
         |__|               888P"      "88bd88" 888    "88 b888P"                  
         /||\\               888    .d888888888  888.d88888 8888                   
        //||\\\\              888    888  888Y88b 888888  88 8888                  
       // || \\\\             888    "Y888888 "Y88888"Y88888 8888                  
    __//__||__\\\\__                                                               
   '--------------'                                                                

""")


def parse_min_max_range(range: str) -> (int, int):
    c = range.split("-")
    if len(c) > 1:
        return int(c[0]), int(c[1]) + 1
    else:
        return int(c[0]), int(c[0]) + 1


# Very naive ip range parsing
def parse_str_ips(ips_str: str) -> List[str]:
    ips = []
    raw_ips = ips_str.split(",")
    for raw_ip in raw_ips:
        oct = raw_ip.split(".")
        if len(oct) != 4:
            raise Exception("Malformed ip")

        f_min, f_max = parse_min_max_range(oct[0])
        for f in range(f_min, f_max):
            s_min, s_max = parse_min_max_range(oct[1])
            for s in range(s_min, s_max):
                t_min, t_max = parse_min_max_range(oct[2])
                for t in range(t_min, t_max):
                    fo_min, fo_max = parse_min_max_range(oct[3])
                    for fo in range(fo_min, fo_max):
                        ips.append(f"{f}.{s}.{t}.{fo}")
    return ips


if __name__ == "__main__":
    args = parser.parse_args()

    # Define workers
    workers = DEFAULT_WORKERS

    if args.input_workers is not None:
        workers = max(args.input_workers, DEFAULT_WORKERS)

    # Define ips
    ips = DEFAULT_IPS

    if args.input_ips is not None:
        ips = parse_str_ips(args.input_ips)

    options = ConnectionWorkerOptions(out=args.input_out, file=DEFAULT_OUT_FILE,
                                      dump=args.input_dump)

    print(options)

    # Create out dir if not exists
    if not os.path.exists(options.out):
        os.makedirs(options.out)

    write_log(f"{options.out}/{options.file}",
              f"=========== | {datetime.now():%Y-%m-%d %H:%M:%S} |  ===========\n")

    print_banner()

    q = Queue()

    for j in range(workers):
        worker = ConnectionWorker(q, j, options)
        worker.setDaemon(True)
        worker.start()

    for ip in ips:
        print(f"Enqueued ip: {ip}")
        q.put(ip)

    q.join()

    print("(•̀ᴗ•́)و ̑̑\" => Done, now loot.")
