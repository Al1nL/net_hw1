import socket
import select
import helper
import sys

HOST = "localhost"
PORT = 1337
def main():
    socks = []
    logged_in={}
    soc_to_msg = {}
    args=sys.argv[1:]
    users_db=users_to_db(args[0])
    port = PORT
    if len(args)==2:
        port=int(args[1])
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSock:
            serverSock.bind((HOST,port))
            socks.append(serverSock)
            serverSock.listen()
            print(f"Listening on {HOST}:{port}")

            while True:
                writable_socks = [s for s in socks if s is not serverSock and soc_to_msg.get(s, b"")]

                readable, writable, _ = select.select(socks, writable_socks,[])
                for sock in readable:
                    if sock is serverSock:
                        clientSock, addr = serverSock.accept()
                        print(f"New connection from {addr}")
                        socks.append(clientSock)
                        soc_to_msg[clientSock] = helper.string_to_binary("Welcome! Please log in.\n")
                    else:
                        req=helper.binary_to_string(helper.recvall(sock))
                        print(req)
                        if sock not in logged_in:
                            if req.find("User: ")!=-1:
                                logged_in[sock]=[req.split(":", 1)[1].strip()]

                            else:
                                close_conn(sock, logged_in, socks, soc_to_msg)

                        elif len(logged_in[sock])<2:
                            if req.find("Password: ")!=-1:
                                logged_in[sock].append(req.split(":", 1)[1].strip())
                                check=check_login(logged_in[sock],users_db)
                                if check:
                                    print("logged in")
                                    soc_to_msg[clientSock] = helper.string_to_binary(f"Hi {logged_in[sock][0]}, good to see you.\n")
                                else:
                                    del logged_in[sock]
                                    soc_to_msg[clientSock] = helper.string_to_binary("Failed to login.\n")
                            else:
                                close_conn(sock, logged_in, socks, soc_to_msg)



                for sock in writable:
                    msg = soc_to_msg.get(sock, b"")
                    print(msg)
                    if len(msg)>0:
                        total = helper.sendall(sock, msg)
                        if total == len(msg+b"\0"): #todo: else error
                            print("done")
                            soc_to_msg[sock] = b""


    except Exception as e:
        print(e)
def close_conn(sock,logged_in,socks,soc_to_msg): #todo
    pass
def check_login(params,db):
    return db[params[0]]==params[1]

def users_to_db(users):
    data = {}
    with open(users, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue  # skip empty lines
            key, value = line.split('\t')
            data[key] = value
    return data
if __name__ == '__main__':
    main()