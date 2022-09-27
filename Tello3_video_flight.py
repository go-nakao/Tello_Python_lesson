import socket
import time
import threading
import cv2
import numpy as np

# データ受け取り用の関数


def udp_receiver():
    while True:
        try:
            response, _ = sock.recvfrom(1024)
        except Exception as e:
            print(e)
            break

# 新規作成コード


def flight():
    while True:
        try:
            sent = sock.sendto('command'.encode(
                encoding="utf-8"), tello_address)
            print('command')
            time.sleep(5)
            sent = sock.sendto('takeoff'.encode(
                encoding="utf-8"), tello_address)
            print('takeoff')
            time.sleep(10)
            # 前方へ移動
            sent = sock.sendto('forward 100'.encode(
                encoding="utf-8"), tello_address)
            print('forward')
            time.sleep(5)
            # 右旋回
            sent = sock.sendto('cw 90'.encode(encoding="utf-8"), tello_address)
            print('cw')
            time.sleep(5)
            # 上昇
            sent = sock.sendto('up 50'.encode(encoding="utf-8"), tello_address)
            print('up')
            time.sleep(5)
            # 後退
            sent = sock.sendto('back 100'.encode(
                encoding="utf-8"), tello_address)
            print('back')
            time.sleep(5)
            sent = sock.sendto('land'.encode(encoding="utf-8"), tello_address)
            print('land')
            time.sleep(5)
            msg = 'end'
            print('end:ok')

            if 'end' in msg:  # endが入力されたら、ソケット終了
                print('Exit...')
                sock.close()
                break

        except KeyboardInterrupt:
            print('\n . . .\n')
            sock.close()  # 通信終了
            break


# Telloからの映像受信用のローカルIPアドレス、宛先ポート番号
TELLO_CAMERA_ADDRESS = 'udp://@0.0.0.0:11111'

# キャプチャ用のオブジェクト
cap = None

# データ受信用のオブジェクト備
response = None


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

# 受信用スレッドの作成
thread = threading.Thread(target=udp_receiver, args=())
thread.daemon = True
thread.start()

# コマンドモード
sock.sendto('command'.encode('utf-8'), tello_address)

time.sleep(1)

# カメラ映像のストリーミング開始
sock.sendto('streamon'.encode('utf-8'), tello_address)

time.sleep(5)

if cap is None:
    cap = cv2.VideoCapture(TELLO_CAMERA_ADDRESS)

if not cap.isOpened():
    cap.open(TELLO_CAMERA_ADDRESS)

time.sleep(1)

thread = threading.Thread(target=flight)
thread.start()

while True:
    ret, frame = cap.read()

    # 動画フレームが空ならスキップ
    if frame is None or frame.size == 0:
        continue

    # カメラ映像のサイズを半分にしてウィンドウに表示
    frame_height, frame_width = frame.shape[:2]
    frame = cv2.resize(frame, (int(frame_width/2), int(frame_height/2)))

    cv2.imshow('Tello Camera View', frame)

    # qキーで終了
    if cv2.waitKey(1) & 0xFF == ord('q'):

        break
cap.release()
cv2.destroyAllWindows()

# ビデオストリーミング停止
sock.sendto('streamoff'.encode('utf-8'), tello_address)


print('\r\n\r\nTello Python3 Tech Blog.\r\n')
