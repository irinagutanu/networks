# UDP client
import socket
import logging
import time
import threading

logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

port = 10001
adresa = '172.111.0.14'
server_address = (adresa, port)

data_max = 52
window_size = 10
first_value = 1 # First value of the current window
send_timeout = 0.1
buffsize = 4096
acknowledged_set = [];


def receive():
    while True:
        data, address = sock.recvfrom(buffsize)
        logging.info('Received %s back from %s', data, address)
        if int(data) < first_value:
            logging.info('Value %s was already received!', data)
        if acknowledged_set.count(data) == 0 and int(data) >= first_value and int(data) < first_value + window_size:
            acknowledged_set.append(data)


def update():
    global first_value
    while True:
        while acknowledged_set.count(str(first_value)) != 0:
            acknowledged_set.remove(str(first_value))
            first_value = first_value + 1


t_receive = threading.Timer(0, receive)
t_receive.start()

t_update = threading.Timer(0, update)
t_update.start()

#def print_ack():
    #while True:
        #print acknowledged_set
        
#t_print = threading.Timer(0,print_ack)
#t_print.start()


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
        time.sleep(1)
        logging.info("Client sent no. %d - Ended", data_max)
        t_receive.cancel()
        logging.info("Receive thread ended")
        t_update.cancel()
        logging.info("Updatethread ended")
        sock.close()
        logging.info("Socket closed")
        break
    
logging.info("Out of while loop")

#time.sleep(1)
#sock.close()
#t_receive.cancel()
#t_update.cancel()