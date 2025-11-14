import socket
import helper
import sys

HOST = "localhost"
PORT = 1337
def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSock:
            clientSock.connect((HOST, PORT))
            req ="welcome"
            answer = helper.recvall(clientSock)
            print(helper.binary_to_string(answer))
            while req!="Password: simplepass\n":
                print("enter req")
                req =  sys.stdin.readline()
                print(req)
                helper.sendall(clientSock,helper.string_to_binary(req))
                print("sent")
            answer = helper.recvall(clientSock)
            print(helper.binary_to_string(answer))
    except socket.error as msg:
        print(msg)

if '__main__' == __name__:
    main()