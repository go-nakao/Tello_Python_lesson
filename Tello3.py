import threading
import socket
import time


# TelloのプライベートIPとポート番号
tello_ip = '192.168.10.1'
tello_port = 8889
tello_address = (tello_ip, tello_port)

# hostのプライベートIPとポート番号
host_ip = '192.168.10.2'
host_port = 8889
host_address = (host_ip, host_port)

# UDP通信の確立
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


print('\r\n\r\nTello Python3 Tech Blog.\r\n')

# recvThread create
recvThread = threading.Thread(target=recv)
recvThread.start()

# 新規作成コード
while True:
    try:
        sent = sock.sendto('command'.encode(encoding="utf-8"), tello_address)
        print('command')
        time.sleep(5)
        sent = sock.sendto('takeoff'.encode(encoding="utf-8"), tello_address)
        print('takeoff')
        time.sleep(10)
        sent = sock.sendto('land'.encode(encoding="utf-8"), tello_address)
        print('land')
        time.sleep(5)

        msg = 'end'
        print('end:ok')

        # if not msg:
        #     break
        if 'end' in msg:  # endが入力されたら、ソケット終了
            print('...')
            sock.close()
            break

    except KeyboardInterrupt:
        print('\n . . .\n')
        sock.close()  # 通信終了
        break
