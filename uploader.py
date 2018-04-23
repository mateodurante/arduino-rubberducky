import os, subprocess, sys
import serial.tools.list_ports
import serial
import string
import argparse
from config import arduino_bin
from payloads import LINUX_PAYLOADS, WINDOWS_PAYLOADS, ALL_PAYLOADS, OPEN_TERMINAL_METHODS, KEY_RETURN, CLOSE_TERMINAL_METHODS, PREDEFINED_COMPILERS
import translater
import executer

class Uploader:
    translater = translater.TranslaterDummy()
    predefinedCompiler = None
    compiler = None
    vendorToSearch = "HoodLoader2"
    executer = None
    payloadName = None
    payload = None
    delayInitial = 1000
    delayLines = 300
    delayTerminal = 1000
    delayPayload = 1000
    delayLoop = 1000
    otm = None
    ctm = None
    inoPayload = None
    inoCodeBlock = None
    inoFinalCode = None
    arduinoPort = None

### STATIC ###
    @staticmethod
    def getAllPayloadNames():
        return ALL_PAYLOADS.keys()
    @staticmethod
    def getLinuxPayloadNames():
        return LINUX_PAYLOADS.keys()
    @staticmethod
    def getWindowsPayloadNames():
        return WINDOWS_PAYLOADS.keys()
    @staticmethod
    def getAllOpenTerminalMethods():
        return OPEN_TERMINAL_METHODS.keys()
    @staticmethod
    def getAllCloseTerminalMethods():
        return CLOSE_TERMINAL_METHODS.keys()
    @staticmethod
    def getAllPredefinedCompilers():
        return PREDEFINED_COMPILERS.keys()


### GETTERS ###
    def getPayload(self):
        if self.payload:
            return self.payload
        raise Exception("Payload is not set")
    def getInoPayload(self):
        if self.inoPayload != None:
            return self.inoPayload
        else:
            raise Exception("Ino Payload is not set")
    def getOpenTerminalMethod(self):
        if self.otm:
            return self.otm
        raise Exception("Open Terminal Method is not set")
    def getCloseTerminalMethod(self):
        if self.ctm:
            return self.ctm
        raise Exception("Close Terminal Method is not set")
    def getArduinoPort(self):
        if self.arduinoPort:
            return self.arduinoPort
        raise Exception("Arduino Port is not set")


### SETTERS ###
    def setTranslaterDummy(self):
        self.translater = translater.TranslaterDummy()
    def setTranslaterEnglish(self):
        self.translater = translater.TranslaterEnglish()
    def setTranslaterUnicode(self):
        self.translater = translater.TranslaterUnicode()
    def setTranslaterSpanish(self):
        self.translater = translater.TranslaterSpanish()
    def setTranslaterWindows(self):
        self.translater = translater.TranslaterWindows()
        
    def setExecuterDirect(self):
        self.executer = executer.ExecuterDirect()
    def setExecuterHexBash(self):
        self.executer = executer.ExecuterHexBash()
    def setExecuterHexZsh(self):
        self.executer = executer.ExecuterHexZsh()

    def setDelayLines(self, n):
        self.delayLines = n
    def setDelayTerminal(self, n):
        self.delayTerminal = n
    def setDelayPayload(self, n):
        self.delayPayload = n
    def setDelayInitial(self, n):
        self.delayInitial = n
    def setDelayLoop(self, n):
        self.delayLoop = n

    def setPayloadName(self, payloadName):
        if payloadName in self.getAllPayloadNames():
            self.payloadName = payloadName
            self.payload = ALL_PAYLOADS[payloadName]
        else:
            raise Exception("Payload name does not exists")
    
    def setOpenTerminalMethod(self, otm):
        if otm in self.getAllOpenTerminalMethods():
            self.otm = OPEN_TERMINAL_METHODS[otm]
        else:
            raise Exception("OpenTerminalMethod does not exists")
    
    def setCloseTerminalMethod(self, ctm):
        if ctm in self.getAllCloseTerminalMethods():
            self.ctm = CLOSE_TERMINAL_METHODS[ctm]
        else:
            raise Exception("CloseTerminalMethod does not exists")

    def setPredefinedCompiler(self, compilerKey):
        if compilerKey in self.getAllPredefinedCompilers():
            self.predefinedCompiler = compilerKey
            self.compiler = PREDEFINED_COMPILERS[compilerKey]
        else:
            raise Exception("Predefined Compiler name/key does not exists")

    def setCustomCompiler(self, compiler):
        self.compiler = compiler
    
    def setCustomPayload(self, payload):
        self.payload = payload
    
    def setVendorToSearch(self, vendor):
        self.vendorToSearch = vendor

    def setArduinoPortByBoard(self, search):
        self.arduinoPort = self.searchPortByBoard(search)
        if not self.arduinoPort:
            raise Exception("Board name not found in serial ports.")

    def setArduinoPort(self, port):
        self.arduinoPort = port



### LOGIC ###

    def _generateInoPayload(self):
        self.inoPayload = self.executer.execCode(self.translater, self.getPayload(), self.delayLines)

    def _generateInoCodeBlock(self):
        self.inoCodeBlock = self._generateCodeBlock()

    def generateInoFinalCode(self):
        self._generateInoPayload()
        self._generateInoCodeBlock()
        self.inoFinalCode = self._generateProgram()
        return self.inoFinalCode


    def searchPortByBoard(self, search):
        clients = []
        ports = serial.tools.list_ports.comports()
        #print(ports)
        arduino_port = None
        for p in ports:
            print (p)
            if search in p[1]:
                #print ("This is a HoodLoader!")
                #print (p)
                arduino_port = p[0]
        #if arduino_port == "":
            #print ("{0} not found".format(search))
            #sys.exit("where is it?")
        return arduino_port

    def _runUpload(self, code_ino, verbose, parameters=[]):
        #https://github.com/arduino/Arduino/blob/master/build/shared/manpage.adoc
        cwd = os.path.dirname(__file__)
        ino_file = cwd + '/temp_upload.ino'
        #ino_file = "temp_upload.ino"
        with open(ino_file, 'w') as f:
            f.write(code_ino)
        command = [arduino_bin, ino_file]
        if verbose:
            command += ['--verbose']
        if self.compiler:
            command += ['--board', self.compiler]
        command += parameters
        print(command)
        subprocess.call(command)
        

    def uploadCode(self, code_ino, verbose=False):
        commands = ['--upload', '--port', self.getArduinoPort()]
        self._runUpload(code_ino, verbose, parameters=commands)
    
    def verifyCode(self, code_ino, verbose=True):
        commands = ['--verify']
        self._runUpload(code_ino, verbose, parameters=commands)

    def exec_payload_to_en(self, exec_payload):
        return "Keyboard.print(F(\" " + exec_payload + " \"));"

    #def exec_payload_to_es(exec_payload):
    #    return translate(exec_payload)

    def _generateProgram(self):
        header = """
        #include "Keyboard.h"
        //#include "HID.h"

        void setup() {
        Keyboard.begin(); /*delay-initial*/delay(%s);
        """
        footer = """
        }
        void loop(){ delay(%s); }
        """
        header = header % (self.delayInitial)
        body = self.inoCodeBlock
        footer = footer % (self.delayLoop) 

        return  "{0}{1}{2}".format(header, body, footer)

    def _generateCodeBlock(self):
        params = {
            'open': self.getOpenTerminalMethod(),
            'terminal_delay': self.delayTerminal,
            'payload_delay': self.delayPayload,
            'payload': self.getInoPayload(),
            'enter': KEY_RETURN,
            'exit': self.getCloseTerminalMethod()
        }

        arduino_code = """
        /*********** OPEN TERMINAL **************/
        %(open)s
        /*delay-terminal*/delay(%(terminal_delay)s);

        /*********** PAYLOAD **************/
        %(payload)s
        /*delay-payload*/delay(%(payload_delay)s);

        /*********** ENTER **************/
        %(enter)s
        /*delay-payload*/delay(%(payload_delay)s);

        /*********** EXIT TERMINAL **************/
        %(exit)s
        """

        return arduino_code % params

    #    /*********** KEYBOARD DISTRIBUTION: execute (xxd bash & [exit]) **************/ 
    #    %(exec)s
    #    delay(500);
