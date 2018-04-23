import abc

class ExecuterBase:
    __metaclass__ = abc.ABCMeta
    @abc.abstractmethod
    def execCode(self, translater, payload, delay):
        pass
    
    def to_hex(self, s):
        hex_payload = ""
        for x in s:
            a = hex(ord(x))[2:]
            if len(a) == 1:
                a = "0"+a
            hex_payload += a
        return hex_payload

    def hex_cmd(self, translater, payload, exec_cmd, delay):
        code = """
        Keyboard.print(F(" echo %(hex)s "));
        /*delay-lines*/delay(%(delay)s);
        %(exec)s
        /*delay-lines*/delay(%(delay)s);
        """ % { "hex": self.to_hex(payload), "exec": translater.translate(exec_cmd), "delay": delay }
        return code


class ExecuterDirect(ExecuterBase):
    def execCode(self, translater, payload, delay):
        return translater.translate(payload)

class ExecuterHexBash(ExecuterBase):
    def execCode(self, translater, payload, delay):
        ec = "|xxd -r -p|/bin/bash;exit;"
        return self.hex_cmd(translater, payload, ec, delay)

class ExecuterHexZsh(ExecuterBase):
    def execCode(self, translater, payload, delay):
        ec = "|xxd -r -p|/bin/zsh;exit;"
        return self.hex_cmd(translater, payload, ec, delay)
