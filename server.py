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


def is_balanced_parentheses(data):
    count_open = 0
    for char in data:
        if char == '(':
            count_open += 1
        elif char == ')':
            count_open -= 1
            if count_open < 0:
                return 'the parentheses are balanced: no'

    if count_open == 0:
        return 'the parentheses are balanced: yes'

    return 'the parentheses are balanced: no'

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return abs(a)
def lcm(X, Y):
    return 'the lcm is: ' + abs(X * Y) // gcd(X, Y)

def caesar_cipher(text, num):
    result = []
    num = num % 26  # normalize shifts

    for char in text:
        if 'a' <= char <= 'z':
            # shift lowercase
            shifted = chr((ord(char) - ord('a') + num) % 26 + ord('a'))
            result.append(shifted)
        elif 'A' <= char <= 'Z':
            # shift uppercase
            shifted = chr((ord(char) - ord('A') + num) % 26 + ord('A'))
            result.append(shifted)
        else:
            # leave numbers, spaces, punctuation unchanged
            if char == ' ':
                result.append(char)
            else:
                return 'error: invalid input'

    return 'the ciphertext is: '+''.join(result)

if __name__ == '__main__':
    main()