import socket
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
                            else:
                                print("!!ERR: TXT", txt, len(txt))
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