import socket
import helper

HOST = "localhost"
PORT = 1337
def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSock:
            clientSock.connect((HOST, PORT))
            welcome = helper.recvall(clientSock)
            print(helper.binary_to_string(welcome))

    except socket.error as msg:
        print(msg)

if '__main__' == __name__:
    main()