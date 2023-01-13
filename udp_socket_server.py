import socket
import logging
import time
import os
import sys
import argparse

def main(UDP_PORT, SOCKET_TYPE):
    # here we prioritize arguments over environement variables
    if UDP_PORT is None:
        UDP_PORT = os.getenv("UDP_PORT", "5005")
    UDP_PORT = int(UDP_PORT)

    if SOCKET_TYPE is None:
        SOCKET_TYPE = os.getenv("SOCKET_TYPE", "ipv6")

    if SOCKET_TYPE.lower() == "ipv6":
        UDP_IP = "::" # localhost
        sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    elif SOCKET_TYPE.lower() == "ipv4":
        UDP_IP = "0.0.0.0" # localhost
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
        logging.error("Socket Type bad definition.")
        sys.exit(-1)
    
    sock.bind((UDP_IP, UDP_PORT))

    logging.info("Initializing UDP server")
    logging.debug(f"IP: {UDP_IP}")
    logging.debug(f"Port: {UDP_PORT}")

    logging.info("Waiting for messages...")
    logging.debug(f"{SOCKET_TYPE}")
    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        logging.debug(f"received message: {data}")

if __name__ == "__main__":
    argParser = argparse.ArgumentParser(description='UDP Socket Server Example')
    argParser.add_argument("-p", "--port", help="Destination port", type=str)
    argParser.add_argument("-s", "--socket_type", help="Socket Type: ipv4, ipv6", type=str)
    args = argParser.parse_args()

    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    main(args.port, args.socket_type)
    
# docker build . -f Dockerfile -t socket_server