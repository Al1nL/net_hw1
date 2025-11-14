def sendall(soc, data):
    total_sent = 0
    sent = 0

    while sent < len(data):
        sent = soc.send(data[total_sent:])
        if sent == 0:
            raise ConnectionError("Socket connection broken during send")
        total_sent = total_sent + sent

    return total_sent

def recvall(soc): # gets msg+\n
    total_recv = b""
    while b"\0" not in total_recv:
        data = soc.recv(1024)
        if not data:
            break
        total_recv += data
    # remove \0
    return total_recv.replace(b"\0", b"")

def string_to_binary(data):
    return data.encode('utf-8')

def binary_to_string(data):
    return data.decode('utf-8')