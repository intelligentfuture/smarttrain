import network
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.ifconfig(('10.0.0.1', '255.255.255.0', '10.0.0.1', '10.0.0.1'))
ap.config(essid='CTRL_CENT_GW_NODE', password='ACDINN--')
ap.config(authmode=3, channel=11, hidden=True)

import usocket as socket

def listen():
    connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind(('0.0.0.0', 55555))
    while True:
        try:
            while True:
                try:
                    rcv, addr = connection.recvfrom(24)
                    for data in rcv.decode('ascii').split(':'):
                        data = data.replace("\r", "")
                        data = data.replace("\n", "")
                        if data:
                            txt = data.strip()
                            if(len(txt) == 22):
                                print(':'+txt)
                            elif(len(txt) == 4):
                                if(txt == "JOIN"):
                                    connection.sendto("ACCEPT\n", addr)
                                    print("!!JOIN request from", addr)
                            elif(len(txt) > 4):
                                print("!!ER:", txt, len(txt))
                                connection.sendto("RESEND\n", addr)
                except Exception as e:
                    print('!!connection:', e)
                    break
        except Exception as e:
            print('!!socket:', e)
                
if __name__ == "__main__":
    try:
        listen()
    except Exception as e:
        print("!!main", e)