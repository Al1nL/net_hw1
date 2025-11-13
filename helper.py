def sendall(soc, data):
    total_sent = 0
    sent = 0

    while sent < len(data):
        sent = soc.send(data[total_sent:])
        if sent == 0:
            break
        total_sent = total_sent + sent

    return total_sent

def recvall(soc):
    total_recv = b""
    while True:
        data = soc.recv(1024)
        if not data:
            break
        total_recv = total_recv + data
    return total_recv

def string_to_binary(data):
    return data.encode('utf-8')

def binary_to_string(data):
    return data.decode('utf-8')