from mongo import Connection
import queue
from datetime import datetime
from writer import write_log

WORKERS = 6
ips = ["127.0.0.1", "127.0.0.2", "127.0.0.3", "127.0.0.4", "127.0.0.5"]

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


if __name__ == "__main__":
    write_log(f"=========== | {datetime.now():%Y-%m-%d %H:%M:%S} |  ===========\n");

    print_banner();

    q = queue.Queue()

    for j in range(WORKERS):
        worker = ConnectionWorker(q, j);
        worker.setDaemon(True)
        worker.start()

    for ip in ips:
        print(f"Enqueued ip: {ip}")
        q.put(ip)
   
    q.join()

    print("[(•̀ᴗ•́)و ̑̑\"] Done, now loot.")

