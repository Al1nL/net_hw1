import socket
import select
import helper

HOST = "localhost"
PORT = 1337
def main():
    socks = []
    soc_to_msg = {}
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSock:
            serverSock.bind((HOST,PORT))
            socks.append(serverSock)
            serverSock.listen()
            print(f"Listening on {HOST}:{PORT}")

            while True:
                writable_socks = [s for s in socks if s is not serverSock and soc_to_msg.get(s, b"")]

                readable, writable, _ = select.select(socks, writable_socks,[])

                for sock in readable:
                    if sock is serverSock:
                        clientSock, addr = serverSock.accept()
                        print(f"New connection from {addr}")
                        socks.append(clientSock)
                        soc_to_msg[clientSock] = helper.string_to_binary("Welcome! Please log in.\n")

                for sock in writable:
                    msg = soc_to_msg.get(sock, b"")
                    if msg:
                        total = helper.sendall(sock, msg+b"\0")
                        if total == len(msg): #todo: else error
                            soc_to_msg[sock] = b""


    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()