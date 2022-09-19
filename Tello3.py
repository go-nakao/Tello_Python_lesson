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


print('\r\n\r\nTello Python3 Tech Blog.\r\n')


# 新規作成コード
while True:
    try:
        sent = sock.sendto('command'.encode(encoding="utf-8"), tello_address)
        print('command')
        data, _ = sock.recvfrom(1518)  # コマンドの送信結果をdataに入れて表示させる。
        print(data.decode(encoding="utf-8"))
        time.sleep(1)
        sent = sock.sendto('streamon'.encode(encoding="utf-8"),
                           tello_address)  # Tello Video受信のためのコマンドstreamonを送信
        print('streamon')
        data, _ = sock.recvfrom(1518)
        print(data.decode(encoding="utf-8"))
        time.sleep(5)

        # 離陸
        sent = sock.sendto('takeoff'.encode(encoding="utf-8"), tello_address)
        print('takeoff')
        data, _ = sock.recvfrom(1518)
        print(data.decode(encoding="utf-8"))
        time.sleep(10)
        # 前方へ移動
        sent = sock.sendto('forward 100'.encode(
            encoding="utf-8"), tello_address)
        print('forward')
        time.sleep(5)
        # 右旋回
        sent = sock.sendto('cw 90'.encode(encoding="utf-8"), tello_address)
        print('cw')
        data, _ = sock.recvfrom(1518)
        print(data.decode(encoding="utf-8"))
        time.sleep(5)
        # 上昇
        sent = sock.sendto('up 50'.encode(encoding="utf-8"), tello_address)
        print('up')
        data, _ = sock.recvfrom(1518)
        print(data.decode(encoding="utf-8"))
        time.sleep(5)
        # 後退
        sent = sock.sendto('back 100'.encode(encoding="utf-8"), tello_address)
        print('back')
        data, _ = sock.recvfrom(1518)
        print(data.decode(encoding="utf-8"))
        time.sleep(5)
        # 着陸
        sent = sock.sendto('land'.encode(encoding="utf-8"), tello_address)
        print('land')
        data, _ = sock.recvfrom(1518)
        print(data.decode(encoding="utf-8"))
        time.sleep(5)
        # ストリーミング終了
        sent = sock.sendto('streamoff'.encode(encoding="utf-8"), tello_address)
        print('video end')
        data, _ = sock.recvfrom(1518)
        print(data.decode(encoding="utf-8"))
        time.sleep(3)
        # 終了
        msg = 'end'
        print('end:ok')
        data, _ = sock.recvfrom(1518)
        print(data.decode(encoding="utf-8"))

        if 'end' in msg:  # endが入力されたら、ソケット終了
            print('Exit...')
            sock.close()
            break

    except KeyboardInterrupt:
        print('\n . . .\n')
        sock.close()  # 通信終了
        break
