import socket
import time
import random
import threading
servip = '0.0.0.0'
port = 80
connections = 0
max_conn = 10
conn_persec = 0
connected_ips = []
print("                 _   _    _____  _____        _____    _____           _       _   ")
print("     /\         | | (_)  |  __ \|  __ \      / ____|  / ____|         (_)     | |  ")
print("    /  \   _ __ | |_ _   | |  | | |  | | ___| (___   | (___   ___ _ __ _ _ __ | |_ ")
print("   / /\ \ | '_ \| __| |  | |  | | |  | |/ _  \___ \   \___ \ / __| '__| | '_ \| __|")
print("  / ____ \| | | | |_| |  | |__| | |__| | (_) |___) |  ____) | (__| |  | | |_) | |_ ")
print(" /_/    \_\_| |_|\__|_|  |_____/|_____/ \___/_____/  |_____/ \___|_|  |_| .__/ \__|")
print("                                                                        | |       ")
print("                                                                        |_|       ")
print(" Script By DrSquid")
print("")
print("[+] IP to be protected:", servip)
print("[+] At Port:", port)
blacklist = []
stopped_midway = False
def conn_timer():
    time.sleep(1)
    global conn_persec
    conn_persec = 0
conn_msg = True
while True:
    try:
        print("")
        max_conn = int(input("[+] What is the max connections that can connect to the server?: "))
        break
    except:
        print("[+] Invalid Input.")
print("[+] Server is up and running!")
time.sleep(1)
print("")
print("[+] Server is now accepting connections.")
def listen():
    while True:
        accept_conn = True
        global connections
        global max_conn
        global conn_msg
        global stopped_midway
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((servip, port))
        if connections < max_conn:
            if accept_conn:
                s.listen(1)
                conn, ip = s.accept()
                print("[+]", ip, "has connected.")
                if connections <= max_conn and ip_conn not in blacklist:
                    print("[+] Connection to server accepted.")
                elif connections <= max_conn and ip_conn in blacklist:
                    conn.shutdown(1)
                    conn.close()
                    print(f"[+] Refusing Connection from IP: {ip}")
                elif connections > max_conn:
                    print("[+] Refusing incoming connection:", ip)
                    conn.shutdown(1)
                    conn.close()
                ip_conn = ip[0]
                timer = threading.Thread(target=conn_timer)
                timer.start()
                conn_persec += 1
                if conn_persec >= 100:
                    print("")
                    print("[+] Potential DDoS Attack Recognized.")
                    stopped_midway = True
                    connections = max_conn + 1
                connections += 1
        else:
            if conn_msg:
                print("")
                if not stopped_midway:
                    print(f"[+] Maximum Amount of Connections reached({max_conn})")
                print("[+] No longer Accepting Incoming Connections.")
                print("")
                print("[+] Checking if server IP can still be resolved.....")
                serverIP = s.getsockname()
                try:
                    print("[+] Server is still up and running!")
                    print(f"[+] IP: {serverIP[0]}")
                except:
                    print("[+] Server is down.")
                conn_msg = False
                accept_conn = False
listener = threading.Thread(target=listen)
listener.start()
