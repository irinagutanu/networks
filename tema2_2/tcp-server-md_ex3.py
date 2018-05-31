import socket
import logging
import time

logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 10000
adresa = '0.0.0.0'
server_address = (adresa, port)
sock.bind(server_address)
logging.info("Serverul a pornit pe %s si portnul portul %d", adresa, port)
sock.listen(5)

logging.info('Asteptam conexiunea...')
conexiune, address = sock.accept()
logging.info("Handshake cu %s", address)

while True:
    data = conexiune.recv(1) #1 bit primit
    logging.info('Content primit: "%s"', data)
    data = str(data).upper()
    logging.info('Content trimis: "%s"', data)
    conexiune.send(data)

conexiune.close()
sock.close()
