import socket
import helper
import sys
from helper import Command
import select

HOST = "localhost"
PORT = 1337
def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSock:
            clientSock.connect((HOST, PORT))
            req ="welcome"
            res=login(clientSock)
            if res:
                while req!="quit":
                    req =  sys.stdin.readline()
                    if checkCommand(req,clientSock):
                        helper.sendall(clientSock,helper.string_to_binary(req))
                        answer = helper.recvall(clientSock)
                        print(helper.binary_to_string(answer))

    except socket.error as msg:
        print(msg)

def login(clientSock):
      err=False
      count=0
      while not err and count<=2 or answer =="Failed to login.":
        answer = helper.binary_to_string(helper.recvall(clientSock))
        print(answer)
        if answer.find("Hi")!=-1: return True

        count=1
        req = sys.stdin.readline()
        helper.sendall(clientSock, helper.string_to_binary(req))
        if b''==helper.recvall(clientSock):
            err=True
            return False
        count+=1
        req = sys.stdin.readline()
        helper.sendall(clientSock, helper.string_to_binary(req))
      return True

def checkCommand(cmd: str, sock):
    cmd = cmd.strip()  # remove leading/trailing spaces and newline

    # QUIT command
    if cmd == Command.QUIT.value:
        return True

    # Split into command and value
    if ":" in cmd:
        command, val = [s.strip() for s in cmd.split(":", 1)]
    else:
        print("Illegal command format, closing session")
        sock.close()
        return False

    # Match the command
    match command:
        case Command.LCM.value:
            # Expect two integers separated by space
            parts = val.split()
            if len(parts) != 2:
                print("Illegal LCM command, closing session")
                sock.close()
                return False
            try:
                x = int(parts[0])
                y = int(parts[1])
            except ValueError:
                print("LCM values must be integers, closing session")
                sock.close()
                return False

        case Command.CEASER.value:
            # Expect text and a number
            parts = val.split()
            if len(parts) != 2:
                print("Illegal CEASER command, closing session")
                sock.close()
                return False
            text, num_str = parts
            try:
                num = int(num_str)
            except ValueError:
                print("CEASER shift must be an integer, closing session")
                sock.close()
                return False

        case Command.PARENTHESIS.value:
            # Ensure val only contains '(' and ')'
            if not all(c in "()" for c in val):
                print("Illegal PARENTHESIS command, closing session")
                sock.close()
                return False
        case _:
            print("Unknown command, closing session")
            sock.close()
            return False

    # If we reached here, command is valid
    return True




if '__main__' == __name__:
    main()