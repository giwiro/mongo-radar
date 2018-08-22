# mongo-radar
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
Extensible and multithread python3 script that scans provided ips, and looks for default mongodb unauthorized access, through Tor sock4 proxy using proxychains and writes it into a log file. 


## Requirements

- Tor sock4 proxy running on port 9050
- proxychains installed (binary `proxychains4` on path)
- python 3
- pipenv
- make
- mongodump

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

