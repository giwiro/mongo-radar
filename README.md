# :satellite: mongo-radar
```
         ,-.                                                                       
        / \  `.  __..-,O    88888b.d88b.  .d88b. 88888b.  .d88b.  .d88b.          
       :   \ --''_..-'.'    888 "888 "88bd88""88b888 "88bd88P"88bd88""88b         
       |    . .-' `. '.     888  888  888888  888888  888888  888888  888          
       :     .     .`.'     888  888  888Y88..88P888  888Y88b 888Y88..88P          
        \     `.  /  ..     888  888  888 "Y88P" 888  888 "Y88888 "Y88P"          
         \      `.   ' .                                      888                 
          `,       `.   \                       888      Y8b d88P                 
         ,|,`.        `-.\                      888       "Y88P"                  
        '.||  ``-...__..-`                      888                                
         |  |               888d888 8888b.  .d88888 8888b.  888d888                
         |__|               888P"      "88bd88" 888    "88 b888P"                  
         /||\               888    .d888888888  888.d88888 8888                   
        //||\\              888    888  888Y88b 888888  88 8888                  
       // || \\             888    "Y888888 "Y88888"Y88888 8888                  
    __//__||__\\__                                                               
   '--------------'                                                                
```
Multithread python3 script that scans and dumps mongo databases with default access (no password), 
through Tor sock4 proxy using proxychains and writes it into a log file.



[<img src="https://1.bp.blogspot.com/-rfPgrl8ikNE/VNx00l4Un9I/AAAAAAAAhzg/CR9GhLSl0_w/s728-e100/mongodb-database-hacking.jpg" width="350">](https://thehackernews.com/2015/02/mongodb-database-hacking.html)

There are tons of mongo databases without any type of authentication out there in the wild;
a lot of them [get hacked](https://docs.google.com/spreadsheets/d/1QonE9oeMOQHVh8heFIyeqrjfKEViL0poLnY8mAakKhM/edit#gid=1781677175),
that's why we should be really careful when configuring the Database.

Just **for research purposes** I developed an automated tool to discover and dump all the collections
in the discovered mongodb list. 
In order to stay anonymous we use [Tor](https://www.torproject.org/) service running as a SOCK4 proxy,
and [proxychains](http://proxychains.sourceforge.net/) to capture all tcp requests made by `mongo-radar`
and proxy them to the Tor SOCK4 port. 

## Usage

```
./mongo-radar [-h] [--out INPUT_OUT] [--ips INPUT_IPS]
                   [--workers INPUT_W] [--dump] [--kidnap INPUT_ACCOUNT]
                   
optional arguments:
  -h, --help            show this help message and exit
  --out INPUT_OUT       Define the ouput folder location.
  --ips INPUT_IPS       Define list of ips or range of ips to scan. Ex:
                        127.0.0.1,127.0.0.2-255
  --workers INPUT_WORKERS
                        Define the number of worker threads (> 4) that will be
                        doing the jobs simultaneously.
  --dump                Dumps all the databases found and saves it into out
                        directory.

```

## Legal Disclamer
```
The author does not hold any responsibility for the bad use of this tool,
remember that attacking targets without prior consent is illegal and punished by law.
```


## Requirements

- Tor sock4 proxy running on port 9050
- proxychains installed (binary `proxychains4` on path)
- python 3
- pipenv
- make
- mongodump (provided in the package `mongo-tools`)


## Install
Run the `install` goal
```
make install
```

## Run
First give execution privileges
```
chmod +x mongo-radar
```

Now just execute `./mongo-radar`.

