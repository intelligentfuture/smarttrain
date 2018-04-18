import network
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.ifconfig(('10.0.0.1', '255.255.255.0', '10.0.0.1', '10.0.0.1'))
ap.config(essid='CTRL_CENT_GW_NODE', password='ACDINN--')
ap.config(authmode=3, channel=11, hidden=True)

import usocket as socket

def decodeData(recv, addr):
    try:
        if (recv[8] == 'F' and recv[9] == 'F' and recv[10:18] == "FFFFFFFF"):
            connection.sendto("ACCEPT\n", addr)
            print("!!JOIN:", addr)
        else:
            print(':'+txt)
    except Exception as e:
        print("!!ERR:", e)


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
                                decodeData(txt, addr)
                            else:
                                print("!!ERR:", txt, len(txt))
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