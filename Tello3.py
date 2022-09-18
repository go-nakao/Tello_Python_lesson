import threading
import socket
# import sys
import time
import platform


# TelloのプライベートIPとポート番号
tello_ip = '192.168.10.1'
tello_port = 8889
tello_address = (tello_ip, tello_port)

# hostのプライベートIPとポート番号
host_ip = '192.168.10.2'
host_port = 8889
host_address = (host_ip, host_port)

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(host_address)


def recv():
    count = 0
    while True:
        try:
            data, server = sock.recvfrom(1518)
            print(data.decode(encoding="utf-8"))
        except Exception:
            print('\nExit . . .\n')
            break


print('\r\n\r\nTello Python3 Demo.\r\n')

print('Tello: command takeoff land flip forward back left right \r\n       up down cw ccw speed speed?\r\n')

print('end -- quit demo.\r\n')


# recvThread create
recvThread = threading.Thread(target=recv)
recvThread.start()

while True:
    try:
        python_version = str(platform.python_version())
        version_init_num = int(python_version.partition('.')[0])
       # print (version_init_num)
        if version_init_num == 3:
            msg = input("")
        elif version_init_num == 2:
            msg = input("")

        if not msg:
            break

        if 'end' in msg:
            print('...')
            sock.close()
            break

        # Send data
        msg = msg.encode(encoding="utf-8")
        sent = sock.sendto(msg, tello_address)
    except KeyboardInterrupt:
        print('\n . . .\n')
        sock.close()
        break
