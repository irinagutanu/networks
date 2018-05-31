# UDP client
import socket
import logging
import time
import threading
from sets import Set

logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

port = 10000
adresa = '172.111.0.14'
server_address = (adresa, port)

data_max = 50
window_size = 10
first_value = 1 # First value of the current window
send_timeout = 0.1
buffsize = 4096
acknowledged_set = Set([]) # Values in the window that have been acknowledged by the server


def receive():
    while True:
        data, address = sock.recvfrom(buffsize)
        logging.info('Receiving %s back from server', data)
        if (not (data in acknowledged_set)) and int(data) >= first_value and int(data) < first_value + window_size:
            acknowledged_set.add(data)


def update():
    global first_value
    while True:
        while str(first_value) in acknowledged_set:
            acknowledged_set.remove(str(first_value))
            first_value = first_value + 1


t_receive = threading.Timer(0, receive)
t_receive.start()

t_update = threading.Timer(0, update)
t_update.start()


while True:
    crt_first_value = first_value
    for i in range(window_size):
        int_mesaj = i + crt_first_value
        if int_mesaj > data_max:
            break
        mesaj = str(int_mesaj)
        if mesaj in acknowledged_set:
            continue
        logging.info('Sending %s', mesaj)
        time.sleep(send_timeout)
        sent = sock.sendto(mesaj, server_address)

    if first_value > data_max:
        logging.info("Client sent no. %d - Ended", data_max)
        t_receive.cancel()
        t_update.cancel()
        sock.close()
        break

sock.close()
t_receive.cancel()
t_update.cancel()