import socket
import logging
import time
import os
import sys
import argparse



def main(UDP_IP, UDP_PORT, SOCKET_TYPE, DEVICE_ID, MESSAGE):
    # here we prioritize arguments over environement variables
    if UDP_IP is None: 
        UDP_IP = os.getenv("DEST_IP", "::1")

    if UDP_PORT is None:
        UDP_PORT = os.getenv("DEST_PORT", "5005")
    UDP_PORT = int(UDP_PORT)
    
    if DEVICE_ID is None:
        DEVICE_ID = os.getenv("DEVICE_ID", "")

    if SOCKET_TYPE is None:
        SOCKET_TYPE = os.getenv("SOCKET_TYPE", "IPV6")

    if MESSAGE is None:
        MESSAGE = f"Hello World from {DEVICE_ID}"
    
    sock = None
    if SOCKET_TYPE.lower() == "ipv6":
        sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) 
    elif SOCKET_TYPE.lower() == "ipv4":
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    else:
        logging.error("socket type bad definition")
        sys.exit(-1)

    logging.info("Initializing UDP Client")
    logging.debug (f"UDP target IP: {UDP_IP}")
    logging.debug (f"UDP target port: {UDP_PORT}")
    logging.debug (f"message: {MESSAGE}")

    while(1):
        logging.debug("Sending message...")
        sock.sendto(MESSAGE.encode('utf-8'), (UDP_IP, UDP_PORT))
        time.sleep(10)


if __name__ == "__main__":
    argParser = argparse.ArgumentParser(description='UDP Socket Client Example')
    argParser.add_argument("-i", "--ip", help="Destination IP", type=str)
    argParser.add_argument("-p", "--port", help="Destination port", type=str)
    argParser.add_argument("-s", "--socket_type", help="Socket Type: ipv4, ipv6", type=str)
    argParser.add_argument("-d", "--deviceid", help="Id of this device", type=str)
    argParser.add_argument("-m", "--message", help="Message to be sent", type=str)
    args = argParser.parse_args()
    
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

    main(args.ip, args.port, args.socket_type, args.deviceid, args.message)

# docker build . -f Dockerfile -t socket_client