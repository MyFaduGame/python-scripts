import os
import paramiko
import socket
import sys
import threading

CwD = os.path.dirname(os.path.realpath(__file__))
HOSTKEY = paramiko.RSAKey(filename=os.path.join(CwD,'test_rsa.key'))

class Server(paramiko.ServerInterface):
    
    def __init__(self) -> None:
        self.event = threading.Event()
        
    def check_channel_request(self, kind: str, chanid: int):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    
    def check_auth_password(self, username: str, password: str):
        if (username == 'kernel') and (password == 'kernel'):
            return paramiko.AUTH_SUCCESSFUL
        
if __name__ == "__main__":
    server = '192.168.0.113'
    ssh_port = 22
    try:
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        sock.bind((server,ssh_port))
        print('[+] Listening to Connection ... ')
        client, addr = sock.accept()
    except Exception as e:
        print(f'[-] Listening Failed {e}')
        sys.exit(1)
    else:
        print('[+] Connection Completed! ',client,addr)


    bhSession = paramiko.Transport(client)
    bhSession.add_server_key(HOSTKEY)
    server = Server()
    bhSession.start_server(server=server)
    
    chan = bhSession.accept(20)
    if chan is None:
        print('*** No Channel')
        sys.exit(1)
    
    print('[+] Authenticated!')
    print(chan.recv(1024))
    chan.send("Welcome to bh_ssh")
    try:
        while True:
            command = input("Enter Command: ")
            if command != 'exit':
                chan.send(command)
                r = chan.recv(8192)
                print(r.decode())
            else:
                chan.send('exit')
                print('exiting')
                bhSession.close()
                break
    except KeyboardInterrupt:
        bhSession.close()