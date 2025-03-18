#!/usr/bin/python3
import math
import base64
import random
import socket

def xor(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])


class LCG:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.mod = 2 ** 16
        self.state = 0

    def next(self):
        self.state = (self.a * self.state + self.b) % self.mod
        return self.state

def fetch_data_from_remote(host, port):
    socket_data = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        socket_data = s.recv(4096)
    except Exception as e:
        print(f"Failed to fetch data from remote: {e}")
    finally:
        s.close()
    return socket_data.decode("ASCII").strip() if socket_data else None

def brute_force_decrypt(encrypted_base64):
    try:
        ciphertext = base64.b64decode(encrypted_base64)
    except Exception as e:
        print(f"Failed to decode base64 data: {e}")
        return None

    for a in range(1337, 10001):
        for b in range(1337, 10001):
            try:
                lcg = LCG(a, b)
                states = (lcg.next() for _ in range(len(ciphertext) // 2))
                key = b"".join(state.to_bytes(2, "little") for state in states)

                plaintext_bytes = xor(ciphertext, key)
                plaintext = plaintext_bytes.decode("ASCII")
                
                if "SpeishFlag" in plaintext:
                    print(f"flag found: {plaintext}")
                    return plaintext
            except Exception:
                continue

    print("No valid decryption found.")
    return None


if __name__ == '__main__':
    # flag = "This_Is_NOT_SpeishFlag{asdfg_not_that_easy}"
    # plaintext = "Stay your hand! Gotcha!\n" + \
    #     "You do not know this part, \n" + \
    #     "but it ends with a\n" + flag
    # # note: message is always ASCII!
    # bintext = plaintext.encode("ASCII")

    # params = [random.randint(1337, 10000) for _ in (1, 2)]
    # lcg = LCG(*params)
    # states = [lcg.next() for _ in range(math.ceil(len(bintext) / 2))]
    # key = b"".join([state.to_bytes(2, "little") for state in states])

    # ciphertext = xor(bintext, key)
    # print(base64.b64encode(ciphertext).decode("ASCII"))
    remote_host = "isc2024.1337.cx"
    remote_port = 11046
    encrypted_base64 = fetch_data_from_remote(remote_host, remote_port)
    if encrypted_base64:
        brute_force_decrypt(encrypted_base64)
