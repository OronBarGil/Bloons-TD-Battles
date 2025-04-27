import socket
import time

from tcp_by_size import *
import threading
import pickle


all_to_die = False
ready_clients = 0
threads = []
sockets = []

send_player_num = 'PLRN' #player number
send_balloons = 'SBLN'
send_monkeys = 'SMKS'
send_health = 'SOHP'
exit_msg = 'EXIT'
client1 = False
def handle_client(sock, tid, addr):
    global all_to_die, threads, sockets, ready_clients, client1
    print(f'New Client number {tid} from {addr}')


    #this player is now player1
    if not client1:
        player_num = "1"
        client1 = True
    else:
        player_num = "2"

    ready = False
    finish = False
    got_ready = False
    while not ready:
        try:
            if not got_ready:
                data = recv_by_size(sock)
                if data == "READY":
                    ready_clients += 1
                    got_ready = True
                elif data == exit_msg:
                    sockets.remove(sock)
                    if got_ready:
                        ready_clients -= 1
                    finish = True
                    if player_num == "1":
                        client1 = False
                    break
        except:
            print("error")

        if ready_clients == 2:
            send_with_size(sock, "START")
            ready = True



    to_send = send_player_num + '~' + player_num
    send_with_size(sock, to_send)
    while not finish:
        data = recv_by_size(sock, 'bytes')
        if data[:4].decode() == send_balloons:
            balloon_group = data[5:]
            to_send = send_balloons.encode() + '~'.encode() + balloon_group
            for socket in sockets:
                if socket != sock:
                    send_with_size(socket, to_send)
        elif data[:4].decode() == send_monkeys:
            monkey_group = data[5:]
            to_send = send_monkeys.encode() + '~'.encode() + monkey_group
            for socket in sockets:
                if socket != sock:
                    send_with_size(socket, to_send)
        #decode
        elif data[:4].decode() == send_health:
            data = data.decode()
            to_send = send_health + '~' + data[5:]
            for socket in sockets:
                if socket != sock:
                    send_with_size(socket, to_send)
        elif data[:4].decode() == exit_msg:
            for socket in sockets:
                if socket != sock:
                    send_with_size(socket, exit_msg)
            finish = True





def main():
    global all_to_die, threads, sockets

    srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv_sock.bind(('0.0.0.0', 12345))
    srv_sock.listen(2)
    tid = 1
    while True:
        try:
            time.sleep(1)
            if len(sockets) <= 2:
                client_socket, addr = srv_sock.accept()
                sockets.append(client_socket)
                t = threading.Thread(target=handle_client, args=(client_socket, str(tid), addr))
                t.start()
                threads.append(t)
                tid += 1
        except socket.error as err:
            print('socket error', err)
            break
    all_to_die = True
    for t in threads:
        t.join()

if __name__ == '__main__':
    main()
